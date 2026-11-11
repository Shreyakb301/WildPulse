# WildPulse new site evaluation

## Frozen protocol

Evaluate 30 complete sequences from [Snapshot Enonkishu](https://lila.science/datasets/snapshot-enonkishu), Kenya: 15 labeled animal and 15 labeled empty. Enonkishu is separate from the Snapshot Kruger site used for the earlier pilot. Dataset names and image paths are disjoint; absence from the model's training data has not been established.

The primary confidence threshold is **0.5**, fixed before inference. Thresholds 0.2, 0.3, and 0.8 are secondary sensitivity checks, not alternatives from which to choose a winning threshold after seeing results. Keep model `MDV6-yolov10-e`, engine sparrow-engine 0.1.32, CPU, and inference floor 0.2.

Score animal presence per complete sequence using the maximum animal score across frames. Exclude human-labeled, corrupt, incomplete, and mixed empty/animal sequences. All other categories in the inspected metadata are animal categories; domestic animals count as animals for this task.

## Sampling

Pin metadata SHA256 `380dbab5598e1468f74c8dd19e59c0424d61f6f26532a85a7a0a757b8c87de21` and seed `wildpulse-enonkishu-transfer-2026-11-11`. Rank sequences by a deterministic hash, then take one sequence per camera in each class before repeating cameras. Select 15 per class before inference; do not replace difficult examples after seeing predictions.

The dataset has 16 camera locations. This is a balanced sample, not its natural class prevalence. Repeated cameras across the positive and negative groups remain a source of dependence; this is not a 30-independent-camera test.

## Run

```bash
python evaluate_sequences.py prepare --config enonkishu_config.json --root /content/WildPulse/evaluation_enonkishu
python evaluate_sequences.py evaluate --root /content/WildPulse/evaluation_enonkishu
```

The original Kruger pilot remains unchanged. The configuration is in [enonkishu_config.json](enonkishu_config.json). Images and raw runtime artifacts are excluded from Git.

## Reporting

Verify full sequence and frame membership, recompute metrics from exported predictions, and report TP, FP, TN, FN, recall, specificity, precision, and accuracy at the locked primary threshold. Review disagreement examples without silently changing labels. Report the small-sample and unknown training-overlap limitations. The run is complete; see [NEW_SITE_RESULTS.md](NEW_SITE_RESULTS.md) for verified results and execution limitations.
