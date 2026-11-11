# WildPulse sequence evaluation

## What this measures

This pilot tests whether MegaDetector finds an animal anywhere in a complete camera-trap sequence. It does not measure species classification, animal counts, or bounding-box localization accuracy.

[Snapshot Kruger](https://lila.science/datasets/snapshot-kruger) provides labels that are reliable at sequence level. An individual image can inherit an animal label even when the animal has already left that frame. Scoring each image against those labels would give misleading results.

## Sample

- Snapshot Kruger Season 1 metadata, SHA256 `3a90de11592822817c61f384df4732b3e9f17903593ed6b48ef15d1f6a5f1f9a`.
- Twenty complete sequences: ten labeled animal and ten labeled empty, totaling 42 images.
- Deterministic hash ordering with seed `wildpulse-pilot-2026-11-10` before inference.
- Human-labeled, corrupt, incomplete, mixed empty/animal, and original six-example sequences excluded.
- Downloaded only selected images from the official public cloud folder. Images remain outside Git.

The metadata contains 10,604 image records, including categories whose images are not publicly released; this differs from the public image count described by the dataset page. Human-labeled sequences are excluded before sampling.

## Method

Run `MDV6-yolov10-e` through sparrow-engine 0.1.32 on CPU, with inference threshold 0.2. For each sequence, take the maximum animal confidence across all its frames. A sequence is predicted positive when this score is at least the evaluation threshold. Person and vehicle detections do not count as animal detections.

Compare fixed thresholds 0.2, 0.3, 0.5, and 0.8. Report true positives, false positives, true negatives, false negatives, recall, specificity, precision, and accuracy. Do not select a production threshold from this pilot.

An unreadable or missing frame stops evaluation rather than silently scoring an incomplete sequence. Per-sequence progress is saved, and the full report is written only after every sequence completes.

## Run

Install `requirements-baseline.txt` first, then:

```bash
python evaluate_sequences.py prepare --root /content/WildPulse/evaluation
python evaluate_sequences.py evaluate --root /content/WildPulse/evaluation
```

For local execution, pass a local directory such as `--root ./evaluation`. The preparation stage downloads the pinned metadata and selected images. Outputs include `manifest.json`, `progress.json`, and, upon successful completion, `evaluation_results.json`.

## Limits

This is a small exploratory sample with deliberately balanced classes, not the dataset's natural prevalence. Precision and accuracy apply to this sample only. Its relationship to the model's training data has not been established, so it is not a known training-disjoint benchmark. The sample covers four animal labels: steenbok, elephant, spotted hyena, and impala, with empty as the negative class; it does not cover all species, seasons, or conditions.

The full run completed on 20 sequences and 42 images. See [EVALUATION_RESULTS.md](EVALUATION_RESULTS.md) for verified metrics, error review, and limitations. The exact sample is recorded in [evaluation_manifest.json](evaluation_manifest.json).
