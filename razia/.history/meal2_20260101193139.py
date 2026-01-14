import requests
import pandas as pd
import os
from nicegui import ui

class MealETL:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
    
    def get_data(self):
        # Single API endpoint - Seafood category
        response = requests.get(f"{self.base_url}/filter.php?c=Seafood")
        return response.json() if response.ok else {}
    
    def clean_data(self, data):
        meals = []
        
        if data and "meals" in data:
            for meal in data["meals"][:4]:  # Get first 4 meals
                # Get full details
                detail = requests.get(f"{self.base_url}/lookup.php?i={meal['idMeal']}")
                if detail.ok:
                    detail_data = detail.json()
                    if detail_data and "meals" in detail_data:
                        cleaned = self._clean_single_meal(detail_data["meals"][0])
                        meals.append(cleaned)
        
        return meals
    
    def _clean_single_meal(self, meal):
        ingredients = []
        for i in range(1, 11):  # First 10 ingredients
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
            
            if os.path.exists(path):
                old_df = pd.read_csv(path)
                df = pd.concat([old_df, df]).drop_duplicates(subset=['id'])
            
            df.to_csv(path, index=False)
            return path, len(meals)
        
        return path, 0

class MealApp:
    def __init__(self):
        self.etl = MealETL()
        self.meals = []
        self.csv_path = "meal_data"
        
        # Create folder if not exists
        if not os.path.exists(self.csv_path):
            os.makedirs(self.csv_path)
        
        # Load existing data
        self.load_data()
    
    def load_data(self):
        file_path = os.path.join(self.csv_path, "meals.csv")
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                self.meals = df.to_dict('records')
            except:
                self.meals = []
    
    def create_ui(self):
        # Header
        with ui.header().classes('bg-blue-600 text-white'):
            with ui.row().classes('items-center w-full'):
                ui.label('Meal Finder App').classes('text-2xl font-bold')
        
        # Main content
        with ui.row().classes('w-full p-4'):
            # Left panel - Controls
            with ui.column().classes('w-1/4 p-4'):
                ui.label('ETL Controls').classes('text-xl font-bold mb-4')
                
                # ETL Button
                self.etl_btn = ui.button('Run ETL Process', on_click=self.do_etl)
                self.etl_btn.props('color=primary').classes('w-full')
                
                # Stats
                ui.separator()
                self.stats_label = ui.label(f'Total Meals: {len(self.meals)}')
                
                # Info
                ui.separator()
                ui.label('About ETL:')
                ui.label('1. Extract from API')
                ui.label('2. Transform data')
                ui.label('3. Load to CSV')
            
            # Right panel - Meals display
            with ui.column().classes('w-3/4 p-4'):
                # Search
                with ui.row().classes('w-full mb-4'):
                    self.search_input = ui.input(
                        placeholder='Search meals...',
                        on_change=self.filter_meals
                    ).classes('w-64')
                
                # Meals grid
                self.meals_container = ui.column().classes('w-full')
                self.display_meals()
    
    def do_etl(self):
        try:
            # Show loading
            with ui.dialog() as dialog, ui.card():
                ui.label('Running ETL Process...')
            
            dialog.open()
            
            # ETL Process
            raw_data = self.etl.get_data()
            clean_meals = self.etl.clean_data(raw_data)
            
            # Save to CSV
            path, count = self.etl.save_csv(clean_meals, self.csv_path)
            
            # Reload data
            self.load_data()
            
            # Update UI
            self.display_meals()
            self.stats_label.text = f'Total Meals: {len(self.meals)}'
            
            dialog.close()
            
            # Show success
            ui.notify(f'ETL Complete: Added {count} meals')
            
        except Exception as e:
            ui.notify(f'Error: {str(e)}', type='negative')
    
    def display_meals(self):
        self.meals_container.clear()
        
        if not self.meals:
            with self.meals_container:
                ui.label('No meals available. Run ETL first.')
            return
        
        with self.meals_container:
            with ui.grid(columns=2).classes('w-full gap-4'):
                for meal in self.meals:
                    self.create_meal_card(meal)
    
    def create_meal_card(self, meal):
        with ui.card().classes('w-full'):
            # Meal image
            if meal.get('image'):
                ui.image(meal['image']).classes('w-full h-48 object-cover')
            
            # Meal info
            with ui.column().classes('p-2'):
                ui.label(meal.get('name', '')).classes('text-lg font-bold')
                
                with ui.row().classes('text-sm text-gray-600'):
                    ui.label(meal.get('category', ''))
                    ui.label('|')
                    ui.label(meal.get('area', ''))
                
                # Ingredients preview
                ingredients = meal.get('ingredients', '')
                if len(ingredients) > 40:
                    ingredients = ingredients[:37] + '...'
                ui.label(f'Ingredients: {ingredients}').classes('text-sm mt-2')
                
                # View button
                ui.button('View Details', on_click=lambda m=meal: self.show_details(m))
    
    def filter_meals(self):
        query = self.search_input.value.lower() if self.search_input.value else ''
        
        self.meals_container.clear()
        
        if not query:
            self.display_meals()
            return
        
        filtered = []
        for meal in self.meals:
            if (query in meal.get('name', '').lower() or 
                query in meal.get('category', '').lower()):
                filtered.append(meal)
        
        if not filtered:
            with self.meals_container:
                ui.label('No meals found')
            return
        
        with self.meals_container:
            with ui.grid(columns=2).classes('w-full gap-4'):
                for meal in filtered:
                    self.create_meal_card(meal)
    
    def show_details(self, meal):
        with ui.dialog() as dialog, ui.card().classes('p-4 w-96'):
            # Header
            ui.label(meal.get('name', '')).classes('text-xl font-bold mb-2')
            
            # Category and area
            with ui.row().classes('text-sm mb-4'):
                ui.label(f"Category: {meal.get('category', '')}")
                ui.label('|')
                ui.label(f"Area: {meal.get('area', '')}")
            
            # Ingredients
            ui.label('Ingredients:').classes('font-bold')
            ingredients = meal.get('ingredients', '').split(', ')
            for ing in ingredients:
                ui.label(f'• {ing}')
            
            # Instructions
            ui.label('Instructions:').classes('font-bold mt-4')
            ui.html(f'<div class="max-h-40 overflow-y-auto p-2 border rounded">{meal.get("instructions", "")}</div>')
            
            # Close button
            ui.button('Close', on_click=dialog.close)

# Main application
@ui.page('/')
def main_page():
    app = MealApp()
    app.create_ui()

# Run the app
if __name__ == "__main__":
    ui.run(title="Meal Finder", port=8081)