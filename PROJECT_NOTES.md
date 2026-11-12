# WildPulse project notes

## Working preferences

- Push completed, verified milestones as work progresses.
- Use three or four words in commit messages, letters and spaces only.
- Follow the README voice and sections of LoadCheck, RepoLens and DepotField.
- Use Trial headings rather than dates in project documentation.
- Keep PROJECT_LOG.md local and excluded from GitHub. Previous commits are not rewritten.
- Publish selected annotated README previews as requested. Keep original uploads, model weights, environments and runtime bundles outside Git.

## Trial 1 — Working baseline

PytorchWildlife 1.3.1 installed but could not import because of a Hugging Face dependency conflict. SPARROW-Engine 0.1.32 with MDV6-yolov10-e completed six images on CPU at confidence 0.2. OpenCV preview writing resolved the Pillow JPEG failure. Mean warmed API wall time was 15.511592 seconds per image. The recovered ZIP passed checksum and integrity checks.

Conflicting person/animal boxes and overlapping animal boxes require review. Predictions are broad categories, not species identities or verified counts. See BASELINE_REVIEW.md.

## Trial 2 — Kruger labeled pilot

Processed all 42 images from 20 complete sequences, balanced between animal and empty labels. At 0.5: TP10 FP2 TN8 FN0 against supplied sequence labels. All frame membership and metrics were checked locally. See EVALUATION_RESULTS.md. The sample is exploratory and does not establish a production threshold.

## Trial 3 — Enonkishu transfer evaluation

Processed 64 images from 30 complete sequences across 16 camera locations. Confidence 0.5 was fixed before inference: TP15 FP4 TN11 FN0. All membership, maximum scores and metrics were recomputed from exported predictions. ZIP checksum and integrity passed. The recovered completed file is the reported source; an interrupted runtime and a failed recursive checkpoint helper are documented in NEW_SITE_RESULTS.md.

Full review covered six frames across four label disagreements: two apparent animals despite empty labels, one likely foreground-obstruction false alarm and one unresolved blur/glare case. Original labels and metrics remain unchanged. Model training overlap is unknown.

## Trial 4 — Image review workflow

WildPulse_Image_Review.ipynb supports upload, confidence selection, annotated previews and ZIP export. Fresh Colab setup and real inference on one public example succeeded. The direct download link was recovered and verified locally. File-picker automation and the standard browser download remain unconfirmed.

The notebook includes a checksum-pinned public example and a fixed runner version. Each rerun gets a separate result folder; cancelled uploads and failed runs clear the previous download target. Four automated notebook-state checks passed. Notebook code parses as Python 3.11.

## Trial 5 — Supplied image test

All six supplied PNG images completed on Colab CPU at confidence 0.5. Original-byte checksums matched after transfer. Animal-box counts in order: 7, 1, 1, 1, 3, 1. Maximum scores: 0.9444, 0.9554, 0.9408, 0.9508, 0.9142, 0.9483. No person or vehicle predictions were retained. Mean API wall time was 12.593204 seconds per image, including first-call overhead.

Six previews and result records were verified, and the ZIP passed SHA256 and CRC checks. Group photos have overlapping boxes, so box counts are not verified animal counts. Selected annotated previews are displayed in README as requested. Original uploads and complete outputs remain local.

## Current limits

WildPulse performs image detection. It does not track identities between frames, identify species, or establish accuracy from these six unlabeled examples. Dataset labels may contain disagreements. File-picker upload still needs manual verification.

## Trial 6 — Human review exports

Added a self-contained review.html to generated result bundles. Each input image, including unreadable entries, has an assessment (not reviewed, correct, incorrect or uncertain) and notes. Exported WildPulse_review.json links to exact results.json bytes by SHA256. Original predictions remain unchanged; review decisions are not automatic ground-truth relabeling. Decisions must be downloaded before closing/reloading; no automatic persistence is claimed.

Verified the real six-image saved predictions render in a local browser without rerunning inference. Selected uncertain and correct on two images, entered a test note and observed progress change to 2 of 6. Browser download saved a review JSON; exact decisions, note, six rows and prediction checksum verified locally. Six automated checks passed, covering script-safe filename handling, result immutability, empty-detection ZIP inclusion and notebook state transitions. Updated notebook runner pin and Python 3.11 syntax checked. Existing Colab file-picker automation limitation remains. Images, generated review page and test export stay ignored locally; PROJECT_LOG.md remains local.
