# Logistics, Delivery & Returns Intelligence

**Python analytics case study | From shipment records to better operational decisions**

An end-to-end analytics project using seven linked synthetic datasets, a documented Python cleaning and validation workflow, five original charts, and a six-page interactive Streamlit dashboard.

> **Business question:** How well are we delivering, and what drives recorded return requests?
>
> **What this work demonstrates:** Turning imperfect operational records into measurable findings, transparent limitations, and practical management recommendations—without claiming unverified results.

**[Explore the Live Dashboard](https://ianocampo-logistics-analytics-python-001.streamlit.app)** · **[Read the One-Page Insights](Docs/One_Page_Insights_Summary.pdf)** · **[Executive Case Study](Docs/Executive_Report.pdf)** · **[Data Analytics Portfolio](https://data.ianocamposystems.com)**

## Explore the project — direct access

All core deliverables open directly from this table. Nothing needs to be moved to the repository root.

| Deliverable | Open the actual file | Why it matters |
| :--- | :--- | :--- |
| **Executive Summary (12 bullets)** | [Executive_Summary.txt](Executive_Summary.txt) | Fast overview of the scope, findings and priorities |
| **One-Page Insights Summary** | [One_Page_Insights_Summary.pdf](Docs/One_Page_Insights_Summary.pdf) | The most concise business-facing summary |
| **Executive Case Study** | [Executive_Report.pdf](Docs/Executive_Report.pdf) | Detailed business narrative and evidence |
| **Python analysis notebook** | [Logistics_Analysis_Documented.ipynb](Notebook/Logistics_Analysis_Documented.ipynb) | Cleaning, calculations, plots and saved validation |
| **Cleaned customers dataset** | [customers_clean.csv](Outputs/Cleaned_Data/customers_clean.csv) | 5,000 prepared customer records |
| **Cleaned products dataset** | [products_clean.csv](Outputs/Cleaned_Data/products_clean.csv) | 800 prepared product records |
| **Five exported charts (PNG)** | [Open chart folder](Outputs/Charts) | Standalone Python visualizations |
| **Six dashboard screenshots** | [Open screenshot folder](Assets) | Original 1920 × 1080 application captures |
| **Streamlit application source** | [logistics_delivery_dashboard.py](logistics_delivery_dashboard.py) | Inspectable interactive dashboard code |

## Executive snapshot

| Measure | Verified observation |
| :--- | ---: |
| Orders and shipments | **15,000** each |
| Shipments marked Delivered | **11,680 / 15,000 (77.87%)** |
| Average recorded delivery duration | **4.00 days**, based on **11,122** eligible shipments |
| Stricter chronology-screened duration | **4.02 days**, based on **5,667** shipments |
| Orders with a recorded return request | **1,200 / 15,000 (8.00%)** |
| Exact duplicate rows removed | **387**, from **89,888** original rows |
| Saved validation register | **85 / 85 PASS** |

**Interpretation boundary:** Delivered status does not establish on-time SLA compliance. The 8.00% figure counts orders with requests—not completed, confirmed item-level returns. The chronology-screened values describe a different sample, not a before-and-after improvement.

## What the findings mean for a business

| Evidence | Business implication | Decision supported |
| :--- | :--- | :--- |
| **7,436** payment-before-order flags, **7,397** shipping-before-order flags, and **3,707** shipment status/date conflicts | Source event sequencing requires investigation; these exception categories overlap | Reconcile timestamps and state transitions before setting service targets |
| Courier averages are close and rankings change after more restrictive date screening | Vendor rankings are sensitive to which shipments qualify for measurement | Define consistent eligibility and sample-size rules before benchmarking providers |
| **1,200** recorded return requests; **Changed mind** leads at **182 (15.17%)** | Recorded reasons guide investigation but do not prove root causes or closed returns | Capture standardized reasons and request-to-resolution outcomes |
| **Home & Kitchen: 352 / 4,076 (8.64%)** order-category association | Multi-category orders do not identify the product actually returned | Add returned item/SKU identification before product-specific interventions |

### Recommended operating priorities

**01 — Data reliability.** Establish a cross-system chronology and status exception register, assign review ownership, and measure unresolved exceptions and validated-event coverage.

**02 — Returns attribution.** Capture returned SKU IDs, standardized reasons, and closed-case outcomes. Track completeness before interpreting category patterns as product-level return rates.

These are **proposed actions** based on a synthetic demonstration dataset—not claims of implemented improvements, realized savings, or proven courier superiority.

## Interactive six-page dashboard

[![Actual 1920×1080 Streamlit operational overview with shipment status and recorded delivery duration](Assets/dashboard_01_overview_1920x1080.png)](Assets/dashboard_01_overview_1920x1080.png)

*Actual Streamlit screenshot — Overview (01/06). [Open the live dashboard](https://ianocampo-logistics-analytics-python-001.streamlit.app) or [inspect the full-resolution image](Assets/dashboard_01_overview_1920x1080.png). Screenshots capture the top viewport, not necessarily the entire scrollable page.*

<details>
<summary><strong>Explore the other five dashboard pages</strong></summary>

| Dashboard | Original screenshot | Analytical purpose |
| :--- | :--- | :--- |
| **02 — Courier Performance** | [View 1920×1080 PNG](Assets/dashboard_02_courier_performance_1920x1080.png) | Baseline versus chronology-screened courier comparisons |
| **03 — Returns Intelligence** | [View 1920×1080 PNG](Assets/dashboard_03_returns_intelligence_1920x1080.png) | Request reasons and order-category associations |
| **04 — Data Quality** | [View 1920×1080 PNG](Assets/dashboard_04_data_quality_1920x1080.png) | Overlapping timeline and state exception flags |
| **05 — Executive Brief** | [View 1920×1080 PNG](Assets/dashboard_05_executive_brief_1920x1080.png) | Supported business priorities |
| **06 — Data & Methodology** | [View 1920×1080 PNG](Assets/dashboard_06_data_methodology_1920x1080.png) | Data lineage, definitions and evidence downloads |

</details>

### Five original Python chart exports

| Original chart | File |
| :--- | :--- |
| Shipment status distribution | [shipment_status_distribution.png](Outputs/Charts/shipment_status_distribution.png) |
| Delivery lead-time distribution | [delivery_lead_time_histogram.png](Outputs/Charts/delivery_lead_time_histogram.png) |
| Courier average delivery days | [courier_average_delivery_days.png](Outputs/Charts/courier_average_delivery_days.png) |
| Recorded return reasons | [return_reasons_distribution.png](Outputs/Charts/return_reasons_distribution.png) |
| Category-associated return-request rates | [category_return_request_rate.png](Outputs/Charts/category_return_request_rate.png) |

## Verified reproducibility

**Fresh-run verification: PASS (November 7, 2026).** An isolated GitHub Actions runner on Python 3.11 executed the complete notebook without error, regenerated five charts, reconciled 14 published analytical CSV files, confirmed 85/85 saved QA checks, and verified unchanged SHA-256 hashes for all seven original CSVs. This is an actual end-to-end clean-environment run, distinct from the notebook's previously saved outputs.

[**View the reproducibility evidence and scope**](Docs/REPRODUCIBILITY_VERIFICATION.md) · [**Inspect the successful validation run**](https://github.com/ianocampo/logistics-python-analytics-dashboard/actions/runs/42376035355)

## Method and evidence

**Seven original CSVs → source audit → deduplication and field-specific preparation → joins and data-quality checks → executive metrics and Matplotlib charts → validated reporting exports → Plotly/Streamlit dashboard → evidence-backed recommendations.**

The notebook documents **387 exact duplicates** across customer, order, and order-item records; resulting prepared files contain **89,501 rows across seven different entities**. That combined row count is *not* a count of unique orders. Missing values, inconsistent source events, and orphan relationships are documented rather than silently corrected.

**Technology:** Python · pandas · NumPy · Jupyter · Matplotlib · Plotly · Streamlit · GitHub.

| Supporting material | Purpose |
| :--- | :--- |
| [Original seven CSVs](Data/Raw) | Preserved source records |
| [Seven cleaned datasets](Outputs/Cleaned_Data) | Analytical working tables |
| [Cleaning evidence](Outputs/Cleaning_Evidence) | Before/after reconciliation, decisions and saved QA register |
| [Dashboard exports](Outputs/Dashboard_Data) | Four dashboard-ready analytical tables |
| [Business findings and recommendations](Outputs/Tables) | Structured decision-support outputs |
| [Public data and methodology guide](Public_Data/DATA_GUIDE.md) | Data definitions, denominators, and downloadable evidence |
| [Source data dictionary](Data/Raw/README_DATA_DICTIONARY.txt) | Original supplied source documentation, retained unchanged |
| [Source data audit notebook](Notebook/Source_Data_Audit.ipynb) | Read-only source inventory before preparation |

The [original source dictionary](Data/Raw/README_DATA_DICTIONARY.txt) describes the input data as synthetically generated. It is preserved as source documentation; the public [data guide](Public_Data/DATA_GUIDE.md) explains how the records are used in this analytics project.

## Run the project locally

Install the dashboard dependencies from the repository root:

~~~bash
python -m pip install -r requirements.txt
python -m streamlit run logistics_delivery_dashboard.py
~~~

For the analytical notebooks, install their separate dependencies and launch Jupyter **from the repository root**:

~~~bash
python -m pip install -r requirements-analysis.txt
python -m notebook
~~~

Open the [main notebook](Notebook/Logistics_Analysis_Documented.ipynb) and use **Restart Kernel and Run All Cells**. The notebook searches for the bundled original data from the repository root or notebook folder. Re-execution may regenerate derived exports under Outputs; it does not intentionally modify the original Data/Raw CSVs.

**Evidence status:** The published notebook contains saved executed cells and no saved error outputs; its Step 109 validation log records **85/85 PASS** checks. This does **not** substitute for an independently witnessed full fresh-clone run. The deployed app reads the committed reporting exports.

## Data boundaries

- The datasets are **synthetic demonstration records**, not a client's private information or a live operational feed.
- Recorded status shares are not independently verified delivery SLAs.
- Return-request rates are order-level; categories may overlap and returned-item identity is unavailable.
- Source quality indicators overlap and identify review candidates, not confirmed operational failures.
- The dashboard operates as a read-only presentation of committed exports; no live refresh or realized improvement is claimed.

---

**Ian Ocampo** · Business & Digital Systems Integrator · Data Analytics & Business Intelligence  
[Explore the Data Analytics Portfolio](https://data.ianocamposystems.com) · [Open the Interactive Dashboard](https://ianocampo-logistics-analytics-python-001.streamlit.app)
