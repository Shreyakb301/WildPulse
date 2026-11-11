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
