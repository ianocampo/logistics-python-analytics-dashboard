# Reproducibility verification — Logistics, Delivery & Returns Analytics

**Status:** PASS — November 7, 2026 (UTC)  
**Execution:** GitHub Actions Ubuntu-hosted clean checkout, Python 3.11.18  
**Primary notebook:** [Logistics_Analysis_Documented.ipynb](../Notebook/Logistics_Analysis_Documented.ipynb)  
**Successful verification run:** [GitHub Actions run 42376035355](https://github.com/ianocampo/logistics-python-analytics-dashboard/actions/runs/42376035355)  
**Repeatable verification:** [Notebook reproducibility workflow](../.github/workflows/reproducibility.yml)

## What was tested

| Test | Result | Evidence |
| :--- | :---: | :--- |
| Complete notebook execution | **PASS** | 108 code cells processed; no execution errors |
| Baseline analysis artifacts available | **PASS** | 14 CSV exports inspected before replay |
| Regenerated CSV consistency | **PASS** | All 14 before/after CSV exports matched semantically using pandas DataFrame comparisons |
| Original source integrity | **PASS** | SHA-256 hashes unchanged across all seven `Data/Raw/*.csv` files |
| Matplotlib PNG chart generation | **PASS** | Five valid regenerated chart files and five displayed notebook PNG outputs |
| Step 109 QA validation register | **PASS** | 85 of 85 checks marked PASS |
| Selected executive KPIs | **PASS** | 15,000 orders, 15,000 shipments, 11,680 Delivered, 1,200 return-request orders, 11,122 baseline durations, 5,667 screened durations |
| Clean checkout runtime | **PASS** | Notebook executed on GitHub-hosted Python 3.11.18 rather than the author's local computer |

## Interpretation

This test demonstrates that the committed notebook can execute in a clean GitHub-hosted environment and regenerate the expected analytical artifacts. It validates **functional reproducibility for the tested environment**, not production deployment readiness, data correctness beyond the documented checks, identical graphic file bytes across package versions, or a test of the owner's macOS/Python 3.14 configuration.

The underlying datasets are **synthetic demonstration data**. Recorded delivery status is not proof of on-time SLA performance; an order-level return request is not a confirmed completed or item-specific return. No realized savings or implemented operational improvements are claimed.

## How to rerun

Use the repository [reproducibility workflow](../.github/workflows/reproducibility.yml) from GitHub Actions (**Run workflow**), or create a fresh clone and run the documented notebook from the repository root after installing [requirements-analysis.txt](../requirements-analysis.txt).

The audit runs in a fresh checked-out working directory, verifies source-data hashes, compares analytic CSVs by content, and does not commit generated outputs into `main`.
