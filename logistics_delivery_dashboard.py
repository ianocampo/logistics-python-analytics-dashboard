"""Logistics, Delivery & Returns Intelligence | Ian Ocampo.

Launch from the project directory:
    python -m streamlit run logistics_delivery_dashboard.py

Sources: seven validated CSV exports produced by the Python capstone notebook.
Public source and evidence files are available in Public_Data/.
The application is read-only. It does not write to raw datasets or exports.

Logo priority: primary source is the official GHL-hosted CDN asset.
If the primary CDN request fails, use Assets/data_port_logo.png as fallback.
Never fabricate or replace the original logo artwork.
"""

# ================================================================
# STEP 113 — PUBLIC REPRODUCIBILITY + SIXTH PAGE
# ================================================================
# PURPOSE: Present decision-ready logistics analytics, accessible charts,
# quality limitations and evidence-based business recommendations.
# INPUT: Previously validated files in Outputs/Dashboard_Data and
#        Outputs/Tables (relative to this script's location).
# OUTPUT: Six-page Streamlit app with public reproducibility downloads.
# DATA SAFETY: No source data is edited or written during this run.
# SCOPE: Courier controls affect shipment analytics only. The delivery
#        sample toggle is LOCAL to Overview; courier benchmarking always
#        displays both samples. Returns and quality use whole-dataset counts.
# ================================================================

# SECTION 1 — IMPORTS AND PAGE SETUP
import base64
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from html import escape
from pathlib import Path
import mimetypes
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Logistics, Delivery & Returns Intelligence | Ian Ocampo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# SECTION 2 — DESIGN SYSTEM / FULL-WIDTH BRANDING FIX
# REFINEMENT: The previous 1.05rem top padding caused the masthead to slide
# beneath the Streamlit toolbar. Full-bleed branding now starts below it.
# Chart/KPI content remains constrained to 1400px for comfortable reading.
NAVY = "#0B1423"
PANEL = "#142236"
PANEL_ALT = "#102338"
TEAL = "#5EEAD4"
TEAL_DARK = "#159B98"
GOLD = "#D9B66F"
INK = "#EAF2F8"
MUTED = "#A7BAC9"
GRID = "#2C3E52"
BLUE = "#4E93B0"
CORAL = "#D97578"

