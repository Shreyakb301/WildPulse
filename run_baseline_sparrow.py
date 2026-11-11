"""WildPulse six-image CPU detection baseline. Requires sparrow-engine==0.1.32."""
import json
import statistics
import time
from pathlib import Path

import sparrow_engine as spe
import cv2

MODEL = 'MDV6-yolov10-e'
THRESHOLD = 0.2


def main(root=Path('/content/WildPulse')):
    images = sorted((root / 'sample_images').glob('*.jpeg'))
    assert len(images) == 6, f'Expected six images, found {len(images)}'
    output = root / 'baseline_output'
    output.mkdir(exist_ok=True)
    start = time.perf_counter()
    spe.download_model(MODEL)
    download_seconds = time.perf_counter() - start
    spe.init(device='cpu')
    start = time.perf_counter()
    spe.detect(images[0], model=MODEL, threshold=THRESHOLD)
    cold_seconds = time.perf_counter() - start
    records, results = [], []
    for path in images:
        start = time.perf_counter()
        result, = spe.detect(path, model=MODEL, threshold=THRESHOLD)
        seconds = time.perf_counter() - start
        results.append(result)
        detections = [dict(label=d.label, label_id=d.label_id,
                           confidence=d.confidence,
                           bbox_xyxy=[d.bbox.x_min, d.bbox.y_min,
                                      d.bbox.x_max, d.bbox.y_max])
                      for d in result.detections]
        records.append(dict(image=path.name, wall_seconds=seconds,
                            processing_time_ms=result.processing_time_ms,
                            detections=detections))
        frame = cv2.imread(str(path))
        assert frame is not None, path
        annotated = spe.draw_detections(frame, result, thickness=4)
        assert cv2.imwrite(str(output / (path.stem + '_detected.jpg')), annotated)
        labels = ', '.join(f"{d['label']} {d['confidence']:.3f}" for d in detections) or 'no detections'
        print(f'{path.name}: {seconds:.3f}s | {labels}', flush=True)
    summary = dict(engine='sparrow-engine', engine_version=spe.__version__,
                   model=MODEL, device=str(spe.active_device()), threshold=THRESHOLD,
                   image_count=len(records), model_download_check_seconds=download_seconds,
                   cold_first_call_seconds=cold_seconds,
                   mean_warm_wall_seconds=statistics.mean(r['wall_seconds'] for r in records),
                   records=records,
                   notes='Six-image exploratory CPU run. Warm timings follow one cold call; include image I/O and Python API overhead. Not an accuracy, GPU, or throughput benchmark. Detection labels are not species identities.')
    (output / 'baseline_results.json').write_text(json.dumps(summary, indent=2))
    spe.export(results, format='megadet', output=output/'megadetector_results.json', model_id=MODEL)
    spe.export(results, format='csv', output=output/'detections.csv', model_id=MODEL)
    print('SUMMARY:', json.dumps({k:v for k,v in summary.items() if k != 'records'}, indent=2))
    return summary


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-dir', type=Path, default=Path('/content/WildPulse'))
    main(parser.parse_args().project_dir)
