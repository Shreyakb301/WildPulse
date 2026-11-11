# WildPulse project log

## 2026-11-10 — Colab setup continuation

- Opened Wildlife.ipynb in connected Chrome. The supplied `authuser=1` selected an account without access; switching to the existing Colab account resolved access without changing sharing.
- Existing notebook outputs showed starter ZIP extraction and a PytorchWildlife installation with dependency conflicts.
- Executed diagnostic cell: Python 3.13.18, PytorchWildlife 1.3.1, torch 2.14.1+cpu, torchvision 0.29.1+cpu, ultralytics 8.4.210.
- PytorchWildlife import failed: `ImportError: cannot import name 'ResolvedRevision' from 'huggingface_hub'`. Installation presence does not mean usable inference.
- Verified six JPEG files in `/content/WildPulse/sample_images`: IMAG0029, 0030, 0031, 0042, 0043, 0044 (prefix `KRU_S1_1_R1_`).
- Installed and imported sparrow-engine 0.1.32 from PyPI successfully. Inspected its documented API in the notebook.
- Started downloading MegaDetector `MDV6-yolov10-e` through `sparrow_engine.download_model` and testing the first image. Result pending at this entry.
- Model download completed in 48.230 seconds with MD5 verification. First CPU call completed in 15.200 seconds and returned one animal detection for IMAG0029 (confidence approximately 0.9794).
- First six-image loop stopped while saving a Pillow JPEG: `TypeError: function takes at most 16 arguments (17 given)`. Detection itself succeeded. Traceback was in Pillow's JPEG encoder; a loaded/native package mismatch after installation is suspected, not proven.
- Changed preview output to OpenCV and restarted the six-image loop. IMAG0029 and IMAG0030 both completed, each with one animal detection; remaining results pending.
- Created local `run_baseline_sparrow.py` and `requirements-baseline.txt` for a repeatable replacement baseline. Only syntax validation has been performed locally; actual inference runs in Colab.

These are local workspace notes. No claim is made that they are saved to Google Drive or the Colab runtime.

### Completed baseline

- All six images completed using sparrow-engine 0.1.32, MDV6-yolov10-e, CPU, threshold 0.2.

| Image suffix | Wall seconds | Predictions (rounded confidence) |
| --- | ---: | --- |
| IMAG0029 | 17.181 | animal 0.979 |
| IMAG0030 | 14.572 | animal 0.976 |
| IMAG0031 | 15.705 | person 0.587; animal 0.301 |
| IMAG0042 | 15.991 | no detections |
| IMAG0043 | 14.688 | animal 0.299; animal 0.276 |
| IMAG0044 | 14.933 | animal 0.408 |

- Mean warmed wall time: 15.51159211866669 seconds/image. Includes decoding/API overhead; follows cold and debugging calls. No accuracy claim.
- Verified runtime artifacts: 6 baseline JSON records, 6 MegaDetector JSON image entries, 6 annotated JPEGs. CSV and contact sheet were also created.
- Created `/content/WildPulse_baseline_results.zip`, verified size 6,878,656 bytes.
- Wrote runtime `/content/WildPulse/PROJECT_LOG.md` (676 bytes) and `PROJECT_NOTES.md` (598 bytes), copied both into the result bundle. These runtime versions are concise summaries, not identical to these local files.
- Colab showed a JavaScript output loading error (expired login or third-party cookies suggested by Colab). Download through Files failed with the same error. Reloaded the saved notebook to try to restore display/download functionality. Download not yet confirmed.
- Reload restored the displayed contact sheet. Visually reviewed both rows: clear large-animal boxes in IMAG0029/0030; small uncertain boxes in later images. This is not a ground-truth annotation review. A second bundle download did not produce a confirmed download; Colab reported inability to connect to reCAPTCHA service. A contact-sheet media export also timed out, and browser control reset. The notebook's saved outputs survived the prior reload; the result archive remains unconfirmed locally.
