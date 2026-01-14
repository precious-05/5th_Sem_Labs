from nicegui import ui
import httpx
import pandas as pd

API_BASE = "https://world.openfoodfacts.org/api/v0/product/"

# =====================================================
# FETCH PRODUCT DATA
# =====================================================
def fetch_product_data(barcode):
    try:
        url = f"{API_BASE}{barcode}.json"
        with httpx.Client(timeout=15) as client:
            resp = client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") != 1:
                ui.notify("Product not found!", color="red")
                return None
            return data["product"]
    except Exception as e:
        ui.notify(f"Error fetching product: {e}", color="red")
        return None

# =====================================================
# TRANSFORM DATA
# =====================================================
def transform_product_data(prod):
    df = pd.DataFrame([{
        "Product Name": prod.get("product_name", "-"),
        "Brands": prod.get("brands", "-"),
        "Quantity": prod.get("quantity", "-"),
        "Categories": prod.get("categories", "-"),
        "Labels": prod.get("labels", "-"),
        "Ingredients": ", ".join([i.get("text", "-") for i in prod.get("ingredients", [])]) if prod.get("ingredients") else "-",
        "Nutriments": ", ".join([f"{k}: {v}" for k,v in prod.get("nutriments", {}).items()]) if prod.get("nutriments") else "-",
        "Countries": prod.get("countries", "-")
    }])
    return df

# =====================================================
# GUI & TABLE HELPERS
# =====================================================
def load_product():
    barcode = barcode_input.value.strip()
    if not barcode:
        ui.notify("Enter a barcode!", color="red")
        return
    product = fetch_product_data(barcode)
    if product:
        df = transform_product_data(product)
        table.rows = df.values.tolist()
        ui.notify("Product loaded ✅", color="green")

        # Store dataframe globally for CSV download
        global current_df
        current_df = df

def download_csv():
    if current_df is None:
        ui.notify("No data to download!", color="red")
        return
    current_df.to_csv("product_data.csv", index=False)
    ui.notify("CSV saved as product_data.csv ✅", color="green")

# =====================================================
# UI PAGE
# =====================================================
current_df = None

@ui.page("/")
def main():
    ui.label("🍎 FoodFacts Explorer").classes("text-3xl font-bold")
    ui.label("Fetch product info by barcode and export CSV").classes("text-gray-500")
    ui.separator()

    with ui.card().classes("w-full p-4 shadow-lg bg-gradient-to-r from-green-100 via-yellow-100 to-pink-100 rounded-xl"):
        ui.label("Enter Barcode:").classes("font-semibold")
        with ui.row():
            global barcode_input
            barcode_input = ui.input(placeholder="e.g. 737628064502").classes("w-64")
            ui.button("Load Product", on_click=load_product, color="green")

        ui.button("Download CSV", on_click=download_csv, color="blue").classes("mt-2")

    ui.separator()

    global table
    table = ui.table(
        columns=[
            {"name": "name", "label": "Product Name"},
            {"name": "brands", "label": "Brands"},
            {"name": "quantity", "label": "Quantity"},
            {"name": "categories", "label": "Categories"},
            {"name": "labels", "label": "Labels"},
            {"name": "ingredients", "label": "Ingredients"},
            {"name": "nutriments", "label": "Nutriments"},
            {"name": "countries", "label": "Countries"},
        ],
        rows=[]
    ).classes("w-full mt-4")

    ui.label("Designed for clarity & easy CSV export").classes("text-xs text-gray-500 mt-2")

# =====================================================
# RUN APP
# =====================================================
ui.run(
    title="FoodFacts Explorer",
    port=9000,
    host="127.0.0.1"
)
