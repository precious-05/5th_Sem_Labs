from nicegui import ui
import httpx
import pandas as pd

# =====================================================
# CONFIG
# =====================================================
API_URL = "https://raw.githubusercontent.com/Hipo/university-domains-list/master/data/world_universities.json"


# =====================================================
# ETL - EXTRACT
# =====================================================
def extract_data():
    with httpx.Client(timeout=15) as client:
        response = client.get(API_URL)
        response.raise_for_status()
        return response.json()

# =====================================================
# ETL - TRANSFORM
# =====================================================
def transform_data(raw_data):
    df = pd.DataFrame(raw_data)

    df = df[["name", "country", "domains", "web_pages"]]

    df["domain_count"] = df["domains"].apply(len)
    df["name_lower"] = df["name"].str.lower()

    return df

# =====================================================
# ETL - LOAD (IN-MEMORY STORE)
# =====================================================
DATAFRAME = None

def run_etl():
    global DATAFRAME
    raw = extract_data()
    DATAFRAME = transform_data(raw)

# =====================================================
# UI HELPERS
# =====================================================
def update_table(df):
    table.rows = df.apply(
        lambda r: [
            r["name"],
            r["country"],
            ", ".join(r["domains"]),
            r["domain_count"]
        ],
        axis=1
    ).tolist()

def apply_filters():
    df = DATAFRAME.copy()

    # Country filter
    if country_select.value != "All":
        df = df[df["country"] == country_select.value]

    # Search
    if search_input.value:
        df = df[df["name_lower"].str.contains(search_input.value.lower())]

    # Sort
    if sort_select.value == "Domain Count (High → Low)":
        df = df.sort_values("domain_count", ascending=False)
    elif sort_select.value == "Domain Count (Low → High)":
        df = df.sort_values("domain_count", ascending=True)

    update_table(df)

# =====================================================
# UI PAGE
# =====================================================
@ui.page("/")
def main():
    ui.label("🎓 University ETL Explorer").classes("text-2xl font-bold")

    ui.separator()

    with ui.row():
        ui.label("Search University:")
        global search_input
        search_input = ui.input(placeholder="e.g. harvard").on("input", lambda _: apply_filters())

    with ui.row():
        ui.label("Country:")
        global country_select
        country_select = ui.select(["All"], value="All").on("change", lambda _: apply_filters())

        global sort_select
        sort_select = ui.select(
            [
                "None",
                "Domain Count (High → Low)",
                "Domain Count (Low → High)"
            ],
            value="None"
        ).on("change", lambda _: apply_filters())

    ui.separator()

    global table
    table = ui.table(
        columns=[
            {"name": "Name", "label": "University Name", "field": "name"},
            {"name": "Country", "label": "Country", "field": "country"},
            {"name": "Domains", "label": "Domains", "field": "domains"},
            {"name": "Count", "label": "Domain Count", "field": "count"},
        ],
        rows=[]
    ).classes("w-full")

    ui.notify("Running ETL process...", color="blue")

    # RUN ETL
    run_etl()

    # Populate country dropdown
    countries = sorted(DATAFRAME["country"].unique())
    country_select.set_options(["All"] + countries)

    update_table(DATAFRAME)

    ui.notify("ETL Completed Successfully ✅", color="green")

# =====================================================
# ======================= RUN APP =====================
# =====================================================
ui.run(
    title="University ETL App",
    reload=True,
    port=9000,
    host="127.0.0.1"
)
