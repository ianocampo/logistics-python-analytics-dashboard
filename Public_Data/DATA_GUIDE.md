# Logistics, Delivery & Returns Intelligence — Public Data Guide

This is a **public portfolio demonstration** built on seven **synthetic demonstration CSV datasets**. The full original files are downloadable and included with the application. The demo is not a live client's operational system.

## Project architecture
- `Public_Data/Source/`: the **seven unmodified original CSV source files**. The same originals may also be present in `Data/Raw/` for local notebook work.
- `Public_Data/Prepared/`: **four deduplicated reference CSVs**. These represent only exact-row deduplication and are **not** a claim that all source issues have been cleaned or corrected.
- `Public_Data/Reporting_Exports/`: seven analysis-ready exports used by the interactive dashboard (including 15,000 shipments, 1,200 return requests, 33,165 order-category associations, 13 KPIs, a quality register, seven insights, and two recommendations).
- `Public_Data/Charts/`: five downloadable Matplotlib PNG figures associated with the notebook outputs; the primary exported-chart paths are in Outputs/Charts/.
- `logistics_delivery_dashboard.py`: public interactive dashboard (Streamlit + Plotly), read-only with respect to source CSVs.

## Original data to deduplication
| Source | Original rows | Exact duplicates removed | Deduplicated rows |
|---|---:|---:|---:|
| customers | 5,050 | 50 | 5,000 |
| orders | 15,075 | 75 | 15,000 |
| order_items | 37,763 | 262 | 37,501 |
| products | 800 | 0 | 800 |

The product-category standardization is part of the analytical notebook/reporting transformation; the prepared product reference is intentionally not represented as completely standardized.

## Key measures and denominators
- **Recorded Delivered Share**: shipments with status `Delivered` / shipments included by courier filter. It is **not** an on-time delivery SLA measure.
- **Recorded Delivery Duration**: `delivered_date - ship_date`; only Delivered records with valid nonnegative durations are eligible (11,122 across all couriers).
- **After Order-Date Screening**: subset of those eligible shipments excluding shipping-before-order inconsistencies (5,667 across all couriers). This is a **data-screening comparison**, not a time-series improvement.
- **Return-request rate**: unique order IDs with a recorded return request / all 15,000 analyzed orders = 1,200/15,000 = 8%. Requests are not necessarily completed returns.
- **Home & Kitchen category association**: 352 orders containing this category with a return request / 4,076 orders containing this category = 8.64%. A multi-category order can be included in more than one category. **This does not attribute the returned item to Home & Kitchen.**
- **Quality indicators**: 7,436 payment-before-order flags; 7,397 shipping-before-order flags; 3,707 status/date conflicts; 938 cancelled/delivered review candidates; 782 cancelled/delivered/paid review candidates. The indicators overlap; never add them as unique affected orders.

## Reproducibility and source of truth
Start from the original CSVs and use the documented Python analysis notebook to reproduce the transformations, KPIs, and charts. Compare notebook-generated exports with `Public_Data/Reporting_Exports/`. The dashboard consumes validated CSV exports; it does not recompute every historical cleaning step at page load. When deploying to Streamlit Cloud, `Public_Data/Reporting_Exports/` serves as a portable fallback if local `Outputs/` is absent.

## Publication status
Public synthetic demonstration data are intentionally included for inspection. This is not a private client dataset or a production-grade system with live data refreshes. Its known quality limitations are part of the project's documented findings. This public repository contains the client-facing case study, dashboard assets, and reproducibility evidence only.
