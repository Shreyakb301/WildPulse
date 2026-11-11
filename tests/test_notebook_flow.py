"""Check notebook state transitions without Colab or model dependencies."""
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

NOTEBOOK = json.loads((Path(__file__).resolve().parents[1]/'WildPulse_Image_Review.ipynb').read_text())


def cell_containing(text):
    return next(''.join(c['source']) for c in NOTEBOOK['cells']
                if c['cell_type']=='code' and text in ''.join(c['source']))


class NotebookFlow(unittest.TestCase):
    def modules(self, uploaded):
        files = types.SimpleNamespace(upload=lambda: uploaded)
        google = types.ModuleType('google')
        colab = types.ModuleType('google.colab')
        colab.files = files
        ipython = types.ModuleType('IPython')
        display = types.ModuleType('IPython.display')
        display.display = lambda *a, **kw: None
        display.Image = lambda **kw: None
        return {'google': google, 'google.colab': colab,
                'IPython': ipython, 'IPython.display': display}

    def test_cancelled_upload_clears_old_results(self):
        state = dict(Path=Path, summary={'old': True}, bundle=Path('old.zip'), images=Path('old'))
        with patch.dict('sys.modules', self.modules({})):
            with self.assertRaisesRegex(ValueError, 'No images selected'):
                exec(cell_containing('uploaded = files.upload()'), state)
        self.assertIsNone(state['bundle'])
        self.assertIsNone(state['images'])

    def test_invalid_upload_does_not_select_partial_batch(self):
        state = dict(Path=Path)
        with patch.dict('sys.modules', self.modules({'good.jpg': b'photo', 'bad.txt': b'text'})):
            with self.assertRaisesRegex(ValueError, 'JPEG or PNG'):
                exec(cell_containing('uploaded = files.upload()'), state)
        self.assertIsNone(state['images'])

    def test_repeated_detection_uses_distinct_results(self):
        outputs = []
        def run(images, output, threshold):
            output.mkdir()
            bundle = output/'results.zip'
            bundle.write_bytes(b'result')
            outputs.append(bundle)
            return dict(successful=1, failed=0, records=[]), bundle
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            images = batch/'images'
            images.mkdir()
            state = dict(Path=Path, batch=batch, images=images, workflow=types.SimpleNamespace(run=run))
            with patch.dict('sys.modules', self.modules({})):
                exec(cell_containing('workflow.run('), state)
                exec(cell_containing('workflow.run('), state)
            self.assertNotEqual(outputs[0], outputs[1])
            self.assertTrue(all(p.is_file() for p in outputs))

    def test_failed_detection_clears_download_target(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            state = dict(Path=Path, batch=batch, images=batch, bundle=Path('old.zip'))
            def fail(*args, **kwargs):
                raise RuntimeError('Detector unavailable')
            state['workflow'] = types.SimpleNamespace(run=fail)
            with patch.dict('sys.modules', self.modules({})):
                with self.assertRaisesRegex(RuntimeError, 'Detector unavailable'):
                    exec(cell_containing('workflow.run('), state)
            self.assertIsNone(state['bundle'])
            with self.assertRaisesRegex(ValueError, 'Complete a detection run'):
                exec(cell_containing('files.download('), state)


if __name__ == '__main__':
    unittest.main()
