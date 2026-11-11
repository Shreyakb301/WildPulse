# WildPulse Enonkishu results

## Run

All 30 complete Snapshot Enonkishu sequences and 64 images completed on CPU with sparrow-engine 0.1.32 and MDV6-yolov10-e. The sample contains 15 animal and 15 empty labels across 16 camera locations. The primary threshold **0.5** was published before inference in commit 59177bc. See [protocol](NEW_SITE_EVALUATION.md) and [manifest](enonkishu_manifest.json).

## Results against supplied labels

| Threshold | TP | FP | TN | FN | Recall | Specificity | Precision | Accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.2 secondary | 15 | 5 | 10 | 0 | 100% | 66.7% | 75.0% | 83.3% |
| 0.3 secondary | 15 | 4 | 11 | 0 | 100% | 73.3% | 78.9% | 86.7% |
| **0.5 primary** | **15** | **4** | **11** | **0** | **100%** | **73.3%** | **78.9%** | **86.7%** |
| 0.8 secondary | 14 | 1 | 14 | 1 | 93.3% | 93.3% | 93.3% | 93.3% |

The higher secondary threshold loses one animal sequence. No new operational threshold was selected. Mean recorded API wall time in the exported completed run was 8.896607 seconds/image; this includes API overhead and is not a controlled throughput comparison with the earlier runtime.

## Disagreement review

The four primary-threshold false positives are relative to supplied empty labels:

| Sequence | Maximum animal score | Visual observation in selected highest-score frame |
| --- | ---: | --- |
| ENO_S1#D06#1#1317 | 0.642 | Box covers a blurred foreground obstruction; animal presence unresolved. |
| ENO_S1#D02#1#90 | 0.902 | Strong overexposure; apparent animal legs/body in the boxed region. |
| ENO_S1#B02#1#259 | 0.696 | Large blurred foreground region and saturated light; unresolved. |
| ENO_S1#B06#2#230 | 0.725 | Small apparent antelope in the box despite the empty label. |

These observations suggest possible label disagreement in at least two frames; they are not authoritative relabeling. Labels and metrics remain unchanged. Full-sequence expert review is needed before calling these verified model errors.

## Verification and artifacts

The JSON export SHA256 matched Colab: `2c84003b5c47617e98611c7e4248d75e2e63268773a35e8dfdf14ef029e6e2a5`. Locally verified all sequence metadata, exact ordered frame membership, all 64 frame records, recomputed maxima and all metrics.

Local bundle `WildPulse_enonkishu_results.zip` contains manifest, predictions, four review frames and a contact sheet. Size 1,327,770 bytes; SHA256 `b929038a88dab0101f94d04a53ef78851882370bd471184c982235002aa4e1a4`. ZIP CRC and prediction equality passed. Images and bundles remain outside Git.

## Limits and execution record

This balanced, small sample does not estimate natural-prevalence precision, species accuracy or box localization accuracy. Cameras repeat across classes. Enonkishu is separate from the Kruger pilot, but model training overlap is unknown. Domestic animals count as animals.

Colab disconnected and diagnostics on the replacement session initially found no temporary files. Preparation was restored. A checkpoint wrapper later failed with recursion after being executed again; that failed attempt is excluded. On reconnect the notebook showed a complete earlier evaluation and a full final file was present. The exported completed file is the basis of this report; saved-output history does not establish exactly when every backend execution occurred. No predictions from the failed attempt were merged into the final report.
