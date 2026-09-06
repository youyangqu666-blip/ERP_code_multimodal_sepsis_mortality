# ERP_code_multimodal_sepsis_mortality

Multimodal deep learning (LSTM + ClinicalBERT, cross-attention fusion) for post-24-hour
in-hospital mortality prediction in a MIMIC-III sepsis cohort. MSc Data Science Extended
Research Project.

This repository contains the code, notebooks, configuration and documentation needed to
reproduce the results reported in the dissertation. No patient data are included
(see *Data and external resources* below).

## Data and external resources

None of the following are included in this repository, obtain them from the official
sources before running the notebooks.

- **MIMIC-III v1.4** — the clinical database. Requires credentialed PhysioNet access:
  https://physionet.org/content/mimiciii/1.4/
  Place the required CSV tables in a single folder and point `DATA_DIR` (in `config.py`)
  at that folder.
- **itemid_to_variable_map.csv** — variable map used to select the physiological
  variables, from the mimic3-benchmarks project (Harutyunyan et al., 2019):
  https://github.com/YerevaNN/mimic3-benchmarks
  (`mimic3benchmark/resources/itemid_to_variable_map.csv`). Place it in `DATA_DIR`.
- **Angus sepsis definition SQL** — downloaded automatically in notebook 02 from the
  MIT-LCP mimic-code repository.
- **ClinicalBERT** (`emilyalsentzer/Bio_ClinicalBERT`) — downloaded automatically from
  Hugging Face when the text notebooks run.

MIMIC-III and its derived files are governed by the PhysioNet Credentialed Health Data
Use Agreement and must not be redistributed.

## Setup

Python 3 with Jupyter notebooks. Install dependencies with:

```
pip install -r requirements.txt
```

Set the path to your local data folder in `config.py` (variable `DATA_DIR`), or via the
`ERP_DATA_DIR` environment variable.

## How to run

Notebooks are numbered in run order and read/write intermediate files in `DATA_DIR`.
Run them top to bottom.

### Core pipeline (required to reproduce the reported results)

| # | Notebook | Purpose |
|---|---|---|
| 02 | Cohort_Construction_Angus | Build the Angus sepsis cohort |
| 03 | Clinical_Notes_Availability | Note availability analysis |
| 04 | ClinicalVariables_Extraction | Extract the physiological variables |
| 05 | Temporal_Alignment | Hourly-align signals to a 24-hour grid |
| 06 | Modelling_Cohort_Labels | Modelling cohort + post-24h mortality label |
| 07 | Clinical_Notes_Alignment | Note preprocessing + hourly alignment |
| 08 | Signal_LSTM_Baseline | Signals-only LSTM baseline |
| 09a | Finetune_ClinicalBERT | Fine-tune the text encoder |
| 09b | Frozen_MBERT_Encoding | Encode notes to hourly embeddings |
| 10 | CrossAttention_Fusion | Cross-attention fusion model (+ multi-seed) |
| 11 | Concat_Fusion_Ablation | Concatenation fusion ablation (+ multi-seed) |
| 13 | Bootstrap_CI_and_Forest_Plot | Bootstrap CIs, paired test, performance figures |

### Supporting material (not required to reproduce the main reported results)

| # | Notebook | Purpose |
|---|---|---|
| 01 | EDA_Sepsis_vs_AKI | Exploratory analysis and cohort EDA figures |
| 14 | SevenVar_Sensitivity | Seven-variable sensitivity analysis (Appendix B) |

## Key settings

- Cohort: Angus administrative sepsis definition; first ICU stay per patient; ≥24h ICU
  window; deaths within the first 24h excluded (label leakage). Final cohort: 10,068
  stays, 20.7% post-24h in-hospital mortality.
- Signals: 16 physiological variables + 16 observation masks, hourly over 24h;
  standardised on training-set statistics.
- Text: first-24h notes only; discharge summaries excluded; encoded with ClinicalBERT.
- Split: patient-level 70/15/15, stratified, random seed 42.
- Evaluation: AUROC, AUPRC, F1 (threshold 0.5); 2,000-sample bootstrap 95% CIs; paired
  bootstrap between fusion models; five-seed sensitivity analysis (seeds 42, 1, 2, 3, 4).

## Notebook outputs

Cells that would display row-level patient records (clinical note text, identifiers) have
had their outputs cleared, in line with the PhysioNet Data Use Agreement. The `figures/`
folder contains the figures reported in the dissertation.

## Licence

Code released under the MIT Licence (see `LICENSE`). MIMIC-III data are **not** covered by
this licence and must be obtained separately under the PhysioNet DUA.
