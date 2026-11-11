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

- Enonkishu new-site test prepared: 30 sequences (15 animal, 15 empty), 64 images, 16 camera locations. Primary threshold 0.5 fixed before inference. See NEW_SITE_EVALUATION.md. Results pending; model training overlap remains unknown.

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
