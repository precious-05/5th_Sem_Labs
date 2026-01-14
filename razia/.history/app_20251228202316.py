from nicegui import ui
import httpx
import pandas as pd
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================
API_URL = "https://api.irail.be/v1/vehicle/"

# =====================================================
# DATA FETCH
# =====================================================
def fetch_train_data(train_id):
    params = {
        "id": train_id,
        "format": "json",
        "lang": "en",
        "alerts": "false"
    }

    with httpx.Client(timeout=15) as client:
        response = client.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()

# =====================================================
# DATA PROCESSING
# =====================================================
def process_data(raw):
    stops = raw["vehicle"]["stops"]["stop"]
    rows = []

    for s in stops:
        rows.append({
            "Station": s["station"],
            "Arrival": format_time(s.get("arrivalTime")),
            "Departure": format_time(s.get("departureTime")),
            "Platform": s.get("platform", "-"),
            "Delay (min)": int(s.get("delay", 0)) // 60
        })

    return pd.DataFrame(rows)

def format_time(ts):
    if not ts:
        return "-"
    return datetime.fromtimestamp(int(ts)).strftime("%H:%M")

# =====================================================
# UI HELPERS
# =====================================================
def load_journey():
    if not train_input.value:
        ui.notify("Please enter a train ID", color="red")
        return

    ui.notify("Loading journey details...", color="blue")

    try:
        raw = fetch_train_data(train_input.value)
        df = process_data(raw)

        table.rows = df.values.tolist()
        ui.notify("Journey loaded successfully 🚆", color="green")

    except Exception as e:
        ui.notify("Invalid Train ID or API error", color="red")

# =====================================================
# UI PAGE
# =====================================================
@ui.page("/")
def main():
    ui.label("🚆 RailPulse").classes("text-3xl font-bold")
    ui.label("Live Train Journey Viewer").classes("text-gray-500")

    ui.separator()

    with ui.card().classes("w-full p-4"):
        ui.label("Enter Train ID").classes("font-semibold")
        ui.label("Example: BE.NMBS.IC1832").classes("text-sm text-gray-400")

        with ui.row():
            global train_input
            train_input = ui.input(
                placeholder="Train ID"
            ).classes("w-64")

            ui.button("View Journey", on_click=load_journey)

    ui.separator()

    global table
    table = ui.table(
        columns=[
            {"name": "station", "label": "Station"},
            {"name": "arrival", "label": "Arrival"},
            {"name": "departure", "label": "Departure"},
            {"name": "platform", "label": "Platform"},
            {"name": "delay", "label": "Delay (min)"},
        ],
        rows=[]
    ).classes("w-full")

    ui.label(
        "Powered by iRail API • Designed for clarity & ease"
    ).classes("text-xs text-gray-400 mt-4")

# =====================================================
# RUN APP
# =====================================================
ui.run(
    title="RailPulse",
    port=9000,
    host="127.0.0.1"
)
