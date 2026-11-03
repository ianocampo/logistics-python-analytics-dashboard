#!/bin/bash
# Beginner-friendly launcher for six clean dashboard screenshots.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$HOME/.cache/ios-dashboard-capture-env"
DASHBOARD_PORT="${DASHBOARD_PORT:-8501}"
export DASHBOARD_PORT

echo "========================================================"
echo "  Python Portfolio | Clean 6-Page Dashboard Capture"
echo "========================================================"
echo "Project: $REPO_DIR"
echo "Dashboard URL: http://localhost:$DASHBOARD_PORT"
echo ""

if [ ! -f "$REPO_DIR/logistics_delivery_dashboard.py" ]; then
  echo "ERROR: Project dashboard source was not found."
  exit 1
fi

# Streamlit health endpoint confirms that the user's local app is running.
if ! curl -fsS --max-time 4 "http://127.0.0.1:$DASHBOARD_PORT/_stcore/health" >/dev/null; then
  echo "Dashboard is not currently running at http://localhost:$DASHBOARD_PORT"
  echo "Start your Streamlit dashboard first, then rerun this command."
  echo "Example (from the repository folder):"
  echo "  python -m streamlit run logistics_delivery_dashboard.py --server.port $DASHBOARD_PORT"
  exit 1
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
  echo "Creating a separate screenshot-only Python environment..."
  python3 -m venv "$VENV_DIR"
fi

if ! "$VENV_DIR/bin/python" -c "import playwright" >/dev/null 2>&1; then
  echo "Installing the Playwright screenshot helper..."
  "$VENV_DIR/bin/python" -m pip install "playwright>=1.54,<2"
fi

echo ""
echo "Capturing six pages using headless Chrome (no browser bookmarks)..."
"$VENV_DIR/bin/python" "$SCRIPT_DIR/capture_dashboard_previews.py"
echo ""
echo "Opening the preview images folder..."
open "$REPO_DIR/Assets"
