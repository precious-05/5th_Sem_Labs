"""
Simple Meal Finder App
3 API endpoints + ETL + NiceGUI
User specifies CSV save path
Clean and simple
"""

import requests
import pandas as pd
import os
from nicegui import ui

# ========== ETL CLASS ==========
class MealETL:
    """ETL with 3 API endpoints"""
    
    def __init__(self, csv_folder="meal_data"):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
        self.csv_folder = csv_folder
        
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)
    
    def get_data(self):
        """Get data from 3 APIs"""
        data = {}
        
        # 1. Random meal
        random_data = self._api_call("/random.php")
        data["random"] = random_data
        
        # 2. Categories
        cat_data = self._api_call("/categories.php")
        data["categories"] = cat_data
        
        # 3. Chicken meals
        chicken_data = self._api_call("/filter.php?i=chicken")
        data["chicken"] = chicken_data
        
        return data
    
    def _api_call(self, endpoint):
        """Simple API call"""
        try:
            response = requests.get(self.base_url + endpoint, timeout=5)
            return response.json() if response.ok else {}
        except:
            return {}
    
    def clean_data(self, data):
        """Clean the data"""
        meals = []
        
        # Random meal
        if data["random"] and "meals" in data["random"]:
            for meal in data["random"]["meals"]:
                meals.append(self._clean_meal(meal))
        
        # Chicken meals
        if data["chicken"] and "meals" in data["chicken"]:
            for meal in data["chicken"]["meals"][:3]:
                full = self._api_call(f"/lookup.php?i={meal['idMeal']}")
                if full and "meals" in full:
                    meals.append(self._clean_meal(full["meals"][0]))
        
        return meals
    
    def _clean_meal(self, meal):
        """Clean single meal"""
        ingredients = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}", "").strip()
            measure = meal.get(f"strMeasure{i}", "").strip()
            if ing and ing.lower() != "null":
                ingredients.append(f"{measure} {ing}".strip())
        
        return {
            "id": meal.get("idMeal", ""),
            "name": meal.get("strMeal", "").strip(),
            "category": meal.get("strCategory", "").strip(),
            "area": meal.get("strArea", "").strip(),
            "instructions": meal.get("strInstructions", "")[:150],
            "image": meal.get("strMealThumb", ""),
            "ingredients": ", ".join(ingredients[:5]),
            "youtube": meal.get("strYoutube", "")
        }
    
    def save_csv(self, meals, folder=None):
        """Save to CSV"""
        save_folder = folder if folder else self.csv_folder
        
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        path = os.path.join(save_folder, "meals.csv")
        
        if meals:
            df = pd.DataFrame(meals)
            
            if os.path.exists(path):
                old_df = pd.read_csv(path)
                df = pd.concat([old_df, df]).drop_duplicates(subset=['id'])
            
            df.to_csv(path, index=False)
            return path, len(meals)
        
        return path, 0

