# WildPulse project log

## 2026-11-11 — New site protocol locked

- User authorized continuing to a larger independent test. Selected Snapshot Enonkishu, a different site from Kruger; no claim of model-training independence.
- Verified official label reliability is sequence-level and inspected all metadata categories. Pinned metadata SHA256 `380dbab5598e1468f74c8dd19e59c0424d61f6f26532a85a7a0a757b8c87de21`.
- Extended evaluate_sequences.py to support pinned dataset configurations and deterministic camera-spread sampling while preserving the original Kruger defaults. Local syntax, config parsing, and threshold boundary checks passed.
- Prepared 30 complete sequences, 64 images, across all 16 camera locations. Each class uses 15 different locations. Primary threshold 0.5 is locked before inference; other thresholds are secondary checks.
- Added NEW_SITE_EVALUATION.md and enonkishu_config.json. Full inference results are pending at this protocol entry.

## 2026-11-11 — Additional visual examples

- User requested another image set to inspect. Prepared six different frames from the existing verified 42-image pilot: steenbok, elephant, spotted hyena, impala, and two empty-labeled sequences.
- Downloaded selected originals from the official public source and drew the saved detection boxes without rerunning inference. Initial local Python HTTPS download failed because its default CA bundle was missing; retry with the installed certifi trust bundle succeeded with certificate verification enabled.
- Created and visually inspected `evaluation/more_examples/another_example_set.jpg`, plus six individual annotated panels. Species names in titles come from dataset labels; model outputs remain broad animal labels. Empty examples had no retained animal detections at threshold 0.2.
- Images remain in ignored local evaluation storage and are not committed.

## 2026-11-10 — Labeled sequence pilot completed

- Finished every selected sequence: 20 sequences, 42 images, 15 camera locations, no skipped frames or reported inference failures.
- At thresholds 0.2/0.3/0.5/0.8, TP counts were 10/10/10/9, FP counts 5/3/2/2, TN counts 5/7/8/8, and FN counts 0/0/0/1. These are relative to supplied sequence labels.
- Mean timed inference API call: 14.4964 seconds/image on CPU. Downloads and separate OpenCV image-read validation were outside the timer.
- Created an error-review contact sheet and six selected annotated frames without rerunning inference. The two high-confidence empty-label false alarms came from camera 14 and boxed a bright lower-left nighttime foreground region; physical cause not established. Kept original labels unchanged.
- Recovered a local evaluation result bundle, 2,450,144 bytes. SHA256 `10c23bf32fb5378b8d386c745202a3d2066a268a5346a92e137daf385228baac` matched Colab and ZIP integrity checks passed. Recomputed all metrics from exported predictions and verified complete frame membership.
- Added EVALUATION_RESULTS.md and the exact public-source sample manifest. No production threshold selected. Images, archive, and raw predictions remain ignored by Git.

## 2026-11-10 — Labeled sequence pilot setup

- Verified official Snapshot Kruger documentation: labels are reliable at sequence level, not necessarily for individual frames. Chose sequence-level animal presence evaluation.
- Downloaded metadata in Colab and pinned SHA256 `3a90de11592822817c61f384df4732b3e9f17903593ed6b48ef15d1f6a5f1f9a`. Metadata contains 10,604 image records, including human-labeled records whose images are not publicly released.
- Added evaluate_sequences.py with deterministic balanced sampling, complete-sequence checks, original-example exclusions, image validation, per-sequence progress output, and fixed-threshold scoring. Verified scoring against known TP/FP/TN/FN outcomes locally.
- Prepared 20 complete sequences and downloaded 42 images in Colab: 10 empty sequences and 10 animal sequences, with animal labels steenbok, elephant, spotted hyena, and impala.
- Started CPU inference with the existing MDV6-yolov10-e model. First three sequences completed successfully; full results pending at this setup entry.
- Added EVALUATION.md describing the method and limits. Evaluation images and generated outputs are ignored by Git.

## 2026-11-10 — Result recovery and review

- Continued in the user's in-app Colab browser. The runtime and result archive were still present.
- Files-panel download did not yield a confirmed browser download. Added a normal notebook export link containing the existing archive and printed its SHA256. The media-download helper failed and the browser reconnected; recovered the archive from the rendered link through a read-only DOM attribute instead.
- Saved `WildPulse_baseline_results.zip` locally, matched SHA256 `9a6941733d08effee20c5b87976edfdf6ae796ec7c6a09220b9af8621fa83180`, passed ZIP CRC checks, and extracted six records plus previews into ignored `baseline_output/`.
- Inspected the contact sheet and full annotated previews for IMAG0031 and IMAG0043. IMAG0031 has identical person/animal boxes at the right edge, indicating conflicting labels for one region. A person is not visually established. IMAG0043 has overlapping animal boxes with IoU 0.6144; do not count these as two verified animals.
- Filtered existing predictions at thresholds 0.2, 0.3, 0.5, and 0.8 without rerunning inference. Animal box counts were 6, 4, 2, and 2; person counts were 1, 1, 1, and 0. Threshold changes alone do not resolve the conflict.
- Added BASELINE_REVIEW.md and updated README.md to reflect the verified local archive. Kept raw outputs and images excluded from Git.

## 2026-11-10 — GitHub setup

