from nicegui import ui
import httpx
import pandas as pd

# =====================================================
# CONFIG
# =====================================================
API_URL = "https://www.amiiboapi.com/api/amiibo/"

# =====================================================
# ETL - EXTRACT
# =====================================================
def extract_data(name=None):
    params = {}
    if name:
        params["name"] = name

    with httpx.Client(timeout=15) as client:
        response = client.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()["amiibo"]

# =====================================================
# ETL - TRANSFORM
# =====================================================
def transform_data(raw):
    df = pd.DataFrame(raw)

    df = df[[
        "name",
        "character",
        "amiiboSeries",
        "gameSeries",
        "type",
        "release"
    ]]

    # Extract NA release date safely
    df["release_na"] = df["release"].apply(
        lambda r: r.get("na") if isinstance(r, dict) else "N/A"
    )

    df.drop(columns=["release"], inplace=True)

    return df

# =====================================================
# UI HELPERS
# =====================================================
def update_table(df):
    table.rows = df.apply(
        lambda r: [
            r["name"],
            r["character"],
            r["gameSeries"],
            r["amiiboSeries"],
            r["type"],
            r["release_na"]
        ],
        axis=1
    ).tolist()

def load_data():
    ui.notify("Running ETL...", color="blue")

    raw = extract_data(search_input.value)
    df = transform_data(raw)

    # Filter by game series
    if game_series_select.value != "All":
        df = df[df["gameSeries"] == game_series_select.value]

    update_table(df)

    # Populate dropdown once
    series = sorted(df["gameSeries"].dropna().unique())
    game_series_select.set_options(["All"] + series)

    ui.notify("ETL Completed ✅", color="green")

# =====================================================
# UI PAGE
# =====================================================
@ui.page("/")
def main():
    ui.label("🎮 Amiibo ETL Explorer").classes("text-2xl font-bold")
    ui.label("Search & explore Nintendo Amiibo figures").classes("text-gray-500")

    ui.separator()

    with ui.row():
        global search_input
        search_input = ui.input(
            placeholder="Search amiibo (e.g. mario, zelda)"
        )

        global game_series_select
        game_series_select = ui.select(
            ["All"],
            value="All"
        )

        ui.button("Search", on_click=load_data)

    ui.separator()

    global table
    table = ui.table(
        columns=[
            {"name": "name", "label": "Amiibo Name"},
            {"name": "character", "label": "Character"},
            {"name": "game", "label": "Game Series"},
            {"name": "series", "label": "Amiibo Series"},
            {"name": "type", "label": "Type"},
            {"name": "date", "label": "NA Release"},
        ],
        rows=[]
    ).classes("w-full")

    ui.notify("Ready 🎉 Start searching!", color="green")

# =====================================================
# RUN APP
# =====================================================
ui.run(
    title="Amiibo ETL App",
    port=9000,
    host="127.0.0.1"
)
