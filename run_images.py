"""Run WildPulse on a folder of JPEG or PNG images and package results."""
import argparse
import json
import base64
import hashlib
from pathlib import Path
import time
import zipfile

MODEL = 'MDV6-yolov10-e'



def write_review(output_dir, summary):
    """Create a self-contained review page; human decisions never change predictions."""
    result_bytes = (output_dir/'results.json').read_bytes()
    payload = dict(results_sha256=hashlib.sha256(result_bytes).hexdigest(),
                   model=summary['model'], threshold=summary['threshold'], records=[])
    for record in summary['records']:
        row = dict(image=record['image'], status=record['status'],
                   detections=record.get('detections', []), error=record.get('error'))
        row['preview'] = ('data:image/jpeg;base64,' + base64.b64encode(
            (output_dir/record['preview']).read_bytes()).decode()) if record['status']=='ok' else None
        payload['records'].append(row)
    # Script-safe JSON also protects filenames containing HTML or closing tags.
    encoded = json.dumps(payload, allow_nan=False).replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')
    page = REVIEW_PAGE.replace('__PAYLOAD__', encoded)
    (output_dir/'review.html').write_text(page)


REVIEW_PAGE = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>WildPulse batch review</title>
<style>
body{font:16px system-ui,sans-serif;background:#f4f6f3;color:#17251e;margin:0}main{max-width:1050px;margin:auto;padding:28px}h1{margin-bottom:8px}button,select,textarea{font:inherit}button{background:#175a3e;color:white;border:0;padding:12px 18px;border-radius:8px;cursor:pointer}article{background:white;padding:20px;margin:22px 0;border:1px solid #cad4cc;border-radius:12px}img{display:block;max-width:100%;max-height:520px;margin:12px auto;object-fit:contain}label{display:block;margin:12px 0}select,textarea{display:block;box-sizing:border-box;width:100%;padding:10px;margin-top:6px}textarea{min-height:80px}.muted{color:#46594c}#progress{font-weight:600}header{position:sticky;top:0;background:#f4f6f3;padding:12px 0;border-bottom:1px solid #cad4cc}
</style>
<main><h1>WildPulse batch review</h1>
<p>Inspect each preview, then mark whether the model output looks correct, incorrect or uncertain. Boxes are predictions, not verified animal counts or species labels.</p>
<p class="muted">Download your review before closing or reloading this page. Decisions stay in this page until exported. Original model results remain unchanged.</p>
<header><p id="progress" aria-live="polite"></p><button id="export">Download review JSON</button></header><section id="cards"></section></main>
<script id="batch" type="application/json">__PAYLOAD__</script>
<script>
'use strict';
const batch=JSON.parse(document.getElementById('batch').textContent);
const decisions=batch.records.map(r=>({image:r.image,decision:'not reviewed',notes:''}));
function progress(){document.getElementById('progress').textContent=decisions.filter(d=>d.decision!=='not reviewed').length+' of '+decisions.length+' images reviewed';}
batch.records.forEach((r,i)=>{
 const card=document.createElement('article');
 const heading=document.createElement('h2'); heading.textContent=(i+1)+'. '+r.image; card.append(heading);
 const description=document.createElement('p'); description.textContent=r.status==='ok' ? r.detections.length+' detection boxes at confidence '+batch.threshold : 'Unreadable image: '+r.error; card.append(description);
 if(r.preview){const image=document.createElement('img');image.src=r.preview;image.alt='Detection preview for '+r.image;card.append(image);}
 const label=document.createElement('label');label.textContent='Your assessment';
 const select=document.createElement('select');select.setAttribute('aria-label','Assessment for image '+(i+1));
 for(const value of ['not reviewed','correct','incorrect','uncertain']){const option=document.createElement('option');option.value=value;option.textContent=value;select.append(option);}
 select.addEventListener('change',()=>{decisions[i].decision=select.value;progress();});label.append(select);card.append(label);
 const noteLabel=document.createElement('label');noteLabel.textContent='Review notes';const notes=document.createElement('textarea');notes.setAttribute('aria-label','Notes for image '+(i+1));notes.addEventListener('input',()=>{decisions[i].notes=notes.value;});noteLabel.append(notes);card.append(noteLabel);
 document.getElementById('cards').append(card);
});
progress();
document.getElementById('export').addEventListener('click',()=>{
 const review={schema_version:1,results_sha256:batch.results_sha256,model:batch.model,threshold:batch.threshold,reviews:decisions};
 const url=URL.createObjectURL(new Blob([JSON.stringify(review,null,2)],{type:'application/json'}));
 const link=document.createElement('a');link.href=url;link.download='WildPulse_review.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
</script></html>'''


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
    write_review(output_dir, summary)
    artifacts.append(output_dir/'review.html')
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
