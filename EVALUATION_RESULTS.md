# WildPulse pilot results

Trial 2 completed: 20 complete Snapshot Kruger sequences, 42 images, 15 camera locations. Ten sequences are labeled animal and ten empty. The animal group covers four species labels. See [EVALUATION.md](EVALUATION.md) for the protocol and [evaluation_manifest.json](evaluation_manifest.json) for the exact sample.

## Results against supplied labels

| Threshold | True positives | False positives | True negatives | False negatives | Recall | Specificity | Precision | Accuracy |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.2 | 10 | 5 | 5 | 0 | 100% | 50% | 66.7% | 75% |
| 0.3 | 10 | 3 | 7 | 0 | 100% | 70% | 76.9% | 85% |
| 0.5 | 10 | 2 | 8 | 0 | 100% | 80% | 83.3% | 90% |
| 0.8 | 9 | 2 | 8 | 1 | 90% | 80% | 81.8% | 85% |

A true positive means an animal-labeled sequence has at least one animal detection at the threshold. A false positive means an empty-labeled sequence has at least one animal detection. Every sequence includes all selected frames.

Threshold 0.5 had the highest accuracy among the four predefined thresholds on this pilot. This is an observation, not a production threshold recommendation. At 0.8, one spotted-hyena sequence was missed while two false alarms remained.

## Error review

Five empty-labeled sequences were flagged at threshold 0.2. The two remaining false alarms at 0.5 and 0.8 both came from camera 14 and boxed a bright, saturated foreground region at the lower left in nighttime frames. The physical cause is not established. Keep the supplied labels and predictions intact; inspect the full sequences before making any relabeling decision.

The other three flagged empty sequences have weaker boxes in vegetation or near the frame edge. This review used annotated resized previews and did not independently establish ground truth. Repeated cases from one camera also reduce the independence of these observations.

## Sequence scores

Maximum animal confidence across all frames. A zero means no animal prediction reached the inference floor of 0.2, not that the underlying model assigned an exact zero probability.

| Sequence | Dataset label | Maximum retained animal confidence |
| --- | --- | ---: |
| KRU_S1#8#1#229 | empty | 0.0000 |
| KRU_S1#14#1#432 | empty | 0.8852 |
| KRU_S1#44#1#27 | empty | 0.2002 |
| KRU_S1#8#1#322 | empty | 0.0000 |
| KRU_S1#3#1#390 | empty | 0.3169 |
| KRU_S1#27#1#10 | empty | 0.2030 |
| KRU_S1#2#1#57 | empty | 0.0000 |
| KRU_S1#14#1#125 | empty | 0.8148 |
| KRU_S1#47#1#69 | empty | 0.0000 |
| KRU_S1#22#1#117 | empty | 0.0000 |
| KRU_S1#43#1#16 | steenbok | 0.9528 |
| KRU_S1#5#1#21 | elephant | 0.9802 |
| KRU_S1#42#1#22 | hyenaspotted | 0.9724 |
| KRU_S1#44#1#32 | impala | 0.9838 |
| KRU_S1#27#1#41 | elephant | 0.9281 |
| KRU_S1#17#1#59 | hyenaspotted | 0.7454 |
| KRU_S1#7#1#141 | impala | 0.9689 |
| KRU_S1#34#1#30 | impala | 0.9599 |
| KRU_S1#7#1#112 | impala | 0.9661 |
| KRU_S1#49#1#33 | impala | 0.9766 |

## Verification and timing

All 20 selected sequences and 42 frames were present. Local scoring recomputed every reported metric from the saved predictions and matched the runtime report. Mean per-image inference API wall time was 14.50 seconds on CPU. This includes model-side image loading and API overhead; image downloads and the separate OpenCV readability check are outside that timer. It is not a throughput benchmark.

The local result bundle is 2,450,144 bytes, passed ZIP integrity checks, and matched the runtime SHA256:

```text
10c23bf32fb5378b8d386c745202a3d2066a268a5346a92e137daf385228baac
```

The archive, raw predictions, and review images remain local in ignored storage. The committed manifest is a small metadata subset derived from [Snapshot Kruger](https://lila.science/datasets/snapshot-kruger), provided under its stated Community Data License Agreement permissive terms.

## Limits and next step

With only ten positive and ten negative sequences, one additional mistake changes recall or specificity by ten percentage points. Balanced sampling does not represent natural prevalence; precision and accuracy here apply only to this pilot. Training overlap is unknown, so these results do not establish generalization to unseen training data or new camera locations.

Keep this pilot frozen. Before selecting a threshold, use a larger independent set with more night, small-animal, partially visible, and camera-obstruction cases; validate labels and split by camera or location.
