# ERP_code_multimodal_sepsis_mortality 
### Technical Appendix - MSc Data Science Extended Research Project

Multimodal deep learning (LSTM + ClinicalBERT with cross-attention fusion) for post-24-hour in-hospital mortality prediction in a MIMIC-III sepsis cohort. MSc Data Science Extended Research Project.

This repository contains the code, notebooks, configuration files and documentation required to reproduce the analyses reported in the report.

No MIMIC-III patient-level data are included in this repository. Restricted source data must be obtained separately from PhysioNet by an authorised user.

## Data and external resources

### MIMIC-III v1.4

This project uses the **MIMIC-III Clinical Database v1.4**.

The database can be obtained from the official PhysioNet MIMIC-III page:

https://physionet.org/content/mimiciii/1.4/

Access to MIMIC-III is restricted. Reproducers must obtain their own authorised PhysioNet access and satisfy the applicable credentialing, training and Data Use Agreement requirements.

After obtaining access, download the required MIMIC-III CSV/CSV.GZ tables and place them in a single local data directory.

The notebooks use the following source tables:

- `ADMISSIONS.csv.gz`
- `PATIENTS.csv.gz`
- `ICUSTAYS.csv.gz`
- `PROCEDURES_ICD.csv.gz`
- `DIAGNOSES_ICD.csv`
- `D_ICD_DIAGNOSES.csv`
- `NOTEEVENTS.csv.gz`
- `CHARTEVENTS.csv.gz`
- `LABEVENTS.csv.gz`
- `D_ITEMS.csv.gz`

If a downloaded table is compressed but the notebook expects the uncompressed `.csv` version, decompress the file or update the filename consistently.

### itemid_to_variable_map.csv

Notebook 04 requires:

`itemid_to_variable_map.csv`

This mapping file is used to map MIMIC ITEMIDs to the benchmark physiological variables.

It is available from the `mimic3-benchmarks` project:

https://github.com/YerevaNN/mimic3-benchmarks

Path within that repository:

`mimic3benchmark/resources/itemid_to_variable_map.csv`

Download this file separately and place it in the same `DATA_DIR` as the MIMIC-III source tables.

**Note**: the notebook filenames use "17" after the mimic3-benchmarks 17-variable set that the extraction starts from. Capillary refill rate is excluded (effectively unrecorded in this cohort), leaving the 16 variables used for modelling and reported in the study (see Table 4.3 in the report).

### Angus sepsis definition

Notebook 02 uses the Angus administrative sepsis definition.

The reference SQL file is downloaded automatically from the MIT-LCP `mimic-code` repository when notebook 02 runs.

### ClinicalBERT

The text models use:

`emilyalsentzer/Bio_ClinicalBERT`

The pretrained tokenizer and model are downloaded automatically through the Hugging Face `transformers` library when notebooks 09a/09b are run.

Internet access is therefore required on first use unless the model is already available in the local Hugging Face cache.

## Setup

The notebooks were run using Python 3.13.x. Local preprocessing was tested with Python **3.13.5**, while the Colab environment used for GPU-based modelling reported Python 3.13.15.

They can be run in any Python environment that supports `.ipynb` notebooks, for example:

- VS Code
- JupyterLab / Jupyter Notebook
- Google Colab

A GPU is strongly recommended for the deep-learning notebooks, particularly notebooks 09a, 09b, 10, 11 and 13.

Install the required Python packages with:

```bash
pip install -r requirements.txt
```

The main third-party packages used are:

- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn`
- `torch`
- `transformers`

Exact package versions used for reproduction are specified in `requirements.txt`.

## Data directory configuration

All notebooks use a shared `DATA_DIR`.

The supplied `config.py` contains:

```python
import os

