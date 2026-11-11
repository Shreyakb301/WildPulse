# WildPulse

WildPulse is a camera-trap wildlife detection project. It runs MegaDetector on a small set of images and saves the boxes, confidence scores, annotated previews, and time taken for each image.

The first working baseline uses SPARROW-Engine on a Google Colab CPU runtime. Six images have been processed successfully. This is the starting point for reviewing detections and measuring performance on a larger dataset.

## What it does

- **Processes each image independently.** Every image gets its own detection record and wall-clock timing.
- **Shows what the model found.** Annotated previews put boxes around predicted animals, people, and vehicles.
- **Saves usable results.** Outputs include a detailed JSON summary, MegaDetector-format JSON, and a CSV export.
- **Separates startup from repeat calls.** The script records the model download or cache check, the first detection call, and the following six timed calls.
- **Keeps an engineering record.** Setup failures, fixes, observed results, and unresolved issues are recorded in the project logs.

## Stack

- Python 3.11 or newer; the observed Colab runtime used Python 3.13.18
- [SPARROW-Engine](https://github.com/microsoft/SPARROW-Engine), pinned to version 0.1.32
- MegaDetector V6, model `MDV6-yolov10-e`
- OpenCV for annotated image output
- Google Colab for the initial CPU run

## Setup

### Run in Google Colab

Place the project files under `/content/WildPulse` and upload the six JPEG images into `/content/WildPulse/sample_images`.

```python
%pip install -r /content/WildPulse/requirements-baseline.txt
```

Then run:

```python
!python /content/WildPulse/run_baseline_sparrow.py
```

The script expects exactly six files with the `.jpeg` extension. The initial experiment used Snapshot Kruger images with suffixes `IMAG0029`, `IMAG0030`, `IMAG0031`, `IMAG0042`, `IMAG0043`, and `IMAG0044`.

The first run needs an internet connection to download the model. Generated files are written to `/content/WildPulse/baseline_output`. Download them before resetting the Colab runtime; session storage is temporary.

### Run locally

Create a Python environment, install the dependencies, and put the six images in `sample_images` inside this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-baseline.txt
python run_baseline_sparrow.py --project-dir .
```

Image files and model weights are not included in this repository. The standalone script has been syntax-checked locally; the equivalent detection and export steps were executed in Colab.

## Baseline results

Observed on November 10, 2026, using CPU inference and a confidence threshold of `0.2`:

| Image | Predictions | Wall time |
| --- | --- | ---: |
| IMAG0029 | animal 0.979 | 17.181 s |
| IMAG0030 | animal 0.976 | 14.572 s |
| IMAG0031 | person 0.587; animal 0.301 | 15.705 s |
| IMAG0042 | no detections | 15.991 s |
| IMAG0043 | animal 0.299; animal 0.276 | 14.688 s |
| IMAG0044 | animal 0.408 | 14.933 s |

Mean warmed wall time was **15.51 seconds per image**. Model download took 48.23 seconds, and the first detection call took 15.20 seconds. The six-image run followed that first call and additional debugging calls; timings include image decoding and Python API overhead.

These labels are predictions. The person prediction and the lower-confidence animal boxes need review. Six images do not establish detection accuracy, throughput, or performance on other hardware. MegaDetector detects broad categories; it does not identify species.

## About the images

The initial images came from [Snapshot Kruger on LILA BC](https://lila.science/datasets/snapshot-kruger). Refer to the dataset page for source information, attribution, and usage terms before using or redistributing images. Model usage terms are separate; the downloaded model package identifies its license as AGPL-3.0.

## Engineering record

PytorchWildlife 1.3.1 installed but failed to import because of a Hugging Face dependency conflict. The working baseline uses SPARROW-Engine. A Pillow JPEG-writing error was resolved by saving previews through OpenCV.

The notebook saved JSON, CSV, six previews, a contact sheet, and a result ZIP. The ZIP has now been recovered locally, checked against Colab's SHA256, and verified for archive integrity. The generated images and archive are not included here.

See [BASELINE_REVIEW.md](BASELINE_REVIEW.md) for the visual review, conflicting labels, overlapping boxes, and a comparison of confidence thresholds. The original 0.2 baseline is preserved.

See [PROJECT_LOG.md](PROJECT_LOG.md) for the work record and [PROJECT_NOTES.md](PROJECT_NOTES.md) for current decisions and next steps.