- User requested ongoing GitHub pushes and commit messages of three or four words using letters and spaces only. Saved these preferences in AGENTS.md and PROJECT_NOTES.md.
- Reviewed README files in the user's LoadCheck, RepoLens, and DepotField repositories. Added README.md with the same plain-language approach and relevant feature, stack, setup, results, and engineering-record sections.
- Created the public repository https://github.com/Shreyakb301/WildPulse after the user's explicit request.
- Published README.md with `Add project readme` (b08afb6fd873d13aee58e3e6f2b0a63ed63403c4).
- Published the baseline script, dependencies, ignore rules, project instructions, and project records with `Add wildlife baseline` (9540c6ee489967f9d9aaccff1cf680bb3ffe06d7). Verified the main branch update and fetched AGENTS.md back from GitHub.
- Added a project-directory argument to the standalone script so the README's local setup command works. Python syntax validation passed; inference was not rerun for this documentation and repository setup.
- Connected the local folder to the GitHub remote. GitHub CLI authentication was invalid, so publication used the connected GitHub app instead.

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

## 2026-11-11 — Enonkishu runtime interruption

- First Enonkishu run visibly completed 15 of 30 sequences before Colab disconnected. No final metrics were obtained.
- Reconnected diagnostics: evaluation root, checkpoint, final results and sparrow-engine were absent. The runtime had been replaced.
- Reinstalled the same pinned engine and restarted deterministic preparation with the published configuration. Primary threshold remains 0.5.
- Queued inference with notebook-visible JSON checkpoint download links after each complete sequence. Recovery has not yet been verified.
- Rerun pending at this entry; interrupted-run predictions are excluded from reported results.

### Enonkishu completion and correction

- Reconnect revealed a complete 30-sequence evaluation in saved output and an existing final runtime JSON. Earlier statements that no completed result existed were provisional and superseded by this inspection.
- Checkpoint wrapper failed with recursion after repeated execution; failed attempt excluded. Exact timing of earlier backend completion remains uncertain.
- Exported completed file, verified SHA256, all 30 sequence records and 64 ordered frame memberships; recomputed every maximum and metric locally.
- Primary 0.5: TP15 FP4 TN11 FN0, relative to supplied labels. Reviewed four disagreement frames; two appear to contain animals despite empty labels. No relabeling.
- Saved local ZIP (1327770 bytes), SHA256 b929038a88dab0101f94d04a53ef78851882370bd471184c982235002aa4e1a4; integrity and prediction equality passed.
- Added NEW_SITE_RESULTS.md, enonkishu_manifest.json and README summary. Images and runtime bundles excluded from Git.

2026-11-11: Reviewed all six original frames in the four Enonkishu primary-threshold disagreements. Two likely label disagreements (D02 90, B06 230), one likely foreground-obstruction false alarm (D06 1317, three frames), and one unresolved blur/glare case (B02 259). Observational review only; original labels and metrics unchanged. Images retained locally outside Git.

2026-11-11: Added run_images.py and WildPulse_Image_Review.ipynb for JPEG/PNG upload, preview and ZIP download. Unique output folders prevent stale exports; unreadable files are recorded, unexpected inference errors stop execution. Isolated simulated-detector checks passed for two valid images, one unreadable image, colliding stems, ZIP contents/integrity and output reuse rejection. Notebook code syntax checked for Python 3.11. New notebook live Colab upload/download verification remains pending; no new real inference claimed.

2026-11-11: Opened the published image-review notebook in a fresh Colab CPU session. Setup completed. File chooser automation timed out; native Codex app access was unavailable. Cancelled upload (zero files) and loaded public ENO_S1_B06_R2_IMAG0434.JPG by URL in a clearly marked temporary verification cell. Real run_images workflow processed one image with one animal detection and generated preview, JSON, CSV and MegaDetector JSON. Standard files.download produced no confirmed browser download event. Added and verified direct data-link fallback up to 20 MB. Recovered local WildPulse_workflow_smoke.zip (254717 bytes), SHA256 3a7feb22dbc29e2eed8afa72140c0e32076fbd946ae8eccb375254d7fe2ec502, matching Colab; ZIP CRC and JSON result counts passed. Full file-picker upload remains unverified. Notebook test changes were not saved through the GitHub UI; repository notebook receives only the download fallback.

2026-11-11: Continued notebook usability work. Added a public Enonkishu example option with SHA256 verification, using the same frame previously tested with real inference. Pinned runner download to commit 0d33fd1e4ee26785a45f91eebc61a12771c230f9. Each detection rerun uses a fresh output folder; cancelled/invalid uploads and failed detection runs invalidate the old downloadable result. Added four automated notebook-state tests; all passed. Notebook cells parse as Python 3.11. File-picker and standard download confirmation remain outstanding; no new real inference or complete upload test claimed in this change.

2026-11-11: Tested six user-supplied PNG images through the unchanged run_images workflow in Colab CPU, sparrow-engine 0.1.32, MDV6-yolov10-e, threshold 0.5. Original PNG bytes transferred with matching SHA256 checksums; all six decoded and completed. Animal-box counts in supplied order: 7, 1, 1, 1, 3, 1 (14 boxes); no person/vehicle predictions at this threshold. Maximum scores: 0.9444, 0.9554, 0.9408, 0.9508, 0.9142, 0.9483. Mean API wall time 12.593204 seconds/image, including first-call overhead. Annotated previews visually reviewed: single subjects localized in images 2, 3, 4, 6; multi-animal frames have overlapping boxes, so box totals are not verified animal counts. No species model or labeled accuracy evaluation performed. ZIP recovered locally (918811 bytes), SHA256 1fbd14fa42ad071f267b893b70a2146ab694a14254b6d616ebd4bb190a877fcc; CRC, six records and previews checked. User images, raw predictions and previews retained locally under ignored evaluation_enonkishu/supplied_six and root ZIP; excluded from Git.
