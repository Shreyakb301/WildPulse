"""Run WildPulse on a folder of JPEG or PNG images and package results."""
import argparse
import json
from pathlib import Path
import time
import zipfile

MODEL = 'MDV6-yolov10-e'


def run(images_dir, output_dir, threshold=0.5):
    if not 0 < threshold <= 1:
        raise ValueError('Confidence threshold must be greater than zero and at most one')
    images_dir, output_dir = Path(images_dir), Path(output_dir)
    images = sorted(p for p in images_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png'})
    if not images:
        raise ValueError('Choose at least one JPEG or PNG image')
    # Refuse reuse so an export cannot silently include old previews.
    output_dir.mkdir(parents=True, exist_ok=False)
    import cv2
    import sparrow_engine as spe
    spe.download_model(MODEL)
    spe.init(device='cpu')
    records, results, artifacts = [], [], []
    for index, path in enumerate(images, 1):
        frame = cv2.imread(str(path))
        if frame is None:
            records.append(dict(image=path.name, status='error', error='Image could not be decoded'))
            print(f'{index}/{len(images)} {path.name}: unreadable image', flush=True)
            continue
        start = time.perf_counter()
        result, = spe.detect(path, model=MODEL, threshold=threshold)
        elapsed = time.perf_counter() - start
        preview = output_dir / f'{index:04d}_detected.jpg'
        if not cv2.imwrite(str(preview), spe.draw_detections(frame, result, thickness=4)):
            raise OSError(f'Could not save preview for {path.name}')
        artifacts.append(preview)
        results.append(result)
        records.append(dict(image=path.name, status='ok', preview=preview.name,
                            wall_seconds=elapsed, detections=[dict(label=d.label,
                            confidence=d.confidence, bbox_xyxy=[d.bbox.x_min, d.bbox.y_min,
                            d.bbox.x_max, d.bbox.y_max]) for d in result.detections]))
        print(f'{index}/{len(images)} {path.name}: {len(result.detections)} detections', flush=True)
    summary = dict(model=MODEL, engine_version=spe.__version__, device=str(spe.active_device()),
                   threshold=threshold, successful=sum(r['status']=='ok' for r in records),
                   failed=sum(r['status']=='error' for r in records), records=records,
                   notes='Broad category predictions, not species identification. Confidence is not verified accuracy. Threshold 0.5 is a review default, not a production recommendation. Timings include first-call overhead.')
    report = output_dir/'results.json'
    report.write_text(json.dumps(summary, indent=2, allow_nan=False))
    artifacts.append(report)
    if results:
        for fmt, name in [('csv', 'detections.csv'), ('megadet', 'megadetector_results.json')]:
            target = output_dir/name
            spe.export(results, format=fmt, output=target, model_id=MODEL)
            artifacts.append(target)
    bundle = output_dir/'WildPulse_results.zip'
    with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED) as archive:
        for artifact in artifacts:
            archive.write(artifact, artifact.name)
    return summary, bundle


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('images_dir', type=Path)
    parser.add_argument('output_dir', type=Path, help='New output directory')
    parser.add_argument('--threshold', type=float, default=0.5)
    args = parser.parse_args()
    run(args.images_dir, args.output_dir, args.threshold)
