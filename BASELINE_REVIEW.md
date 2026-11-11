# WildPulse baseline review

## Verified artifact

The Colab result archive was recovered locally on November 10, 2026. Its SHA256 matches the value printed in the runtime:

```text
9a6941733d08effee20c5b87976edfdf6ae796ec7c6a09220b9af8621fa83180
```

Archive size: 6,878,656 bytes. ZIP integrity checks passed. The extracted baseline has six records and six annotated image files. The archive and images remain local and are excluded from Git.

## What needs review

| Images | Observation | Interpretation |
| --- | --- | --- |
| IMAG0029 and IMAG0030 | A large animal is clearly visible inside the predicted boxes; confidence is above 0.97. | Useful successful detection examples. No species label was produced. |
| IMAG0031 | Person 0.587 and animal 0.301 have identical coordinates at the extreme right edge. The preview shows a narrow, cropped portion of a subject leaving the frame. | Conflicting labels for the same region, not evidence of two subjects. A person is not visually established. Keep for manual review. |
| IMAG0042 | No boxes at threshold 0.2. | No detection is not proof that the image is empty. |
| IMAG0043 | Two low-confidence animal boxes overlap strongly in vegetation; their intersection over union is 0.6144. | Possible duplicate predictions or an obscured subject. Two animals are not established by these boxes. |
| IMAG0044 | One animal box at confidence 0.408 in vegetation. | An uncertain prediction requiring closer review against the original image. |

This was a visual inspection of annotated previews, not a ground-truth labeling exercise. Original, unannotated images and dataset labels should be used for an accuracy evaluation.

## Threshold comparison

The following table filters saved predictions using confidence greater than or equal to each threshold. It does not rerun the model, change its postprocessing, or recover predictions below the original 0.2 threshold.

| Confidence threshold | Animal boxes | Person boxes | Images with any box |
| ---: | ---: | ---: | ---: |
| 0.2 | 6 | 1 | 5 |
| 0.3 | 4 | 1 | 4 |
| 0.5 | 2 | 1 | 3 |
| 0.8 | 2 | 0 | 2 |

These are box counts, not unique-animal counts. Raising the threshold to 0.5 removes several animal predictions while retaining the conflicting person prediction. Confidence filtering alone does not resolve the class conflict.

Keep the 0.2 baseline unchanged for inspection. The next evaluation step is to obtain ground-truth labels for a larger, varied set of images and measure errors before selecting an operational threshold.