# ========== APP CLASS ==========
class MealApp:
    """Main app class"""
    
    def __init__(self):
        self.etl = MealETL()
        self.meals = []
        self.csv_path = "meal_data"
        
        # Make tabs available globally
        self.tabs = None
        self.meals_tab = None
        self.home_tab = None
    
    def run(self):
        """Run the app"""
        # Header
        with ui.header():
            with ui.row().classes('items-center w-full'):
                ui.label("Meal Finder App").classes('text-xl font-bold')
                ui.space()
                
                with ui.row():
                    ui.label("Save to:").classes('mr-2')
                    self.path_input = ui.input(
                        value=self.csv_path,
                        on_change=lambda e: setattr(self, 'csv_path', e.value)
                    ).classes('w-40')
        
        # Create tabs
        with ui.tabs() as self.tabs:
            self.home_tab = ui.tab('Home')
            self.meals_tab = ui.tab('Browse Meals')
            ui.tab('Search')
            ui.tab('Settings')
        
        # Tab panels
        with ui.tab_panels(self.tabs, value=self.home_tab).classes('w-full'):
            # Home
            with ui.tab_panel(self.home_tab):
                self.make_home()
            
            # Meals
            with ui.tab_panel(self.meals_tab):
                self.make_meals_tab()
            
            # Search
            with ui.tab_panel('Search'):
                self.make_search_tab()
            
            # Settings
            with ui.tab_panel('Settings'):
                self.make_settings_tab()
        
        # Load data
        self.load_data()
    
    def make_home(self):
        """Home page"""
        with ui.column().classes('p-8'):
            ui.label("Welcome to Meal Finder").classes('text-2xl font-bold mb-4')
            ui.label("Simple app to find and save meals").classes('mb-8')
            
            with ui.row().classes('gap-6'):
                # ETL box
                with ui.card():
                    ui.label("ETL Process").classes('font-bold mb-2')
                    ui.label("Get data from API and save to CSV").classes('mb-4')
                    ui.button("Run ETL", on_click=self.do_etl).props('color=primary')
                
                # View box
                with ui.card():
                    ui.label("View Meals").classes('font-bold mb-2')
                    ui.label(f"Loaded: {len(self.meals)} meals").classes('mb-4')
                    ui.button("Browse", on_click=lambda: self.tabs.set_value(self.meals_tab))
    
    def make_meals_tab(self):
        """Meals browsing"""
        with ui.column().classes('p-4'):
            ui.label("Browse Meals").classes('text-xl font-bold mb-4')
            
            # Search box
            with ui.row().classes('mb-4'):
                self.search_box = ui.input(
                    placeholder="Search meals...",
                    on_change=self.search_meals
                ).classes('w-64')
            
            # Meals container
            self.meals_display = ui.column().classes('w-full')
            
            self.show_all_meals()
    
    def make_search_tab(self):
        """Search page"""
        with ui.column().classes('p-4'):
            ui.label("Search API").classes('text-xl font-bold mb-4')
            
            with ui.row().classes('mb-4'):
                self.api_search = ui.input(placeholder="Enter meal name...")
                ui.button("Search", on_click=self.search_api)
            
            self.api_results = ui.column().classes('w-full')
    
    def make_settings_tab(self):
        """Settings page"""
        with ui.column().classes('p-4'):
            ui.label("Settings").classes('text-xl font-bold mb-4')
            
            with ui.card():
                ui.label("CSV Path").classes('font-bold mb-2')
                
                with ui.row().classes('items-center mb-4'):
                    self.settings_path = ui.input(value=self.csv_path)
                    ui.button("Update", on_click=self.update_path)
                
                # File info
                file_path = os.path.join(self.csv_path, "meals.csv")
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path) / 1024
                    ui.label(f"meals.csv: {size:.1f} KB").classes('text-green')
                else:
                    ui.label("No CSV file yet").classes('text-gray')
    
    def load_data(self):
        """Load existing CSV data"""
        file_path = os.path.join(self.csv_path, "meals.csv")
        
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                self.meals = df.to_dict('records')
                ui.notify(f"Loaded {len(self.meals)} meals")
            except:
                ui.notify("Error loading CSV")
    
    def update_path(self):
        """Update CSV path"""
        new_path = self.settings_path.value
        if new_path:
            self.csv_path = new_path
            self.path_input.value = new_path
            
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            
            self.load_data()
            ui.notify(f"Path updated to: {new_path}")
    
    def do_etl(self):
        """Run ETL process"""
        # Show loading
        with ui.dialog() as dialog, ui.card():
            ui.label("Running ETL...")
        
        dialog.open()
        
        try:
            # Extract
            raw = self.etl.get_data()
            
            # Transform
            clean_meals = self.etl.clean_data(raw)
            
            # Load
            path, count = self.etl.save_csv(clean_meals, self.csv_path)
            
            # Update data
            self.load_data()
            
            dialog.close()
            
            # Show success
            with ui.dialog() as success, ui.card():
                ui.label("Success!").classes('text-green font-bold')
                ui.label(f"Saved {count} meals")
                ui.label(f"to: {path}")
                ui.button("OK", on_click=success.close)
            
            success.open()
            
        except Exception as e:
            dialog.close()
            ui.notify(f"Error: {str(e)}", type='negative')
    
    def show_all_meals(self):
        """Show all meals"""
        self.meals_display.clear()
        
        if not self.meals:
            with self.meals_display:
                ui.label("No meals found").classes('text-gray')
            return
        
        for meal in self.meals[:12]:
            with self.meals_display:
                self.show_meal_card(meal)
    
    def show_meal_card(self, meal):
        """Show single meal card"""
        with ui.card().classes('w-64'):
            # Image
            if meal.get("image"):
                ui.image(meal["image"]).classes('w-full h-40')
            
            # Info
            with ui.column().classes('p-2'):
                ui.label(meal.get("name", "")).classes('font-bold truncate')
                
                with ui.row().classes('text-sm'):
                    ui.label(meal.get("category", ""))
                    ui.label("•")
                    ui.label(meal.get("area", ""))
                
                # View button
                ui.button("Details", 
                         on_click=lambda m=meal: self.show_details(m)).props('flat')
    
    def search_meals(self):
        """Search loaded meals"""
        query = self.search_box.value.lower() if self.search_box.value else ""
        
        self.meals_display.clear()
        
        if not query:
            self.show_all_meals()
            return
        
        found = []
        for meal in self.meals:
            if (query in meal.get("name", "").lower() or 
                query in meal.get("category", "").lower()):
                found.append(meal)
        
        if not found:
            with self.meals_display:
                ui.label("No meals found")
            return
        
        for meal in found[:10]:
            with self.meals_display:
                self.show_meal_card(meal)
    
    def search_api(self):
        """Search API directly"""
        query = self.api_search.value
        if not query:
            ui.notify("Enter search term")
            return
        
        self.api_results.clear()
        
        with self.api_results:
            ui.label(f"Searching for: {query}...")
        
        try:
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            self.api_results.clear()
            
            if data and "meals" in data:
                with self.api_results:
                    for meal in data["meals"][:5]:
                        clean = self.etl._clean_meal(meal)
                        
                        with ui.card().classes('mb-2'):
                            with ui.row().classes('items-center'):
                                if clean.get("image"):
                                    ui.image(clean["image"]).classes('w-12 h-12')
                                
                                with ui.column():
                                    ui.label(clean.get("name", ""))
                                    ui.label(clean.get("category", "")).classes('text-sm')
                                
                                ui.button("Save", 
                                         on_click=lambda m=clean: self.save_meal(m)).props('small')
            else:
                with self.api_results:
                    ui.label("No results found")
                    
        except:
            with self.api_results:
                ui.label("Search failed")
    
    def save_meal(self, meal):
        """Save single meal to CSV"""
        try:
            # Add to current meals
            self.meals.append(meal)
            
            # Save to CSV
            df = pd.DataFrame([meal])
            path = os.path.join(self.csv_path, "meals.csv")
            
            if os.path.exists(path):
                old = pd.read_csv(path)
                df = pd.concat([old, df]).drop_duplicates(subset=['id'])
            
            df.to_csv(path, index=False)
            
            ui.notify(f"Saved: {meal['name']}")
            
        except Exception as e:
            ui.notify(f"Save error: {str(e)}", type='negative')
    
    def show_details(self, meal):
        """Show meal details"""
        with ui.dialog() as dialog, ui.card().classes('p-4'):
            # Header
            with ui.row().classes('items-start'):
                if meal.get("image"):
                    ui.image(meal["image"]).classes('w-32 h-32')
                
                with ui.column().classes('ml-4'):
                    ui.label(meal.get("name", "")).classes('text-xl font-bold')
                    ui.label(f"{meal.get('category')} - {meal.get('area')}").classes('text-gray')
            
            # Ingredients
            ui.label("Ingredients:").classes('font-bold mt-4')
            ings = meal.get("ingredients", "").split(", ")
            for ing in ings[:8]:
                ui.label(f"• {ing}")
            
            # Instructions
            ui.label("Instructions:").classes('font-bold mt-4')
            ui.markdown(meal.get("instructions", "")[:200])
            
            # Save button
            ui.button("Save to CSV", 
                     on_click=lambda: [self.save_meal(meal), dialog.close()]).props('color=primary').classes('mt-4')
            
            # Close
            ui.button("Close", on_click=dialog.close)
        
        dialog.open()

# ========== RUN APP ==========
def main():
    """Start app"""
    app = MealApp()
    app.run()
    
    # Run on port 8081
    ui.run(
        title="Meal Finder",
        port=8081,
        reload=False
    )

if __name__ == "__main__":
    main()