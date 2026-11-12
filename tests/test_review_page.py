"""Review export preserves prediction provenance and treats filenames as data."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import types
import zipfile
from unittest.mock import patch
from run_images import write_review


class ReviewPage(unittest.TestCase):
    def test_review_page_keeps_predictions_and_safe_filenames(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = [dict(image='</script><script>alert(1)</script>.png', status='ok',
                            preview='preview.jpg', detections=[]),
                       dict(image='broken.png', status='error', error='Cannot decode')]
            summary = dict(model='test', threshold=.5, records=records)
            raw = json.dumps(summary).encode()
            (root/'results.json').write_bytes(raw)
            (root/'preview.jpg').write_bytes(b'preview')
            write_review(root, summary)
            page = (root/'review.html').read_text()
            payload = page.split('<script id="batch" type="application/json">')[1].split('</script>')[0]
            parsed = json.loads(payload)
            self.assertNotIn('<script>', payload)
            self.assertEqual(parsed['records'][0]['image'], records[0]['image'])
            self.assertTrue(parsed['records'][0]['preview'].startswith('data:image/jpeg;base64,'))
            self.assertIsNone(parsed['records'][1]['preview'])
            self.assertEqual(parsed['results_sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual((root/'results.json').read_bytes(), raw)
            self.assertNotIn('https://', page)
            self.assertIn("decision:'not reviewed'", page)

    def test_batch_zip_contains_review_for_empty_detection(self):
        import run_images
        cv2 = types.SimpleNamespace(imread=lambda p: object(),
            imwrite=lambda p, frame: Path(p).write_bytes(b'preview') > 0)
        engine = types.SimpleNamespace(__version__='test', download_model=lambda m: None,
            init=lambda **kw: None, active_device=lambda: 'cpu',
            detect=lambda *a, **kw: [types.SimpleNamespace(detections=[])],
            draw_detections=lambda *a, **kw: object(),
            export=lambda items, format, output, model_id: Path(output).write_text(format))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            images = root/'images'
            images.mkdir()
            (images/'empty.jpg').touch()
            with patch.dict('sys.modules', {'cv2': cv2, 'sparrow_engine': engine}):
                summary, bundle = run_images.run(images, root/'output')
            with zipfile.ZipFile(bundle) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('review.html', archive.namelist())
                self.assertIn('results.json', archive.namelist())
                self.assertEqual(summary['records'][0]['detections'], [])
                self.assertIn('empty.jpg', archive.read('review.html').decode())


if __name__ == '__main__':
    unittest.main()
