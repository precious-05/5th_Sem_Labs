from nicegui import ui
import httpx
import pandas as pd

# =====================================================
# CONFIG (LIVE API)
# =====================================================
API_URL = "http://universities.hipolabs.com/search"

# =====================================================
# ETL - EXTRACT
# =====================================================
def extract_data(name=None, country=None):
    params = {}
    if name:
        params["name"] = name
    if country and country != "All":
        params["country"] = country

    with httpx.Client(timeout=15) as client:
        response = client.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()

# =====================================================
# ETL - TRANSFORM
# =====================================================
def transform_data(raw):
    if not raw:
        return pd.DataFrame(columns=["name", "country", "domains", "web_pages", "domain_count"])

    df = pd.DataFrame(raw)
    df["domain_count"] = df["domains"].apply(len)
    df["name_lower"] = df["name"].str.lower()
    return df

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

def load_data():
    raw = extract_data(
        name=search_input.value,
        country=country_select.value
    )
    df = transform_data(raw)

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
    ui.label("🎓 Universities ETL Explorer").classes("text-2xl font-bold")
    ui.separator()

    with ui.row():
        global search_input
        search_input = ui.input(
            placeholder="Search university name (e.g. Harvard)"
        )

        global country_select
        country_select = ui.input(
            placeholder="Country (optional, e.g. United States)"
        )

        global sort_select
        sort_select = ui.select(
            ["None", "Domain Count (High → Low)", "Domain Count (Low → High)"],
            value="None"
        )

        ui.button("Search", on_click=load_data)

    ui.separator()

    global table
    table = ui.table(
        columns=[
            {"name": "name", "label": "University"},
            {"name": "country", "label": "Country"},
            {"name": "domains", "label": "Domains"},
            {"name": "count", "label": "Domain Count"},
        ],
        rows=[]
    ).classes("w-full")

    ui.notify("Ready ✅ Use search to load data", color="green")

# =====================================================
# RUN
# =====================================================
ui.run(
    title="University ETL App",
    port=9000,
    host="127.0.0.1"
)
