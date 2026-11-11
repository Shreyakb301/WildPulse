"""Reproducible camera-trap animal-presence evaluation, scored by sequence."""
import argparse
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import time
from urllib.parse import quote
from urllib.request import urlopen
import zipfile

METADATA_URL = 'https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/KRU/SnapshotKruger_S1_v1.0.json.zip'
IMAGE_BASE = 'https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/KRU/KRU_public/'
METADATA_SHA256 = '3a90de11592822817c61f384df4732b3e9f17903593ed6b48ef15d1f6a5f1f9a'
MODEL = 'MDV6-yolov10-e'
SEED = 'wildpulse-pilot-2026-11-10'
EXCLUDED = {f'KRU_S1_1_R1_IMAG{n:04d}' for n in (29, 30, 31, 42, 43, 44)}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False))


def prepare(root, per_class=None, config=None):
    config = config or dict(dataset='Snapshot Kruger S1', metadata_url=METADATA_URL,
                            metadata_sha256=METADATA_SHA256, image_base=IMAGE_BASE,
                            seed=SEED, per_class=10, spread_cameras=False)
    per_class = per_class if per_class is not None else config['per_class']
    root.mkdir(parents=True, exist_ok=True)
    raw = urlopen(config['metadata_url'], timeout=60).read()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != config['metadata_sha256']:
        raise ValueError('Metadata changed; inspect before sampling')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        metadata = json.loads(archive.read(next(n for n in archive.namelist() if n.endswith('.json'))))
    categories = {c['id']: c['name'] for c in metadata['categories']}
    labels, groups = defaultdict(set), defaultdict(list)
    for annotation in metadata['annotations']:
        labels[annotation['seq_id']].add(categories[annotation['category_id']])
    for image in metadata['images']:
        groups[image['seq_id']].append(image)
    pools = {False: [], True: []}
    for seq_id, images in groups.items():
        names = labels[seq_id]
        if not names or 'human' in names or ('empty' in names and len(names) > 1):
            continue
        if any(i.get('corrupt', False) or Path(i['file_name']).stem in EXCLUDED for i in images):
            continue
        if any(i.get('seq_num_frames') != len(images) for i in images):
            continue
        animal = names != {'empty'}
        pools[animal].append(dict(seq_id=seq_id, animal_present=animal,
                                 labels=sorted(names), files=sorted(i['file_name'] for i in images)))
    chosen = []
    for animal in (False, True):
        ordered = sorted(pools[animal], key=lambda s: hashlib.sha256((config['seed']+s['seq_id']).encode()).hexdigest())
        if config.get('spread_cameras'):
            buckets = defaultdict(list)
            for sequence in ordered:
                buckets[sequence['files'][0].split('/')[1]].append(sequence)
            ordered = [items[round_index] for round_index in range(max(map(len, buckets.values())))
                       for items in buckets.values() if round_index < len(items)]
        if len(ordered) < per_class:
            raise ValueError('Insufficient complete sequences')
        chosen.extend(ordered[:per_class])
    manifest = dict(dataset=config['dataset'], source=config['metadata_url'],
                    metadata_sha256=digest, seed=config['seed'], per_class=per_class,
                    image_base=config['image_base'], spread_cameras=config.get('spread_cameras', False),
                    primary_threshold=config.get('primary_threshold'),
                    available_empty=len(pools[False]), available_animal=len(pools[True]),
                    sequences=chosen)
    save(root/'manifest.json', manifest)
    count = 0
    for sequence in chosen:
        for name in sequence['files']:
            path = root/'images'/name
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_bytes(urlopen(config['image_base']+quote(name, safe='/'), timeout=60).read())
            count += 1
        print('Downloaded sequence', sequence['seq_id'], sequence['labels'], flush=True)
    print(f'PREPARED {len(chosen)} sequences and {count} images', flush=True)
    return manifest


def score(sequences, thresholds=(0.2, 0.3, 0.5, 0.8)):
    metrics = []
    for threshold in thresholds:
        tp = fp = tn = fn = 0
        for sequence in sequences:
            predicted = sequence['max_animal_confidence'] >= threshold
            actual = sequence['animal_present']
            tp += actual and predicted
            fp += not actual and predicted
            tn += not actual and not predicted
            fn += actual and not predicted
        ratio = lambda a, b: a/b if b else None
        metrics.append(dict(threshold=threshold, tp=tp, fp=fp, tn=tn, fn=fn,
                            recall=ratio(tp, tp+fn), specificity=ratio(tn, tn+fp),
                            precision=ratio(tp, tp+fp), accuracy=ratio(tp+tn, len(sequences))))
    return metrics


def evaluate(root):
    import cv2
    import sparrow_engine as spe
    manifest = json.loads((root/'manifest.json').read_text())
    spe.download_model(MODEL)
    spe.init(device='cpu')
    records = []
    for sequence in manifest['sequences']:
        frames = []
        for name in sequence['files']:
            path = root/'images'/name
            if cv2.imread(str(path)) is None:
                raise ValueError(f'Invalid image {name}; cannot score incomplete sequence')
            start = time.perf_counter()
            result, = spe.detect(path, model=MODEL, threshold=0.2)
            elapsed = time.perf_counter()-start
            frames.append(dict(file=name, wall_seconds=elapsed,
                               detections=[dict(label=d.label, confidence=d.confidence,
                                                bbox_xyxy=[d.bbox.x_min,d.bbox.y_min,d.bbox.x_max,d.bbox.y_max])
                                           for d in result.detections]))
            print('Detected', name, f'{elapsed:.2f}s', flush=True)
        maximum = max((d['confidence'] for f in frames for d in f['detections'] if d['label']=='animal'), default=0)
        records.append(dict(**sequence, frames=frames, max_animal_confidence=maximum))
        save(root/'progress.json', records)
        print('Completed sequence', len(records), '/', len(manifest['sequences']), flush=True)
    report = dict(model=MODEL, engine_version=spe.__version__, device=str(spe.active_device()),
                  dataset=manifest['dataset'], primary_threshold=manifest.get('primary_threshold'),
                  evaluation_unit='complete sequence', sequences=records, metrics=score(records),
                  notes='Balanced exploratory pilot; not natural prevalence, species accuracy, box localization accuracy, or a known training-disjoint test. Sequence positive if any frame has an animal box at threshold. No threshold selected from this pilot.')
    save(root/'evaluation_results.json', report)
    print('EVALUATION COMPLETE', json.dumps(report['metrics'], indent=2), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'evaluate'])
    parser.add_argument('--root', type=Path, default=Path('/content/WildPulse/evaluation'))
    parser.add_argument('--config', type=Path, help='Dataset preparation configuration JSON')
    args = parser.parse_args()
    if args.stage == 'prepare':
        prepare(args.root, config=json.loads(args.config.read_text()) if args.config else None)
    else:
        evaluate(args.root)