DATA_DIR = os.environ.get("ERP_DATA_DIR", "./data")
```

There are two ways to configure the data location.

### Option 1: use the default `data/` folder

Create a folder named:

```text
data/
```

and place the downloaded MIMIC-III source files in that directory.

Download `itemid_to_variable_map.csv` separately from the source listed above and place it in the same `DATA_DIR`.

### Option 2: use another local authorised data directory

Set the environment variable:

```text
ERP_DATA_DIR
```

to the location of your data.

For example on Windows:

```powershell
$env:ERP_DATA_DIR="E:\path\to\mimic_data"
```

On macOS/Linux:

```bash
export ERP_DATA_DIR="/path/to/mimic_data"
```

The notebooks then construct file paths through:

```python
data_path("filename")
```

This allows the same code to run without hard-coded user-specific paths.

## How to run

Before running anything, make sure `config.py` (in `notebooks/`) points to your data (see *Data directory configuration* above).

The notebooks read source or intermediate files from `DATA_DIR` and write generated intermediate files back to the same directory.

The recommended execution order is:

### Core pipeline

| # | Notebook | Purpose |
|---|---|---|
| 02 | `Cohort_Construction_Angus` | Build the Angus sepsis cohort |
| 03 | `Clinical_Notes_Availability` | Analyse availability of clinical notes |
| 04 | `ClinicalVariables17_Extraction` | Extract physiological variables from CHARTEVENTS/LABEVENTS |
| 05 | `Temporal_Alignment_17vars` | Align physiological measurements to the first-24-hour hourly grid |
| 06 | `Modelling_Cohort_Labels` | Construct the final modelling cohort and mortality label |
| 07 | `Clinical_Notes_Alignment` | Clean and align clinical notes to hourly bins |
| 08 | `Signal_LSTM_Baseline` | Train and evaluate the signals-only LSTM |
| 09a | `Finetune_ClinicalBERT` | Fine-tune ClinicalBERT and generate text-only predictions |
| 09b | `Frozen_MBERT_Encoding` | Encode hourly clinical notes using the fine-tuned encoder |
| 10 | `CrossAttention_Fusion` | Train and evaluate the cross-attention fusion model |
| 11 | `Concat_Fusion_Ablation` | Train and evaluate the concatenation fusion model |
| 12 | `Bootstrap_CI_and_Forest_Plot` | Compute confidence intervals, paired tests and performance figures |

### Supporting analysis

| # | Notebook | Purpose |
|---|---|---|
| 01 | `EDA_Sepsis_vs_AKI` | Exploratory/descriptive analysis and EDA figures |
| 13 | `SevenVar_Sensitivity` | Seven-variable sensitivity analysis |

Notebook 01 is numbered first for presentation purposes but depends on files generated later in the pipeline. It should therefore be run after the required intermediate files have been generated.

Notebook 13 is a supporting sensitivity analysis and is not required to reproduce the main reported model results.

## Main generated files

### Notebook 02

Produces:

- `final_cohort_angus.csv`

Used by later cohort, signal and note-processing notebooks.

### Notebook 04

Produces:

- `filtered_chartevents_17vars.csv`
- `filtered_labevents_17vars.csv`

These are generated from the original MIMIC-III event tables and are not included in the repository.

### Notebook 05

Produces:

- `hourly_vitals_partial.csv`
- `hourly_vitals_raw.csv`
- `hourly_vitals.csv`

`hourly_vitals.csv` is the final aligned physiological time-series dataset used by the modelling notebooks.

### Notebook 06

Produces:

- `modelling_cohort_sepsis_mortality.csv`

This contains the final modelling cohort and post-24-hour in-hospital mortality outcome.

### Notebook 07

Produces:

- `hourly_notes_24h.csv`

This contains first-24-hour clinical notes aligned to hourly bins.

### Notebook 08

Produces:

- `preds_signal.npz`

### Notebook 09a

Produces:

- `mbert_ckpt/last.pt`
- `mbert_ckpt/mbert_best.pt`
- `preds_text.npz`

For a clean reproduction, start with an empty `mbert_ckpt` directory. If `last.pt` already exists, training resumes automatically from that checkpoint.

### Notebook 09b

Produces:

- `text_hourly_cls_mbert.npz`

### Notebook 10

Produces:

- `preds_crossattn.npz`
- the reported attention visualisation

### Notebook 11

Produces:

- `preds_concat.npz`

### Notebook 12

Uses the saved prediction files from notebooks 08, 09a, 10 and 11 to compute:

- AUROC
- AUPRC
- F1
- 95% bootstrap confidence intervals
- paired bootstrap differences between fusion models

It also produces the reported performance figures, including:

- ROC curve
- precision-recall curve
- metric comparison bar chart
- calibration plot
- AUROC forest plot

## Key analysis settings

- Cohort definition: Angus administrative sepsis definition.
- First ICU stay per patient.
- At least 24 hours of ICU observation.
- Patients who died within the first 24 hours were excluded from the prediction cohort.
- Final modelling cohort: **10,068 ICU stays**.
- Post-24-hour in-hospital mortality: **20.7%**.
- Physiological signals are aligned hourly over the first 24 hours.
- Clinical text is restricted to the first 24 hours; discharge summaries are excluded.
- Patient-level train/validation/test splitting uses a fixed random seed of **42**.
- Primary evaluation metrics: AUROC, AUPRC and F1.
- F1 threshold: **0.5**.
- Bootstrap confidence intervals: **2,000 bootstrap samples**.
- Multi-seed sensitivity analysis uses seeds **42, 1, 2, 3 and 4**.

## Outputs and patient-level information

Outputs containing row-level MIMIC-III patient information, clinical-note text or identifiers have been removed from the public notebooks.

The repository contains only code, non-sensitive analytical outputs and report figures appropriate for public sharing.

The `figures/` directory contains figures used in the dissertation.

Restricted MIMIC-III source files and patient-level generated datasets are not redistributed.

## Repository structure

```text
ERP_code_multimodal_sepsis_mortality/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── notebooks/
│   ├── config.py
│   ├── 01_EDA_Sepsis_vs_AKI.ipynb
│   ├── 02_Cohort_Construction_Angus.ipynb
│   ├── ...
│   └── 13_SevenVar_Sensitivity.ipynb
│
└── figures/
    ├── fig_outcome_dist.png
    ├── fig_vitals_by_outcome.png
    ├── fig_missingness.png
    ├── ...
    └── forest_auroc.png
```

## Licence

Code is released under the MIT Licence where applicable.

MIMIC-III data are **not** covered by this licence and must be obtained independently under the applicable PhysioNet Data Use Agreement.

