# WildPulse project notes

## User preferences

- Push completed and verified milestones to GitHub as work progresses.
- Commit messages must be three or four words, letters and spaces only, with no special characters. Example: `Add wildlife baseline`.
- Match the README style and relevant sections of the user's existing GitHub projects, including LoadCheck, RepoLens, and DepotField.
- User authorized a new public WildPulse repository on 2026-11-10.

## Current project state

- Notebook: `Wildlife.ipynb` in Google Colab; the private notebook link is not published here.
- Runtime project root: `/content/WildPulse`; starter script: `run_baseline.py`.
- Goal: independent wildlife detection on six uploaded camera-trap images, with real timing and saved detection outputs.
- PytorchWildlife 1.3.1 is installed but cannot import in the current runtime. Its warning states it is the final unmaintained release and names SPARROW-Engine as replacement.
- Verified working path: sparrow-engine 0.1.32, CPU, MegaDetector `MDV6-yolov10-e`, confidence threshold 0.2.
- Official reference: https://github.com/microsoft/SPARROW-Engine
- MegaDetector finds animals, people, and vehicles; it does not establish species identity. Six images cannot establish accuracy or deployment performance.
- Separate model download/load, first inference, and warmed per-image timings when reporting results.
- `/content` files are runtime storage and can disappear when the Colab runtime is reset. Save a downloadable result bundle before completion if feasible.
- Baseline succeeded on all six images. Outputs: `/content/WildPulse/baseline_output`; bundle: `/content/WildPulse_baseline_results.zip` (6,878,656 bytes).
- Mean warmed CPU wall time was 15.511592 seconds/image. IMAG0031 has a person prediction (0.587) that requires visual review; do not treat model labels as verified facts.
- Runtime logs were written and included in the bundle. Local logs are more detailed and separate.
- Colab's output JavaScript loading issue has blocked preview display and bundle download so far; no local result archive has been claimed.
- Reload restored previews; both rows were visually inspected. Download is still unconfirmed (reCAPTCHA service connection issue), and the subsequent media export timed out. Notebook results were saved and persisted across reload.

## Latest verified state

- Enonkishu first run interrupted after 15 visibly completed sequences; replacement runtime lost temporary files. Same-config rerun underway with notebook-visible checkpoint links. Superseded by completed export below.

- Enonkishu new-site test prepared: 30 sequences (15 animal, 15 empty), 64 images, 16 camera locations. Primary threshold 0.5 fixed before inference. See NEW_SITE_EVALUATION.md. Completed export verified: TP15 FP4 TN11 FN0 at primary 0.5. See NEW_SITE_RESULTS.md; model training overlap remains unknown.

- Additional six-frame visual set: `evaluation/more_examples/another_example_set.jpg`; individual panels `example_1.jpg` through `example_6.jpg`. Uses existing pilot predictions, not a fresh benchmark.

- Labeled pilot completed: all 20 sequences and 42 images scored. See EVALUATION_RESULTS.md and evaluation_manifest.json. At 0.2, TP=10 FP=5 TN=5 FN=0; at 0.5, TP=10 FP=2 TN=8 FN=0. Metrics are relative to supplied labels on this balanced pilot.
- Local evaluation archive checksum verified: `10c23bf32fb5378b8d386c745202a3d2066a268a5346a92e137daf385228baac`. All metrics recomputed successfully.
- Next validation should use a larger independent sample split by camera/location, with night, small-animal, partial-visibility, and obstruction cases. Do not choose an operational threshold from the pilot.

- Pilot setup used 20 complete Snapshot Kruger sequences (10 animal, 10 empty), 42 images. See EVALUATION.md and evaluate_sequences.py. Score presence per sequence, not per frame.