# Responsive, restrained typography; visuals remain readable at 100% zoom.
st.markdown(
    """
    <style>
      .stApp {background:#0B1423; color:#EAF2F8;}
      [data-testid="stSidebar"] {background:#101D2D; border-right:1px solid #24394B;}
      [data-testid="stSidebar"] .stMarkdown {color:#D5E4ED;}
      /* The Streamlit Deploy/menu bar is the framework toolbar, not our header.
         Reserve enough space below it; don't position branding under the toolbar. */
      [data-testid="stMainBlockContainer"], .block-container {
        box-sizing:border-box;max-width:none!important;width:100%!important;
        padding:4.65rem 0 1.3rem!important;
      }
      /* Header + footer fill the entire MAIN dashboard area, beside the sidebar.
         Only charts, KPI cards and tab content use a comfortable max width. */
      .st-key-dashboard_body {
        box-sizing:border-box;max-width:1400px!important;
        width:calc(100% - 52px)!important;margin:14px auto 0!important;
      }
      .brand-masthead {display:flex;align-items:center;justify-content:space-between;gap:1rem;
        box-sizing:border-box;width:100%;min-height:82px;overflow:visible;
        padding:15px clamp(24px,4.4vw,78px);
        background:linear-gradient(110deg,#153244,#101D2E 82%);
        border-top:1px solid #294758;border-bottom:1px solid #294758;
        border-left:0;border-right:0;border-radius:0;}
      .brand-left {display:flex;align-items:center;gap:13px;min-width:0;}
      .brand-logo {display:block;max-width:108px;width:auto;height:auto;max-height:58px;
        object-fit:contain;flex:0 0 auto;}
      .brand-fallback {width:49px;height:49px;flex:0 0 auto;display:flex;align-items:center;
        justify-content:center;border:1px solid #337E81;border-radius:10px;
        background:#173D49;color:#5EEAD4;font-size:18px;font-weight:750;letter-spacing:-.04em;}
      .brand-name {font-size:18px;line-height:1.23;font-weight:750;color:#F4F9FD;}
      .brand-role {font-size:12px;line-height:1.4;color:#C5D7E3;}
      .brand-specialty {font-size:12px;line-height:1.4;color:#5EEAD4;font-weight:650;}
      .brand-right {flex:0 0 auto;text-align:right;}
      .brand-right strong {color:#D9B66F;display:block;font-size:10px;letter-spacing:.15em;}
      .brand-right small {color:#A7BAC9;font-size:11px;}
      .project-banner {box-sizing:border-box;width:100%;background:#101E30;
        border-bottom:1px solid #294758;border-top:0;border-left:0;border-right:0;
        border-radius:0;padding:12px clamp(24px,4.4vw,78px) 15px;margin:0;}
      .project-banner h1 {font-size:clamp(21px,2.2vw,29px);line-height:1.2;
        letter-spacing:-.025em;margin:0 0 4px;color:#F3FAFF;font-weight:750;}
      .project-banner p {font-size:12.5px;line-height:1.5;color:#AFC3D1;margin:0;}
      .section-eyebrow {margin:12px 0 4px;font-size:10px;letter-spacing:.16em;
        font-weight:750;color:#5EEAD4;text-transform:uppercase;}
      .section-title {font-size:20px;line-height:1.3;font-weight:720;color:#F4F9FD;margin:0 0 6px;}
      .section-note {font-size:13px;line-height:1.55;color:#B2C4D1;margin:0 0 11px;}
      .scope-note {font-size:12.5px;line-height:1.55;color:#B6CCD9;margin:8px 0 14px;}
      .screening-explainer {font-size:12.75px;line-height:1.55;color:#E5EEF4;
        padding:10px 14px;background:#12283A;border:1px solid #285064;
        border-radius:9px;margin:8px 0 13px;}
      .screening-explainer strong {color:#5EEAD4;}
      .decision-tag {display:inline-block;font-size:10px;letter-spacing:.08em;
        color:#D9B66F;font-weight:750;margin:0 0 6px;}
      .executive-card h3{line-height:1.4;}
      .executive-card b{color:#EAF2F8;}
      .method-card{background:#142236;border:1px solid #294053;border-radius:10px;
        padding:14px 16px;min-height:155px;margin:4px 0 8px;}
      .method-card h4{color:#F2F9FD;font-size:14px;line-height:1.4;margin:0 0 9px;}
      .method-card p{font-size:12.5px;line-height:1.55;color:#D5E6EF;margin:6px 0;}
      .method-card small{font-size:11.5px;line-height:1.5;color:#AAC6D3;}

      [data-testid="stMetric"] {background:#142236;border:1px solid #294053;
        padding:13px 15px;border-radius:11px;min-height:92px;}
      [data-testid="stMetricLabel"] {color:#B5CCD9;font-size:12px;}
      [data-testid="stMetricValue"] {color:#F5FBFF;font-size:clamp(20px,1.8vw,28px);}
      [data-testid="stTabs"] button {font-weight:650;font-size:13px;white-space:nowrap;}
      /* Primary control color comes from the project theme plus CLI overrides.
         CSS selectors supplement (not replace) Streamlit's native theming. */
      :root { color-scheme:dark; accent-color:#14B8A6; }
      [data-testid="stRadio"] input[type="radio"] {accent-color:#14B8A6!important;}
      [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
        color:#5EEAD4!important;
      }
      [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) p {
        color:#5EEAD4!important;
      }
      [data-testid="stTabs"] button[aria-selected="true"],
      [data-testid="stTabs"] button[aria-selected="true"] p {color:#5EEAD4!important;}
      [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background:#14B8A6!important;
      }
      [data-testid="stTabs"] button[aria-selected="true"] {border-bottom-color:#14B8A6!important;}
      [data-testid="stTabs"] {margin-top:2px;}
      /* Robust native-widget fallback for user browsers that retain the
         default red theme instead of loading the project configuration. */
      [data-testid="stTabs"] [role="tablist"] button[aria-selected="true"],
      [data-testid="stTabs"] [role="tablist"] button[aria-selected="true"] * {
        color:#5EEAD4!important;
      }
      [data-testid="stTabs"] [role="tablist"] button[aria-selected="true"] {
        border-bottom:2px solid #14B8A6!important;
        box-shadow:inset 0 -2px 0 #14B8A6!important;
      }
      [data-testid="stTabs"] [data-baseweb="tab-highlight"],
      [data-testid="stTabs"] [data-baseweb="tab-highlight"] div {
        background-color:#14B8A6!important;
      }
      [data-testid="stRadio"] input:checked {accent-color:#14B8A6!important;}
      [data-testid="stRadio"] label:has(input:checked) [data-baseweb="radio"] > div:first-child,
      [data-testid="stRadio"] label:has(input:checked) [data-baseweb="radio"] > div:first-child > div:first-child,
      [data-testid="stRadio"] label:has(input:checked) [role="radio"] > div:first-child {
        border-color:#14B8A6!important;
      }
      [data-testid="stRadio"] label:has(input:checked) [data-baseweb="radio"] > div:first-child > div,
      [data-testid="stRadio"] label:has(input:checked) [role="radio"] svg circle:last-child {
        background-color:#14B8A6!important;
        fill:#14B8A6!important;
      }
      /* Native captions were smaller than the accompanying charts at 100%.
         Improve readability, without enlarging cards or global components. */
      [data-testid="stCaptionContainer"] p,
      [data-testid="stCaptionContainer"] span {
        font-size:12px!important;
        line-height:1.5!important;
        color:#B6C9D6!important;
      }
      .insight-ribbon {padding:12px 15px;border-radius:9px;background:#143448;
        border-left:3px solid #5EEAD4;color:#E5F4F8;font-size:13px;line-height:1.5;
        margin:12px 0 18px;}
      .warning-ribbon {padding:10px 14px;border-radius:9px;background:#353522;
        border-left:3px solid #D9B66F;color:#F2E5BC;font-size:12px;line-height:1.5;
        margin:12px 0;}
      /* Compact evidence cards lower scroll burden without shrinking type. */
      .executive-card {background:#142236;border:1px solid #2B4052;border-radius:10px;
        padding:12px 15px;margin:7px 0;}
      .executive-card h3 {font-size:14px;margin:0 0 6px;color:#F2FAFF;line-height:1.35;}
      .executive-card p {font-size:13px;line-height:1.48;margin:4px 0;color:#D7E6EE;}
      .executive-card small {font-size:11.5px;line-height:1.45;color:#A7BAC9;}
      .priority-card {height:100%;margin:0;}
      .evidence-card {padding:10px 14px;margin:7px 0;}
      .evidence-card h3 {margin-bottom:4px;}
      .evidence-card p {margin:3px 0;}
      .portfolio-footer {box-sizing:border-box;width:100%;margin-top:28px;
        background:linear-gradient(110deg,#112637,#0D1A2A);
        border-top:1px solid #2D4657;border-bottom:1px solid #263A4B;
        padding:20px clamp(24px,4.4vw,78px) 14px;}
      .footer-top {display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;}
      .footer-name {font-size:13px;font-weight:750;color:#F2F8FC;}
      .footer-detail {font-size:11.5px;line-height:1.55;color:#A7BAC9;}
      .footer-link {font-size:12px;font-weight:700;color:#5EEAD4;text-decoration:none;}
      /* Separate compact project toolkit from attribution/disclosure, without a bulky footer. */
      .footer-toolkit {display:flex;gap:8px 24px;flex-wrap:wrap;
        border-top:1px solid #263C4D;margin-top:13px;padding-top:11px;
        color:#C9DBE6;font-size:11.5px;line-height:1.55;}
      .footer-toolkit strong {color:#5EEAD4;font-size:10px;
        font-weight:750;letter-spacing:.08em;margin-right:6px;}
      .footer-bottom {display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;
        border-top:1px solid #263C4D;margin-top:10px;padding-top:9px;
        color:#A6BAC9;font-size:11px;line-height:1.45;}
      .stPlotlyChart {border:1px solid #263A4C;border-radius:9px;overflow:hidden;}
      [data-testid="stDataFrame"] {border:1px solid #263A4C;border-radius:9px;}
      @media(max-width:900px){
        .brand-right{display:none}.block-container{padding-left:1rem;padding-right:1rem}
        .brand-masthead{padding:14px 18px;min-height:74px}
        .project-banner{padding:12px 18px 14px}
        .portfolio-footer{padding:18px 18px 14px}
        .st-key-dashboard_body{width:calc(100% - 26px)!important}
        .brand-name{font-size:16px}.brand-role,.brand-specialty{font-size:11px}
      }
      @media(max-width:600px){
        .brand-logo{max-width:66px;max-height:48px}
        .brand-left{gap:10px}.brand-name{font-size:15px}
        .brand-role,.brand-specialty{font-size:10px}
        .project-banner h1{font-size:21px}
        .st-key-dashboard_body{width:calc(100% - 22px)!important}
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# SECTION 3 — LOCATE THE NOTEBOOK'S VERIFIED EXPORTS
# Using __file__ means moving notebooks into NOTEBOOK/ does not affect
# this dashboard's ability to load validated CSV exports.
PROJECT_ROOT = Path(__file__).resolve().parent
DASHBOARD_DIR = PROJECT_ROOT / "Outputs" / "Dashboard_Data"
TABLE_DIR = PROJECT_ROOT / "Outputs" / "Tables"
# Prefer the existing notebook's validated Outputs/ on the owner's iMac.
# On public Streamlit Cloud, use identical verified CSVs from Public_Data/.
PUBLIC_DATA = PROJECT_ROOT / "Public_Data"
PUBLIC_SOURCE = PUBLIC_DATA / "Source"
PUBLIC_PREPARED = PUBLIC_DATA / "Prepared"
PUBLIC_EXPORTS = PUBLIC_DATA / "Reporting_Exports"
PUBLIC_CHARTS = PUBLIC_DATA / "Charts"

def local_or_public(local_path: Path) -> Path:
    """Choose notebook export first, then its portable public verified copy."""
    if local_path.is_file():
        return local_path
    return PUBLIC_EXPORTS / local_path.name

DATA_PATHS = {
    "shipments": local_or_public(DASHBOARD_DIR / "shipments_dashboard.csv"),
    "returns": local_or_public(DASHBOARD_DIR / "returns_dashboard.csv"),
    "categories": local_or_public(DASHBOARD_DIR / "order_category_dashboard.csv"),
    "kpis": local_or_public(DASHBOARD_DIR / "executive_kpis.csv"),
    "quality": local_or_public(TABLE_DIR / "data_quality_findings_register.csv"),
    "insights": local_or_public(TABLE_DIR / "business_insights.csv"),
    "recommendations": local_or_public(TABLE_DIR / "business_recommendations.csv"),
}
REQUIRED_COLUMNS = {
    "shipments": {"order_id", "courier", "shipment_status", "lead_time_days",
                  "lead_time_eligible", "lead_time_chronology_consistent",
                  "ship_before_order", "shipment_status_date_conflict"},
    "returns": {"order_id", "reason"},
    "categories": {"order_id", "category_reporting", "has_return_request"},
    "kpis": {"metric", "value"},
    "quality": {"quality_check", "flagged_records", "records_checked", "flagged_pct"},
    "insights": {"id", "topic", "finding", "interpretation", "limitation"},
    "recommendations": {"id", "recommendation", "action", "success_measure"},
}

@st.cache_data(show_spinner=False)
def load_exported_data() -> dict[str, pd.DataFrame]:
    """Load and schema-validate the seven dashboard exports without editing files."""
    missing = [str(path) for path in DATA_PATHS.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing exported CSV files:\n" + "\n".join(missing))
    data = {}
    for name, path in DATA_PATHS.items():
        df = pd.read_csv(path)
        absent = REQUIRED_COLUMNS[name] - set(df.columns)
        if absent:
            raise ValueError(f"{path.name} is missing columns: {sorted(absent)}")
        data[name] = df
    return data


def as_boolean(series: pd.Series) -> pd.Series:
    """Correctly interpret exported True/False strings, avoiding bool('False')."""
    return series.astype("string").str.strip().str.lower().isin(["true", "1"])


def chart_style(fig: go.Figure, *, height: int = 335) -> go.Figure:
    """Shared chart theme and layout that keep titles outside plotting areas."""
    fig.update_layout(
        template="plotly_dark", height=height,
        margin=dict(l=14, r=22, t=24, b=34),
        paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font=dict(color=INK, size=12),
        hoverlabel=dict(bgcolor="#1A3042", font_color=INK),
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig


def section(eyebrow: str, heading: str, note: str = "") -> None:
    """Reusable accessible section heading for all six dashboard pages."""
    st.markdown(
        f'<div class="section-eyebrow">{eyebrow}</div>'
        f'<div class="section-title">{heading}</div>'
        + (f'<p class="section-note">{note}</p>' if note else ""),
        unsafe_allow_html=True,
    )


# Primary brand source: user's existing logo hosted on the GHL media CDN.
# Local Assets directory is intentionally SECONDARY only.
GHL_LOGO_URL = (
    "https://assets.cdn.filesafe.space/DgN0za1SVUav6ss38Kw8/"
    "media/6ad0b1f3134df87e411f1158.png"
)


@st.cache_data(ttl=3600, show_spinner=False)
def primary_ghl_logo() -> tuple[bytes, str] | None:
    """Load the official GHL CDN artwork once per cache hour.

    PURPOSE: Favor the centrally hosted original asset over any local copy.
    SAFETY: Static trusted URL, timeout, image-type and size validation;
    no response is saved to the user's project or raw data folders.
    """
    request = Request(
        GHL_LOGO_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; PythonPortfolioDashboard/1.0)"},
    )
    try:
        with urlopen(request, timeout=4) as response:
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
            # Reject non-image responses and unexpectedly large assets.
            if not content_type.startswith("image/"):
                return None
            image_bytes = response.read(5_000_001)
            if not image_bytes or len(image_bytes) > 5_000_000:
                return None
            return image_bytes, content_type
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        return None


def portfolio_logo_markup() -> str:
    """GHL CDN is PRIMARY; local Assets PNG is fallback on CDN failure."""
    # SECTION A — OFFICIAL GHL-HOSTED IMAGE (FIRST PRIORITY)
    logo_data = primary_ghl_logo()
    if logo_data is not None:
        image_bytes, mime = logo_data
        encoded = base64.b64encode(image_bytes).decode("ascii")
        return (
            f'<img class="brand-logo" src="data:{mime};base64,{encoded}" '
            'alt="Ian Ocampo Data Analytics portfolio logo">'
        )

    # SECTION B — LOCAL BACKUP (ONLY WHEN GHL CDN IS UNREACHABLE)
    for filename in ("data_port_logo.png", "data_port_logo.webp", "data_port_logo.jpg"):
        logo_path = PROJECT_ROOT / "Assets" / filename
        if logo_path.is_file():
            mime = mimetypes.guess_type(str(logo_path))[0] or "image/png"
            encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
            return (
                f'<img class="brand-logo" src="data:{mime};base64,{encoded}" '
                'alt="Ian Ocampo Data Analytics portfolio logo">'
            )

    # SECTION C — NEUTRAL TEXT ONLY IF BOTH SOURCES ARE UNAVAILABLE
    return '<span class="brand-fallback" aria-label="Ian Ocampo">IO</span>'



# SECTION 3B — PUBLIC TRANSPARENCY DOWNLOADS
# Source originals remain immutable; ZIPs are built in memory and downloaded
# directly by the visitor's browser. No upload service or server write is used.
SOURCE_NAMES = ("customers", "products", "orders", "order_items",
                "payments", "shipments", "returns")
SOURCE_ROLES = {
    "customers": "Customer reference and geographic attributes",
    "products": "Product names, categories and reference prices",
    "orders": "Order identifiers, dates, status and channels",
    "order_items": "Order-to-product links and purchase quantities",
    "payments": "Payment timestamps, methods and values",
    "shipments": "Carrier, shipment status and shipping/delivery dates",
    "returns": "Order-level return requests and recorded reasons",
}

@st.cache_data(show_spinner=False)
def public_download_bundle(group: str) -> bytes:
    """Create downloadable public ZIP with deterministic file order."""
    groups = {
        "source": (PUBLIC_SOURCE, "Source"),
        "prepared": (PUBLIC_PREPARED, "Prepared"),
        "reporting": (PUBLIC_EXPORTS, "Reporting_Exports"),
        "charts": (PUBLIC_CHARTS, "Charts"),
    }
    if group not in groups:
        raise ValueError("Unknown public download category")
    directory, folder_name = groups[group]
    files = sorted(directory.glob("*.csv" if group != "charts" else "*.png"))
    if not files:
        raise FileNotFoundError(f"Public {group} evidence not packaged under {directory}")
    memory = BytesIO()
    with ZipFile(memory, "w", compression=ZIP_DEFLATED, compresslevel=6) as bundle:
        guide = PUBLIC_DATA / "DATA_GUIDE.md"
        if guide.is_file():
            bundle.writestr("DATA_GUIDE.md", guide.read_bytes())
        for file_path in files:
            bundle.write(file_path, f"{folder_name}/{file_path.name}")
    return memory.getvalue()


def available_original_sources() -> dict[str, Path]:
    """Use owner's original Data/Raw first; fall back to the public copies."""
    originals = {}
    for name in SOURCE_NAMES:
        local = PROJECT_ROOT / "Data" / "Raw" / f"{name}.csv"
        published = PUBLIC_SOURCE / f"{name}.csv"
        candidate = local if local.is_file() else published
        if candidate.is_file():
            originals[name] = candidate
    return originals


@st.cache_data(show_spinner=False)
def source_profile(path: str) -> tuple[int, int]:
    """Return original row and exact-row duplicate counts, read-only."""
    frame = pd.read_csv(path, low_memory=False)
    return len(frame), int(frame.duplicated().sum())

# SECTION 4 — READ AND CONVERT TYPES
try:
    data = load_exported_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
    st.error("The dashboard could not load its validated CSV exports.")
    st.code(str(exc))
    st.info("Place validated exports in Outputs/ or ship the matching files in Public_Data/Reporting_Exports/. Keep the notebook in NOTEBOOK/.")
    st.stop()

shipments = data["shipments"].copy()
returns = data["returns"].copy()
categories = data["categories"].copy()
kpis = data["kpis"].copy()
quality = data["quality"].copy()
insights = data["insights"].copy()
recommendations = data["recommendations"].copy()

shipments["lead_time_days"] = pd.to_numeric(shipments["lead_time_days"], errors="coerce")
for column in ("lead_time_eligible", "lead_time_chronology_consistent",
               "ship_before_order", "shipment_status_date_conflict"):
    shipments[column] = as_boolean(shipments[column])
categories["has_return_request"] = as_boolean(categories["has_return_request"])
kpis["value"] = pd.to_numeric(kpis["value"], errors="coerce")
for column in ("flagged_records", "records_checked", "flagged_pct"):
    quality[column] = pd.to_numeric(quality[column], errors="coerce")

# SECTION 5 — COMPACT SIDEBAR FILTERS
# Default to 'All couriers' to prevent a five-chip control from overwhelming
# the sidebar. Empty individual selections do NOT block independent tabs.
st.sidebar.markdown("**DASHBOARD CONTROLS**")
st.sidebar.caption("Logistics & Returns Intelligence")
st.sidebar.divider()
all_couriers = sorted(shipments["courier"].dropna().astype(str).unique().tolist())
courier_scope = st.sidebar.radio(
    "Courier scope", ["All couriers", "Choose couriers"],
    index=0, help="Affects shipment Overview and Courier Performance only.",
)
if courier_scope == "All couriers":
    selected_couriers = all_couriers
    st.sidebar.caption(f"{len(all_couriers)} of {len(all_couriers)} couriers selected")
else:
    selected_couriers = st.sidebar.multiselect(
        "Select couriers", options=all_couriers, default=all_couriers,
        help="Selecting none displays an empty-state message on shipment views.",
    )
    st.sidebar.caption(f"{len(selected_couriers)} of {len(all_couriers)} couriers selected")
# The cross-page sidebar intentionally contains ONLY the courier filter.
# The screening view is local to Overview because Courier Performance compares
# BOTH samples at the same time. Avoid suggesting a global data-screening filter.
st.sidebar.caption("Applies to Overview shipment metrics and Courier Performance only.")
st.sidebar.divider()
with st.sidebar.expander("About these data & filters", expanded=False):
    st.caption(
        "Courier selections affect shipment analytics only. Returns and Data Quality "
        "always use the full dataset. The two delivery samples are different record "
        "selection rules, not before/after operating periods. All figures are from "
        "synthetic demonstration data with known limitations."
    )

# Both delivery groups are already eligible derived observations, not raw data.
COHORT_LABEL_TO_COLUMN = {
    "Before Order-Date Screening": "lead_time_eligible",
    "After Order-Date Screening": "lead_time_chronology_consistent",
}
selected_shipments = shipments.loc[shipments["courier"].isin(selected_couriers)].copy()

metric_lookup = kpis.set_index("metric")["value"]
total_orders = int(metric_lookup.get("Total Orders", 0))
return_orders = int(metric_lookup.get("Orders with Return Requests", 0))
return_rate = (return_orders / total_orders * 100) if total_orders else 0.0

# SECTION 6 — FULL-WIDTH PROFESSIONAL HEADER / PROJECT IDENTITY
# This is deliberately BELOW Streamlit's built-in Deploy toolbar and extends
# from the sidebar edge to the right edge of the main dashboard panel.
st.markdown(
    f"""
    <div class="brand-masthead">
      <div class="brand-left">
        {portfolio_logo_markup()}
        <div>
          <div class="brand-name">Ian Ocampo</div>
          <div class="brand-role">Business &amp; Digital Systems Integrator</div>
          <div class="brand-specialty">Data Analytics &amp; Business Intelligence</div>
        </div>
      </div>
      <div class="brand-right"><strong>PYTHON ANALYTICS</strong><small>INTERACTIVE BUSINESS INTELLIGENCE</small></div>
    </div>
    <div class="project-banner">
      <h1>Logistics, Delivery &amp; Returns Intelligence</h1>
      <p>Operational visibility, courier benchmarking, returns intelligence, and responsible data-quality reporting.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# SECTION 7 — SIX PAGES (APP IS READ-ONLY)
# Readable max-width body, independent from end-to-end identity bars.
with st.container(key="dashboard_body"):
    tab_overview, tab_courier, tab_returns, tab_quality, tab_brief, tab_method = st.tabs([
        "01 · Overview", "02 · Courier Performance", "03 · Returns Intelligence",
        "04 · Data Quality", "05 · Executive Brief", "06 · Data & Methodology",
    ])

    with tab_overview:
        section("EXECUTIVE OVERVIEW", "Operational Snapshot",
                "At a glance: shipment metrics for selected couriers, plus the all-order return-request rate.")
        # This selector only changes the Overview delivery average and histogram.
        cohort = st.radio(
            "Delivery sample for the average and distribution below",
            list(COHORT_LABEL_TO_COLUMN), horizontal=True,
            help=(
                "Before: delivered shipments with usable shipping and delivery dates "
                "and nonnegative durations. After: the same group with shipping-before-order "
                "records excluded. These are NOT historical operating periods."
            ),
            key="overview_delivery_sample",
        )
        cohort_column = COHORT_LABEL_TO_COLUMN[cohort]
        eligible_selected = selected_shipments.loc[
            selected_shipments[cohort_column], "lead_time_days"
        ].dropna()
        shipment_n = len(selected_shipments)
        delivered_n = int(selected_shipments["shipment_status"].eq("Delivered").sum())
        k1, k2, k3, k4 = st.columns(4, gap="small")
        with k1: st.metric("Shipment records · selected", f"{shipment_n:,}")
        with k2: st.metric("Marked Delivered · selected", f"{delivered_n/shipment_n*100:.2f}%" if shipment_n else "N/A")
        with k3: st.metric("Avg. days · selected sample", f"{eligible_selected.mean():.2f}" if len(eligible_selected) else "N/A")
        with k4: st.metric("Return-request rate · all orders", f"{return_rate:.2f}%")
        st.markdown(
            f'<div class="scope-note"><b>Sample:</b> {escape(cohort)} ({len(eligible_selected):,} records). '
            f'<b>Returns:</b> {return_orders:,} of {total_orders:,} orders across all couriers. '
            '<b>Data trust:</b> reported delivery statuses and timestamps contain unresolved exceptions.</div>',
            unsafe_allow_html=True,
        )
        if shipment_n == 0:
            st.info("No couriers selected. Use the sidebar to choose one or switch to All couriers. Returns, Data Quality, and Executive Brief remain available.")
        else:
            # CLIENT INTERPRETATION: distinguish recorded status from independently
            # verified on-time delivery. Show an actionable trust-first next step.
            st.markdown(
                '<div class="insight-ribbon"><b>Executive takeaway:</b> '
                f'{delivered_n:,} of {shipment_n:,} selected shipments '
                f'({delivered_n/shipment_n*100:.2f}%) are <b>recorded</b> as Delivered. '
                'This is a shipment-status share, not a verified on-time delivery rate. '
                '<b>Decision:</b> reconcile event-date and status exceptions before using '
                'these figures to benchmark courier performance.</div>',
                unsafe_allow_html=True,
            )
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                st.markdown("**Shipment status breakdown**")
                statuses = selected_shipments["shipment_status"].fillna("Missing status").value_counts()
                status_df = pd.DataFrame({"status": statuses.index, "count": statuses.values})
                status_df["pct"] = status_df["count"] / shipment_n * 100
                status_df = status_df.sort_values("count", ascending=True)
                palette = {"Delivered": TEAL_DARK, "In Transit": BLUE,
                           "Returned to Sender": GOLD, "Lost": CORAL}
                fig = go.Figure(go.Bar(
                    x=status_df["count"], y=status_df["status"], orientation="h",
                    marker_color=[palette.get(s, "#8095A5") for s in status_df["status"]],
                    text=[f"{x:,} · {p:.1f}%" for x, p in zip(status_df["count"], status_df["pct"])],
                    textposition="outside", cliponaxis=False,
                    customdata=status_df[["pct"]].to_numpy(),
                    hovertemplate="%{y}<br>Shipments: %{x:,}<br>Share: %{customdata[0]:.2f}%<extra></extra>",
                ))
                fig.update_xaxes(title="Shipment records", range=[0, max(status_df["count"]) * 1.27])
                fig.update_yaxes(title=None)
                st.plotly_chart(chart_style(fig, height=355), width="stretch")
            with col2:
                st.markdown(f"**Recorded delivery-time distribution · {cohort}**")
                if eligible_selected.empty:
                    st.info("No eligible delivery durations for the selected couriers/cohort.")
                else:
                    fig = go.Figure(go.Histogram(
                        x=eligible_selected, xbins=dict(start=.5, end=7.5, size=1),
                        marker_color=TEAL_DARK, hovertemplate="%{x} days: %{y:,} shipments<extra></extra>",
                    ))
                    fig.update_layout(bargap=.10)
                    fig.update_xaxes(title="Recorded ship-to-delivery days", dtick=1)
                    fig.update_yaxes(title="Shipments")
                    st.plotly_chart(chart_style(fig, height=355), width="stretch")
            with st.expander("Methodology & interpretation", expanded=False):
                st.write(
                    "Before Order-Date Screening includes Delivered shipments with usable "
                    "shipping/delivery dates and nonnegative recorded ship-to-delivery durations. "
                    "After Order-Date Screening is a subset that removes records whose shipping date "
                    "precedes the linked order date. The raw 15,000 shipment records are not directly "
                    "compared in this chart. Screening does not verify every timestamp or demonstrate "
                    "an actual change in delivery speed."
                )

    with tab_courier:
        section(
            "COURIER BENCHMARKING",
            "Courier Delivery Times — Before vs. After Date Screening",
            "A data-reliability comparison, not a comparison of different operating periods. "
            "Courier selection comes from the sidebar; both samples always appear in the chart.",
        )
        if selected_shipments.empty:
            st.info("No couriers selected. Choose one or more in the sidebar to see shipment comparisons.")
        else:
            source = selected_shipments.copy()

            # Describe the two record-selection rules openly on the page.
            # Counts follow the courier filter rather than always quoting all couriers.
            before_screening_n = int(source["lead_time_eligible"].sum())
            after_screening_n = int(source["lead_time_chronology_consistent"].sum())
            excluded_by_order_date_n = before_screening_n - after_screening_n
            # Always show the denominators so clients know which records are compared.
            a, b, c = st.columns(3, gap="small")
            with a: st.metric("Before screening · records", f"{before_screening_n:,}")
            with b: st.metric("Excluded · date conflicts", f"{excluded_by_order_date_n:,}")
            with c: st.metric("After screening · records", f"{after_screening_n:,}")
            st.markdown(
                '<div class="screening-explainer">'
                '<strong>What changed?</strong> The first sample includes only Delivered shipments with '
                'valid, nonnegative ship-to-delivery durations. The second sample removes '
                f'<strong>{excluded_by_order_date_n:,}</strong> of those records because the shipping date '
                'was earlier than the linked order date. The averages are recalculated using '
                '<strong>different records—not different business periods.</strong> '
                'This does not prove improvement or deterioration in actual courier service.'
                '</div>', unsafe_allow_html=True,
            )

            source["baseline_days"] = source["lead_time_days"].where(source["lead_time_eligible"])
            source["screened_days"] = source["lead_time_days"].where(source["lead_time_chronology_consistent"])
            courier_table = (
                source.groupby("courier", dropna=False)
                .agg(baseline_n=("baseline_days", "count"),
                     baseline_avg_days=("baseline_days", "mean"),
                     screened_n=("screened_days", "count"),
                     screened_avg_days=("screened_days", "mean"))
                .reset_index().sort_values("screened_avg_days", na_position="last")
            )
            courier_table["delta_days"] = courier_table["screened_avg_days"] - courier_table["baseline_avg_days"]
            valid = courier_table.dropna(subset=["baseline_avg_days", "screened_avg_days"])
            if valid.empty:
                st.info("No usable before-and-after screening delivery durations are available for the selected couriers.")
            else:
                values = pd.concat([valid["baseline_avg_days"], valid["screened_avg_days"]])
                axis_low = float(values.min() - .055)
                axis_high = float(values.max() + .055)
                fig = go.Figure()
                for rec in valid.itertuples():
                    fig.add_trace(go.Scatter(
                        x=[rec.baseline_avg_days, rec.screened_avg_days],
                        y=[rec.courier, rec.courier], mode="lines",
                        line=dict(color="#5E7085", width=3),
                        showlegend=False, hoverinfo="skip",
                    ))
                for key, label, color, symbol in (
                    ("baseline_avg_days", "Before screening", BLUE, "circle"),
                    ("screened_avg_days", "After screening", TEAL, "diamond"),
                ):
                    fig.add_trace(go.Scatter(
                        x=valid[key], y=valid["courier"],
                        mode="markers", name=label, showlegend=True,
                        marker=dict(color=color, size=13, symbol=symbol, line=dict(color=PANEL, width=1)),
                        customdata=valid[["baseline_n", "screened_n"]].to_numpy(),
                        hovertemplate="<b>%{y}</b><br>Mean: %{x:.3f} days<extra>" + label + "</extra>",
                    ))
                fig.update_layout(showlegend=True, legend=dict(
                    orientation="h", x=0, y=1.16, xanchor="left", yanchor="bottom"),
                    margin=dict(l=15, r=28, t=58, b=42))
                fig.update_xaxes(title="Average delivery days (zoomed comparison scale)", range=[axis_low, axis_high], tickformat=".2f")
                fig.update_yaxes(title=None, categoryorder="array", categoryarray=valid["courier"].tolist()[::-1])
                st.markdown("**Average delivery time by courier — before vs. after screening**")
                st.plotly_chart(chart_style(fig, height=360), width="stretch")
                st.caption("**Axis note:** This dot plot uses a non-zero x-axis to distinguish small differences; compare the numeric values, not apparent bar lengths. No statistical superiority is implied.")
                # BUSINESS INTERPRETATION: selection-aware descriptive comparison.
                # A change in the screened sample does not measure improvement.
                if len(valid) > 1:
                    before_leader = valid.loc[valid["baseline_avg_days"].idxmin(), "courier"]
                    after_leader = valid.loc[valid["screened_avg_days"].idxmin(), "courier"]
                    screened_range = (
                        valid["screened_avg_days"].max()
                        - valid["screened_avg_days"].min()
                    )
                    # Rankings may stay the same when users select only a
                    # subset of couriers; never assert a change unconditionally.
                    if before_leader == after_leader:
                        leader_message = (
                            f'The lowest observed mean remains with '
                            f'<b>{escape(str(before_leader))}</b> after screening.'
                        )
                    else:
                        leader_message = (
                            f'The lowest observed mean shifts from '
                            f'<b>{escape(str(before_leader))}</b> to '
                            f'<b>{escape(str(after_leader))}</b> after screening.'
                        )
                    st.markdown(
                        '<div class="insight-ribbon"><b>Decision takeaway:</b> '
                        + leader_message
                        + f' Screened courier means span <b>{screened_range:.3f} days</b>. '
                        + 'This is data sensitivity, not proof of superior service.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<div class="insight-ribbon"><b>Decision takeaway:</b> '
                        'One courier is selected. The two values show how its mean changes '
                        'when flagged records are excluded; they do not establish an '
                        'improvement or compare couriers.</div>',
                        unsafe_allow_html=True,
                    )
            display = courier_table.rename(columns={
                "courier": "Courier", "baseline_n": "Before: records",
                "baseline_avg_days": "Before: avg days", "screened_n": "After: records",
                "screened_avg_days": "After: avg days", "delta_days": "Avg difference (days)",
            })
            st.dataframe(display.style.format({
                "Before: avg days": "{:.3f}", "After: avg days": "{:.3f}",
                "Avg difference (days)": "{:+.3f}",
            }), hide_index=True, width="stretch")
            st.download_button(
                "Download selected courier comparison (CSV)",
                data=courier_table.to_csv(index=False).encode("utf-8"),
                file_name="selected_courier_screening_comparison.csv",
                mime="text/csv",
                help="Downloads only the couriers selected in the sidebar. Both screening samples are included.",
                key="courier_csv_export",
            )
            with st.expander("Methodology: what was removed and why", expanded=False):
                st.write(
                    "**Step 1 — Before Order-Date Screening:** start with shipment records marked "
                    "Delivered that have usable shipping and delivery dates and a nonnegative "
                    "ship-to-delivery duration. This is already a filtered analytical sample, "
                    "not the full raw dataset of 15,000 shipments. "
                    "**Step 2 — After Order-Date Screening:** exclude records whose shipping "
                    "date falls before the linked order date. No timestamps are corrected or "
                    "imputed. Each courier's average is recalculated using its remaining "
                    "eligible records. "
                    "**Interpretation:** the 'Avg difference' column is the after-screening "
                    "average minus the before-screening average; it is NOT a measured change "
                    "in real-world delivery speed over time. The retained data are not "
                    "independently verified, and no statistical superiority test was performed."
                )

    with tab_returns:
        section("RETURNS INTELLIGENCE", "Return Requests & Category Associations",
                "Whole-dataset analysis. Courier filter does not change these results.")
        r1, r2, r3 = st.columns(3, gap="small")
        with r1: st.metric("Orders with requests", f"{return_orders:,}")
        with r2: st.metric("Return request rate", f"{return_rate:.2f}%")
        # A top reason/share is more actionable than the number of categories.
        reason_counts_all = returns["reason"].fillna("Unspecified").value_counts()
        top_reason = str(reason_counts_all.index[0]) if not reason_counts_all.empty else "None"
        top_reason_n = int(reason_counts_all.iloc[0]) if not reason_counts_all.empty else 0
        top_reason_share = (top_reason_n / len(returns) * 100) if len(returns) else 0.0
        with r3: st.metric("Most recorded reason", top_reason, help=f"{top_reason_n:,} requests · {top_reason_share:.2f}% of request records")
        # RETURNS TAKEAWAY: the largest label accounts for only a minority
        # of requests; category associations cannot identify returned products.
        st.markdown(
            '<div class="insight-ribbon"><b>Business takeaway:</b> '
            f'<b>{escape(top_reason)}</b> is the most common recorded reason '
            f'({top_reason_n:,} of {len(returns):,} requests; {top_reason_share:.2f}%). '
            'No single reason dominates. Capture verified returned-item IDs and '
            'review reasons before targeting product-category interventions.</div>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown("**Recorded return requests by reason**")
            reasons = returns["reason"].fillna("Unspecified").value_counts().reset_index()
            reasons.columns = ["reason", "requests"]
            reasons = reasons.sort_values("requests")
            fig = go.Figure(go.Bar(
                x=reasons["requests"], y=reasons["reason"], orientation="h",
                marker_color=TEAL_DARK, text=[f"{v:,}" for v in reasons["requests"]],
                textposition="outside", cliponaxis=False,
                hovertemplate="%{y}: %{x:,} requests<extra></extra>",
            ))
            fig.update_xaxes(title="Return requests", range=[0, float(reasons["requests"].max())*1.18])
            fig.update_yaxes(title=None)
            st.plotly_chart(chart_style(fig, height=380), width="stretch")
        with col2:
            st.markdown("**Category-associated return-request rate**")
            category_table = (
                categories.groupby("category_reporting", dropna=False)
                .agg(orders_containing_category=("order_id", "nunique"),
                     orders_with_return_request=("has_return_request", "sum"))
                .reset_index()
            )
            category_table["rate_pct"] = (
                category_table["orders_with_return_request"] /
                category_table["orders_containing_category"] * 100
            )
            ranked = category_table.sort_values("rate_pct")
            fig = go.Figure(go.Bar(
                x=ranked["rate_pct"], y=ranked["category_reporting"], orientation="h",
                marker_color=TEAL_DARK, text=[f"{v:.2f}%" for v in ranked["rate_pct"]],
                textposition="outside", cliponaxis=False,
                customdata=ranked[["orders_containing_category", "orders_with_return_request"]].to_numpy(),
                hovertemplate="%{y}: %{x:.2f}%<br>Orders with category: %{customdata[0]:,}<br>Associated request orders: %{customdata[1]:,}<extra></extra>",
            ))
            fig.update_xaxes(title="Order-category association rate (%)", range=[0, float(ranked["rate_pct"].max())*1.22])
            fig.update_yaxes(title=None)
            st.plotly_chart(chart_style(fig, height=380), width="stretch")
        st.markdown(
            '<div class="warning-ribbon"><b>How to read category percentages:</b> '
            'The rate shows the share of orders <b>containing that category</b> that also had a return request. '
            'The return record does not say which item was returned. '
            'An order containing several categories can appear in several category calculations. '
            'These are <b>not verified returned-product rates</b>.</div>', unsafe_allow_html=True,
        )
        # Home & Kitchen is an example computed from the current category table,
        # never a hardcoded denominator or invented returned-product attribution.
        home_row = category_table.loc[
            category_table["category_reporting"] == "Home & Kitchen"
        ]
        if not home_row.empty:
            home = home_row.iloc[0]
            st.caption(
                f"**Calculation example — Home & Kitchen:** "
                f"{int(home['orders_with_return_request']):,} orders with return requests "
                f"÷ {int(home['orders_containing_category']):,} orders containing Home & Kitchen "
                f"= {float(home['rate_pct']):.2f}%. "
                "This does **not** establish that the returned item belonged to Home & Kitchen."
            )
        with st.expander("Show category denominators & counts", expanded=False):
            st.dataframe(category_table.sort_values("rate_pct", ascending=False).rename(columns={
                "category_reporting": "Category", "orders_containing_category": "Orders containing category",
                "orders_with_return_request": "Orders with request", "rate_pct": "Association rate (%)",
            }).style.format({"Association rate (%)": "{:.2f}"}), hide_index=True, width="stretch")

    with tab_quality:
        section("DATA TRUST & RELIABILITY", "Source Data Quality Exception Register",
                "Whole-dataset checks; percentages represent overlapping findings, not unique affected orders.")
        # Make the two major chronology indicators visible at a glance.
        flagged_by_type = quality.set_index("quality_check")
        d1, d2 = st.columns(2, gap="small")
        for slot, quality_name, display_name in (
            (d1, "Payment date before order", "Payment chronology flagged"),
            (d2, "Shipping date before order", "Shipping chronology flagged"),
        ):
            with slot:
                match = flagged_by_type.loc[quality_name] if quality_name in flagged_by_type.index else None
                if match is not None:
                    st.metric(display_name, f"{float(match['flagged_pct']):.2f}%",
                              help=f"{int(match['flagged_records']):,} of {int(match['records_checked']):,} checked records")
        st.markdown(
            '<div class="insight-ribbon"><b>Why this matters:</b> '
            'Separate payment and shipping chronology checks each flag nearly half of their '
            '15,000 checked records. Without source reconciliation, sequence-based KPIs '
            'can mislead decisions. '
            'These are <b>synthetic-data review flags</b>, not confirmed business failures. '
            'The five indicators overlap; do not add them as unique affected orders.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Five source-data quality indicators**")
        q = quality.sort_values("flagged_pct")
        fig = go.Figure(go.Bar(
            x=q["flagged_pct"], y=q["quality_check"], orientation="h",
            marker_color=GOLD,
            text=[f"{v:.2f}%" for v in q["flagged_pct"]],
            textposition="outside", cliponaxis=False,
            customdata=q[["flagged_records", "records_checked"]].to_numpy(),
            hovertemplate="%{y}: %{x:.2f}%<br>Flagged: %{customdata[0]:,} / %{customdata[1]:,}<extra></extra>",
        ))
        fig.update_xaxes(title="Checked records flagged (%)", range=[0, max(55, float(q["flagged_pct"].max())*1.2)])
        fig.update_yaxes(title=None)
        st.plotly_chart(chart_style(fig, height=345), width="stretch")
        st.dataframe(quality.sort_values("flagged_records", ascending=False).rename(columns={
            "quality_check": "Quality indicator", "flagged_records": "Flagged records",
            "records_checked": "Records checked", "flagged_pct": "Flagged (%)",
        }).style.format({"Flagged (%)": "{:.2f}"}), hide_index=True, width="stretch")
        with st.expander("Why these quality checks matter for decisions", expanded=False):
            st.markdown(
                "**Event chronology — payment or shipping before order:** the source timestamps "
                "may distort sequence-based KPIs and should be reconciled before operational benchmarking."
            )
            st.markdown(
                "**Shipment status/date consistency:** recorded shipment status can disagree with "
                "delivery-date fields, limiting confidence in fulfillment reporting."
            )
            st.markdown(
                "**Cancelled versus delivered/paid states:** potential exceptions for business-rule "
                "review; legitimate operational scenarios may explain some combinations."
            )
        st.markdown(
            '<div class="warning-ribbon"><b>Reporting limitation:</b> Indicators overlap and MUST NOT be summed '
            'as unique affected orders. Cancelled/Delivered records are review candidates, not automatic proof '
            'of business errors. Source data are synthetic with unresolved chronology.</div>', unsafe_allow_html=True,
        )
        st.download_button("Download quality register (CSV)",
                           data=quality.to_csv(index=False).encode("utf-8"),
                           file_name="data_quality_findings_register.csv", mime="text/csv")

    with tab_brief:
        section("EXECUTIVE DECISION SUPPORT", "Business Priorities & Evidence",
                "Lead with recommended actions; supporting insights and data limitations remain available below.")
        st.markdown(
            '<div class="insight-ribbon"><b>Executive summary:</b> Recorded shipment performance and '
            'order-level returns are measurable, but substantial cross-system chronology anomalies '
            'limit the strength of operational conclusions. Prioritize reliable reporting before '
            'optimizing courier or category performance.</div>', unsafe_allow_html=True,
        )
        st.markdown("**Operational priorities — what to do next**")
        # Context is a business interpretation; the source recommendation text
        # stays intact, and these are proposals (not implemented results).
        priority_context = {
            "R01": "Cross-system event dates conflict in many records, so chronology-based performance reporting needs stronger controls.",
            "R02": "Return requests lack verified returned-item attribution, limiting root-cause and category-specific decisions.",
        }
        # Compact two-column priorities on desktop; Streamlit columns stack
        # on narrow devices. Show business action before technical evidence.
        priority_cols = st.columns(2, gap="medium")
        for index, (_, rec) in enumerate(recommendations.iterrows()):
            rec_id = str(rec["id"])
            rationale = priority_context.get(rec_id, "Validate the evidence before taking action.")
            with priority_cols[index % 2]:
                st.markdown(
                    '<div class="executive-card priority-card">'
                    f'<span class="decision-tag">PRIORITY {index + 1:02d}</span>'
                    f'<h3>{escape(str(rec["recommendation"]))}</h3>'
                    f'<p><b>Why:</b> {escape(rationale)}</p>'
                    f'<p><b>Action:</b> {escape(str(rec["action"]))}</p>'
                    f'<small><b>Measure:</b> {escape(str(rec["success_measure"]))}</small>'
                    '</div>', unsafe_allow_html=True,
                )
        st.markdown("**Key evidence behind these priorities**")
        priority_ids = ["I01", "I04", "I07"]
        # Concise client-facing implications. Facts and limitations still come
        # directly from the previously validated business_insights.csv export.
        evidence_business_use = {
            "I01": (
                "Use the Delivered status as a recorded shipment-status share, "
                "not a verified on-time delivery performance measure."
            ),
            "I04": (
                "Monitor return-request volume, but verify completed returns "
                "and returned items before targeting product categories."
            ),
            "I07": (
                "Reconcile event chronology and cross-system status records "
                "before relying on time-based performance comparisons."
            ),
        }
        for _, rec in insights[insights["id"].isin(priority_ids)].iterrows():
            rec_id = str(rec["id"])
            business_use = evidence_business_use.get(rec_id, str(rec["interpretation"]))
            st.markdown(
                '<div class="executive-card evidence-card">'
                f'<span class="decision-tag">{escape(rec_id)} · EVIDENCE</span>'
                f'<h3>{escape(str(rec["topic"]))}</h3>'
                f'<p>{escape(str(rec["finding"]))}</p>'
                f'<small><b>Decision relevance:</b> {escape(business_use)}<br>'
                f'<b>Reporting limit:</b> {escape(str(rec["limitation"]))}</small></div>',
                unsafe_allow_html=True,
            )
        with st.expander("View all seven findings and methodology limitations", expanded=False):
            for _, rec in insights.iterrows():
                st.markdown(f"**{rec['id']} · {rec['topic']}**")
                st.write(rec["finding"])
                st.caption(f"Why it matters: {rec['interpretation']}")
                st.caption(f"Limitation: {rec['limitation']}")
                st.divider()
        st.caption(
            "For source files, KPI definitions, preparation rules and the Python technology "
            "workflow, see **06 · Data & Methodology**."
        )
        left, right = st.columns(2, gap="medium")
        with left:
            st.download_button("Download seven findings (CSV)",
                               data=insights.to_csv(index=False).encode("utf-8"),
                               file_name="business_insights.csv", mime="text/csv")
        with right:
            st.download_button("Download recommendations (CSV)",
                               data=recommendations.to_csv(index=False).encode("utf-8"),
                               file_name="business_recommendations.csv", mime="text/csv")

    # SECTION 7F — PUBLIC DATA & METHODOLOGY, OWNER-FACING AND REPRODUCIBLE
    with tab_method:
        section(
            "DATA TRANSPARENCY & REPRODUCIBILITY",
            "Explore the Data & Methodology",
            "See exactly what was analyzed, how the metrics were produced, and download "
            "the evidence behind this public Python portfolio demonstration.",
        )
        st.markdown(
            '<div class="insight-ribbon"><b>Public demonstration:</b> '
            'This dashboard uses seven synthetic training CSVs. The original data, '
            'prepared reference tables, reporting exports and PNG charts can be '
            'downloaded for independent inspection. The dashboard does not claim '
            'live operational updates or access to a real company’s private data.</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**01 — Original source datasets**")
        original_paths = available_original_sources()
        if len(original_paths) != len(SOURCE_NAMES):
            st.warning(
                "Some original source datasets have not been included in this installation. "
                "The analysis and dashboard remain available from verified reporting exports."
            )
        source_rows = []
        for dataset_name in SOURCE_NAMES:
            p = original_paths.get(dataset_name)
            if p is not None:
                raw_n, duplicate_n = source_profile(str(p))
                source_rows.append({
                    "Dataset": f"{dataset_name}.csv",
                    "Original records": raw_n,
                    "Exact duplicate rows": duplicate_n,
                    "What it contains": SOURCE_ROLES[dataset_name],
                })
        if source_rows:
            st.dataframe(pd.DataFrame(source_rows), hide_index=True, width="stretch")

        st.markdown("**02 — Original vs. prepared data**")
        st.caption(
            "The preparation files illustrate exact-row deduplication only. Other cleaning "
            "choices, join checks and metric-specific exclusions are documented in the "
            "Python analysis workflow; they are not silently rewritten here."
        )
        prep_rows = []
        for name in ("customers", "orders", "order_items", "products"):
            path = original_paths.get(name)
            if path is None:
                continue
            raw_n, dup_n = source_profile(str(path))
            prep_rows.append({
                "Dataset": name,
                "Original rows": raw_n,
                "Exact duplicates removed": dup_n,
                "Deduplicated reference rows": raw_n - dup_n,
            })
        if prep_rows:
            st.dataframe(pd.DataFrame(prep_rows), hide_index=True, width="stretch")

        st.markdown("**03 — KPI definitions and calculation rules**")
        # Present methodology as wrap-friendly business cards, not a wide,
        # truncated table of formulas. Two cards per row stack on small screens.
        kpi_definitions = [
            ("Recorded delivered share", "Delivered status records / shipments in the courier selection", "Not a verified on-time SLA measure"),
            ("Recorded delivery duration", "Delivered date − shipping date; eligible nonnegative durations", "11,122 baseline observations across all couriers"),
            ("After order-date screening", "Baseline subset excluding shipping-before-order conflicts", "5,667 observations; the periods are not different"),
            ("Return-request rate", "Unique order IDs with requests / 15,000 unique orders", "1,200 / 15,000 = 8.00%; not necessarily completed returns"),
            ("Category-associated request rate", "Request orders containing category / all orders containing category", "The returned product is unidentified in multi-category orders"),
            ("Quality exception share", "Flagged records for each check / checked records", "Findings overlap, so do not add the rates together"),
        ]
        for i in range(0, len(kpi_definitions), 2):
            boxes = st.columns(2, gap="medium")
            for box, (metric, formula, limitation) in zip(boxes, kpi_definitions[i:i+2]):
                with box:
                    st.markdown(
                        '<div class="method-card">'
                        f'<h4>{escape(metric)}</h4>'
                        f'<p><b>Calculation:</b> {escape(formula)}</p>'
                        f'<small><b>Interpret carefully:</b> {escape(limitation)}</small>'
                        '</div>', unsafe_allow_html=True,
                    )
        # Match the live validated category reporting table instead of freezing
        # 352 / 4,076 into the markup if the published dataset is updated.
        home_data = categories.loc[categories["category_reporting"] == "Home & Kitchen"]
        if not home_data.empty:
            n_total = int(home_data["order_id"].nunique())
            n_requested = int(home_data["has_return_request"].sum())
            home_share = n_requested / n_total * 100 if n_total else 0.0
            st.markdown(
                '<div class="screening-explainer"><strong>Category example — Home &amp; Kitchen:</strong> '
                f'<b>{n_requested:,}</b> of <b>{n_total:,}</b> orders containing the category '
                f'had a recorded return request (<b>{home_share:.2f}%</b>). '
                'Because requests are linked to <b>orders</b> rather than specific '
                'returned <b>items</b>, the result does not prove that a Home &amp; '
                'Kitchen product was the item returned.</div>',
                unsafe_allow_html=True,
            )

        st.markdown("**04 — Public datasets and evidence downloads**")
        st.caption(
            "These files are downloaded by your browser. No account or sign-in is required. "
            "The ZIPs are stored in this published project and read on demand."
        )
        choices = (
            ("source", "Original source CSVs", "7 unmodified synthetic training CSVs", "01_original_source_csvs.zip"),
            ("prepared", "Deduplicated reference data", "4 reference CSVs, exact-row duplicates removed", "02_deduplicated_reference_tables.zip"),
            ("reporting", "Verified analytics exports", "7 validated CSVs that support the dashboard", "03_dashboard_reporting_exports.zip"),
            ("charts", "Five required PNG charts", "Original Matplotlib figures for evidence review", "04_capstone_charts_png.zip"),
        )
        for left_choice, right_choice in ((choices[0], choices[1]), (choices[2], choices[3])):
            cols = st.columns(2, gap="medium")
            for col, (group, label, detail, filename) in zip(cols, (left_choice, right_choice)):
                with col:
                    st.markdown(f"**{label}**")
                    st.caption(detail)
                    directory = {
                        "source": PUBLIC_SOURCE, "prepared": PUBLIC_PREPARED,
                        "reporting": PUBLIC_EXPORTS, "charts": PUBLIC_CHARTS,
                    }[group]
                    if directory.is_dir() and any(directory.iterdir()):
                        st.download_button(
                            f"Download {label} (ZIP)",
                            data=public_download_bundle(group),
                            file_name=filename, mime="application/zip",
                            key=f"public_{group}_bundle",
                        )
                    else:
                        st.info("File bundle not present in this local installation.")
        guide_path = PUBLIC_DATA / "DATA_GUIDE.md"
        if guide_path.is_file():
            st.download_button(
                "Download Data & Methodology Guide (Markdown)",
                data=guide_path.read_bytes(), file_name="DATA_GUIDE.md",
                mime="text/markdown", key="public_data_guide",
            )

        st.markdown("**05 — How the Python workflow connects the evidence**")
        st.markdown(
            "**Original CSVs → Pandas preparation and validation → linked order, shipment and "
            "return measures → Matplotlib charts and seven dashboard CSV exports → "
            "Plotly visualizations in Streamlit.**"
        )
        st.caption(
            "Python, Jupyter Notebook, Pandas and NumPy support the analytical workflow; "
            "Matplotlib produces the five static charts; Plotly and Streamlit power the "
            "interactive business dashboard. Source date inconsistencies were flagged, "
            "not silently corrected. The notebook is a separate reproducibility artifact "
            "for the public project repository."
        )
        st.markdown(
            '<div class="warning-ribbon"><b>Important:</b> The source records are synthetic; '
            'results are descriptive and subject to documented data-quality limitations. '
            'There is no claim of actual cost savings, implemented operational changes, '
            'or statistically proven courier superiority.</div>',
            unsafe_allow_html=True,
        )
        st.link_button("View the Data Analytics Portfolio", "https://data.ianocamposystems.com")

# SECTION 8 — SHARED FULL-WIDTH PROFESSIONAL FOOTER
# A GHL portfolio link remains available even if a Streamlit instance sleeps.
st.markdown(
    """
    <footer class="portfolio-footer">
      <div class="footer-top">
        <div><div class="footer-name">Ian Ocampo</div>
             <div class="footer-detail">Business &amp; Digital Systems Integrator</div>
             <div class="footer-detail">Data Analytics &amp; Business Intelligence</div></div>
        <div style="text-align:right"><a class="footer-link" href="https://data.ianocamposystems.com"
             target="_blank" rel="noopener noreferrer">View Data Portfolio ↗</a>
             <div class="footer-detail">data.ianocamposystems.com</div></div>
      </div>
      <div class="footer-toolkit" aria-label="Technologies used in this capstone">
        <span><strong>ANALYSIS</strong> Python · Jupyter Notebook · Pandas · NumPy · Matplotlib</span>
        <span><strong>INTERACTIVE DASHBOARD</strong> Plotly · Streamlit</span>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Ian Ocampo. All rights reserved.</span>
        <span>Public synthetic-data demonstration · See Data &amp; Methodology for downloads and limitations.</span>
      </div>
    </footer>
    """, unsafe_allow_html=True,
)
