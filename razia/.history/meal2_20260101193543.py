import requests
import pandas as pd
import os
from nicegui import ui

class MealETL:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
    
    def get_data(self):
        try:
            response = requests.get(f"{self.base_url}/filter.php?c=Seafood", timeout=10)
            return response.json() if response.ok else {}
        except:
            return {}
    
    def clean_data(self, data):
        meals = []
        
        if data and "meals" in data:
            for meal in data["meals"][:4]:
                try:
                    detail = requests.get(f"{self.base_url}/lookup.php?i={meal['idMeal']}", timeout=10)
                    if detail.ok:
                        detail_data = detail.json()
                        if detail_data and "meals" in detail_data:
                            cleaned = self._clean_single_meal(detail_data["meals"][0])
                            meals.append(cleaned)
                except:
                    continue
        
        return meals
    
    def _clean_single_meal(self, meal):
        ingredients = []
        for i in range(1, 11):
            ing = meal.get(f"strIngredient{i}", "").strip()
            measure = meal.get(f"strMeasure{i}", "").strip()
            if ing and ing.lower() != "null":
                ingredients.append(f"{measure} {ing}".strip())
        
        instructions = meal.get("strInstructions", "")
        if len(instructions) > 200:
            instructions = instructions[:197] + "..."
        
        return {
            "id": meal.get("idMeal", ""),
            "name": meal.get("strMeal", "").strip(),
            "category": meal.get("strCategory", "").strip(),
            "area": meal.get("strArea", "").strip(),
            "instructions": instructions,
            "image": meal.get("strMealThumb", ""),
            "ingredients": ", ".join(ingredients[:3])
        }
    
    def save_csv(self, meals, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        path = os.path.join(folder, "meals.csv")
        
        if meals:
            df = pd.DataFrame(meals)
            
            if os.path.exists(path) and os.path.getsize(path) > 0:
                old_df = pd.read_csv(path)
                df = pd.concat([old_df, df]).drop_duplicates(subset=['id'])
            
            df.to_csv(path, index=False)
            return path, len(meals)
        
        return path, 0

# Create main app instance
app = MealETL()
meals_data = []
csv_path = "meal_data"

# Create folder if not exists
if not os.path.exists(csv_path):
    os.makedirs(csv_path)

# Load existing data
def load_existing_data():
    global meals_data
    file_path = os.path.join(csv_path, "meals.csv")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            meals_data = df.to_dict('records')
        except:
            meals_data = []

load_existing_data()

# Create UI
@ui.page('/')
def create_ui():
    # Header
    with ui.header().style('background-color: #1e40af; color: white'):
        with ui.row().classes('items-center w-full justify-center'):
            ui.label('Meal Finder Application').style('font-size: 24px; font-weight: bold')
    
    # Main content
    with ui.row().classes('w-full p-4 gap-4'):
        # Left panel - Controls
        with ui.column().classes('w-1/4'):
            # ETL Section
            with ui.card().classes('w-full p-4'):
                ui.label('ETL Controls').style('font-size: 18px; font-weight: bold; margin-bottom: 20px')
                
                # Run ETL button
                def run_etl_process():
                    try:
                        # Extract
                        raw_data = app.get_data()
                        
                        # Transform
                        clean_meals = app.clean_data(raw_data)
                        
                        # Load
                        path, count = app.save_csv(clean_meals, csv_path)
                        
                        # Reload data
                        load_existing_data()
                        
                        # Update UI
                        display_meals()
                        stats_label.set_text(f'Total Meals: {len(meals_data)}')
                        
                        ui.notify(f'Success! Added {count} new meals', type='positive')
                        
                    except Exception as e:
                        ui.notify(f'Error: {str(e)}', type='negative')
                
                ui.button('Run ETL', on_click=run_etl_process).props('color=primary').classes('w-full mb-4')
                
                # Stats
                ui.separator()
                stats_label = ui.label(f'Total Meals: {len(meals_data)}')
                
                # Info
                ui.separator()
                ui.label('ETL Process:')
                ui.label('1. Extract from API')
                ui.label('2. Transform data')
                ui.label('3. Load to CSV')
        
        # Right panel - Meals display
        with ui.column().classes('w-3/4'):
            # Search bar
            with ui.row().classes('w-full mb-4 items-center'):
                ui.label('Search:')
                search_input = ui.input(
                    placeholder='Enter meal name or category...',
                    on_change=lambda e: filter_meals(e.value)
                ).classes('w-64 ml-2')
            
            # Meals container
            meals_container = ui.column().classes('w-full')
            
            def display_meals():
                meals_container.clear()
                
                if not meals_data:
                    with meals_container:
                        ui.label('No meals available. Click "Run ETL" to fetch meals.')
                    return
                
                with meals_container:
                    with ui.grid(columns=2).classes('w-full gap-4'):
                        for meal in meals_data:
                            create_meal_card(meal)
            
            def create_meal_card(meal):
                with ui.card().classes('w-full'):
                    # Image
                    if meal.get('image'):
                        ui.image(meal['image']).classes('w-full h-48 object-cover')
                    
                    # Content
                    with ui.column().classes('p-2'):
                        ui.label(meal.get('name', '')).style('font-size: 16px; font-weight: bold')
                        
                        with ui.row().classes('text-gray-600 text-sm'):
                            ui.label(meal.get('category', ''))
                            ui.label('|')
                            ui.label(meal.get('area', ''))
                        
                        # Ingredients preview
                        ingredients = meal.get('ingredients', '')
                        if len(ingredients) > 40:
                            ingredients = ingredients[:37] + '...'
                        ui.label(f'Ingredients: {ingredients}').classes('text-sm mt-1')
                        
                        # View button
                        ui.button('View Details', on_click=lambda: show_meal_details(meal))
            
            def filter_meals(query):
                meals_container.clear()
                
                if not query:
                    display_meals()
                    return
                
                query = query.lower()
                filtered = []
                for meal in meals_data:
                    if (query in meal.get('name', '').lower() or 
                        query in meal.get('category', '').lower()):
                        filtered.append(meal)
                
                if not filtered:
                    with meals_container:
                        ui.label('No meals found')
                    return
                
                with meals_container:
                    with ui.grid(columns=2).classes('w-full gap-4'):
                        for meal in filtered:
                            create_meal_card(meal)
            
            def show_meal_details(meal):
                with ui.dialog() as dialog, ui.card().classes('p-4'):
                    # Title
                    ui.label(meal.get('name', '')).style('font-size: 20px; font-weight: bold')
                    
                    # Info
                    with ui.row().classes('text-gray-600 mb-3'):
                        ui.label(f"Category: {meal.get('category', '')}")
                        ui.label('|')
                        ui.label(f"Area: {meal.get('area', '')}")
                    
                    # Ingredients
                    ui.label('Ingredients:').style('font-weight: bold')
                    ingredients = meal.get('ingredients', '').split(', ')
                    for ing in ingredients:
                        ui.label(f'• {ing}')
                    
                    # Instructions
                    ui.label('Instructions:').style('font-weight: bold; margin-top: 10px')
                    instructions = meal.get('instructions', '')
                    with ui.column().classes('border rounded p-2 max-h-48 overflow-y-auto'):
                        ui.label(instructions)
                    
                    # Close button
                    ui.button('Close', on_click=dialog.close)
            
            # Display initial meals
            display_meals()

# Run the app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Meal Finder", port=8082, reload=False)