- Result recovery is now complete. Local `WildPulse_baseline_results.zip` matches Colab's SHA256 and passes ZIP CRC checks. Extracted files are in ignored `baseline_output/`.
- SHA256: `9a6941733d08effee20c5b87976edfdf6ae796ec7c6a09220b9af8621fa83180`.
- BASELINE_REVIEW.md records visual review and saved-prediction threshold filtering. Preserve the 0.2 baseline; an operational threshold has not been selected.
- The person and animal predictions on IMAG0031 use identical boxes at the frame edge. Person presence is not visually established. IMAG0043 contains overlapping low-confidence boxes, not two verified animals.
- Next: obtain ground-truth labels for a larger, varied image set before calculating accuracy or choosing a production threshold.

- Enonkishu completed file recovered and validated locally. Four dataset-label disagreements reviewed; apparent animals in two empty-labeled frames. Preserve supplied labels until expert sequence review. Checkpoint wrapper recursion failure excluded; do not rerun that helper unchanged.

2026-11-11: Reviewed all six original frames in the four Enonkishu primary-threshold disagreements. Two likely label disagreements (D02 90, B06 230), one likely foreground-obstruction false alarm (D06 1317, three frames), and one unresolved blur/glare case (B02 259). Observational review only; original labels and metrics unchanged. Images retained locally outside Git.

2026-11-11: Added run_images.py and WildPulse_Image_Review.ipynb for JPEG/PNG upload, preview and ZIP download. Unique output folders prevent stale exports; unreadable files are recorded, unexpected inference errors stop execution. Isolated simulated-detector checks passed for two valid images, one unreadable image, colliding stems, ZIP contents/integrity and output reuse rejection. Notebook code syntax checked for Python 3.11. New notebook live Colab upload/download verification remains pending; no new real inference claimed.

2026-11-11: Opened the published image-review notebook in a fresh Colab CPU session. Setup completed. File chooser automation timed out; native Codex app access was unavailable. Cancelled upload (zero files) and loaded public ENO_S1_B06_R2_IMAG0434.JPG by URL in a clearly marked temporary verification cell. Real run_images workflow processed one image with one animal detection and generated preview, JSON, CSV and MegaDetector JSON. Standard files.download produced no confirmed browser download event. Added and verified direct data-link fallback up to 20 MB. Recovered local WildPulse_workflow_smoke.zip (254717 bytes), SHA256 3a7feb22dbc29e2eed8afa72140c0e32076fbd946ae8eccb375254d7fe2ec502, matching Colab; ZIP CRC and JSON result counts passed. Full file-picker upload remains unverified. Notebook test changes were not saved through the GitHub UI; repository notebook receives only the download fallback.

2026-11-11: Continued notebook usability work. Added a public Enonkishu example option with SHA256 verification, using the same frame previously tested with real inference. Pinned runner download to commit 0d33fd1e4ee26785a45f91eebc61a12771c230f9. Each detection rerun uses a fresh output folder; cancelled/invalid uploads and failed detection runs invalidate the old downloadable result. Added four automated notebook-state tests; all passed. Notebook cells parse as Python 3.11. File-picker and standard download confirmation remain outstanding; no new real inference or complete upload test claimed in this change.

2026-11-11: Tested six user-supplied PNG images through the unchanged run_images workflow in Colab CPU, sparrow-engine 0.1.32, MDV6-yolov10-e, threshold 0.5. Original PNG bytes transferred with matching SHA256 checksums; all six decoded and completed. Animal-box counts in supplied order: 7, 1, 1, 1, 3, 1 (14 boxes); no person/vehicle predictions at this threshold. Maximum scores: 0.9444, 0.9554, 0.9408, 0.9508, 0.9142, 0.9483. Mean API wall time 12.593204 seconds/image, including first-call overhead. Annotated previews visually reviewed: single subjects localized in images 2, 3, 4, 6; multi-animal frames have overlapping boxes, so box totals are not verified animal counts. No species model or labeled accuracy evaluation performed. ZIP recovered locally (918811 bytes), SHA256 1fbd14fa42ad071f267b893b70a2146ab694a14254b6d616ebd4bb190a877fcc; CRC, six records and previews checked. User images, raw predictions and previews retained locally under ignored evaluation_enonkishu/supplied_six and root ZIP; excluded from Git.
