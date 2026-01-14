"""
Simple Meal Finder App
3 API endpoints + ETL + NiceGUI
Beginners ke liye perfect!
"""

import requests
import pandas as pd
from nicegui import ui

# ========== SIMPLE ETL CLASS ==========
class SimpleMealETL:
    """ETL class jo 3 API endpoints use karega"""
    
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
        
    # 1. EXTRACT - 3 simple endpoints
    def extract_data(self):
        """3 APIs se data extract karo"""
        print("Extracting data from 3 APIs...")
        
        # Endpoint 1: Random meal (always fresh data)
        print("1. Fetching random meal...")
        random_meal = self._fetch_api("/random.php")
        
        # Endpoint 2: Categories list
        print("2. Fetching categories...")
        categories = self._fetch_api("/categories.php")
        
        # Endpoint 3: Search chicken meals (example)
        print("3. Searching chicken meals...")
        chicken_meals = self._fetch_api("/filter.php?i=chicken")
        
        return {
            "random_meal": random_meal,
            "categories": categories,
            "chicken_meals": chicken_meals
        }
    
    def _fetch_api(self, endpoint):
        """Simple API call"""
        try:
            response = requests.get(self.base_url + endpoint, timeout=5)
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    # 2. TRANSFORM - Simple cleaning
    def transform_data(self, data):
        """Data ko clean aur simple banaye"""
        print("Transforming data...")
        
        meals_list = []
        
        # Random meal ko add karo
        if data["random_meal"] and "meals" in data["random_meal"]:
            for meal in data["random_meal"]["meals"]:
                clean_meal = self._clean_meal(meal)
                meals_list.append(clean_meal)
        
        # Chicken meals ko add karo
        if data["chicken_meals"] and "meals" in data["chicken_meals"]:
            for meal in data["chicken_meals"]["meals"][:3]:  # Sirf 3
                # Chicken meals mein full details nahi hote, isliye ID se fetch karte hain
                full_meal = self._fetch_api(f"/lookup.php?i={meal['idMeal']}")
                if full_meal and "meals" in full_meal:
                    clean_meal = self._clean_meal(full_meal["meals"][0])
                    meals_list.append(clean_meal)
        
        # Categories ko alag se transform karo
        categories_list = []
        if data["categories"] and "categories" in data["categories"]:
            for cat in data["categories"]["categories"][:5]:  # Sirf 5 categories
                categories_list.append({
                    "name": cat.get("strCategory", ""),
                    "description": cat.get("strCategoryDescription", "")[:100] + "..."
                })
        
        return {
            "meals": meals_list,
            "categories": categories_list
        }
    
    def _clean_meal(self, meal):
        """Single meal ko clean karo"""
        # Ingredients list banaye
        ingredients = []
        for i in range(1, 21):  # Max 20 ingredients
            ing = meal.get(f"strIngredient{i}", "").strip()
            measure = meal.get(f"strMeasure{i}", "").strip()
            if ing and ing.lower() != "null":
                ingredients.append(f"{measure} {ing}" if measure else ing)
        
        return {
            "id": meal.get("idMeal", ""),
            "name": meal.get("strMeal", "Unknown Meal").strip(),
            "category": meal.get("strCategory", "Unknown").strip(),
            "area": meal.get("strArea", "Unknown").strip(),
            "instructions": meal.get("strInstructions", "")[:200] + "...",
            "image": meal.get("strMealThumb", ""),
            "ingredients": ", ".join(ingredients[:5]),  # Sirf 5 ingredients
            "youtube": meal.get("strYoutube", "")
        }
    
    # 3. LOAD - CSV mein save karo
    def load_to_csv(self, data):
        """Data ko CSV files mein save karo"""
        print("Loading to CSV...")
        
        # Meals CSV
        if data["meals"]:
            df_meals = pd.DataFrame(data["meals"])
            df_meals.to_csv("simple_meals.csv", index=False)
            print(f"✓ {len(data['meals'])} meals saved to simple_meals.csv")
        
        # Categories CSV
        if data["categories"]:
            df_cats = pd.DataFrame(data["categories"])
            df_cats.to_csv("simple_categories.csv", index=False)
            print(f"✓ {len(data['categories'])} categories saved to simple_categories.csv")
        
        return len(data["meals"]), len(data["categories"])

# ========== SIMPLE UI ==========
class SimpleMealApp:
    """Simple NiceGUI app beginners ke liye"""
    
    def __init__(self):
        self.etl = SimpleMealETL()
        self.meals = []
        self.categories = []
    
    def run(self):
        """App run karo"""
        # Header
        with ui.header().style("background-color: #4CAF50; color: white;"):
            ui.label("🍔 Simple Meal Finder").style("font-size: 24px; font-weight: bold;")
            ui.space()
            ui.button("🔄 Run ETL", on_click=self.run_etl).props("color=white flat")
        
        # Main content - 3 sections
        with ui.tabs().style("width: 100%;") as tabs:
            home_tab = ui.tab("🏠 Home")
            meals_tab = ui.tab("🍽️ Meals")
            search_tab = ui.tab("🔍 Search")
        
        with ui.tab_panels(tabs, value=home_tab).style("width: 100%;"):
            
            # Tab 1: Home
            with ui.tab_panel(home_tab):
                self.create_home_tab()
            
            # Tab 2: Meals
            with ui.tab_panel(meals_tab):
                self.create_meals_tab()
            
            # Tab 3: Search
            with ui.tab_panel(search_tab):
                self.create_search_tab()
        
        # Startup par ETL run karo
        ui.timer(0.5, self.run_startup_etl, once=True)
    
    def create_home_tab(self):
        """Home page banaye"""
        with ui.column().style("padding: 20px;"):
            ui.label("Welcome to Simple Meal Finder!").style("font-size: 28px; color: #4CAF50; margin-bottom: 20px;")
            
            with ui.card().style("padding: 20px; background-color: #f9f9f9;"):
                ui.label("📊 About This App").style("font-size: 20px; font-weight: bold; color: #333;")
                ui.label("This is a beginner-friendly app that:")
                ui.label("• Uses only 3 API endpoints")
                ui.label("• Performs simple ETL (Extract, Transform, Load)")
                ui.label("• Stores data in CSV files")
                ui.label("• Has a clean, simple UI")
            
            with ui.row().style("margin-top: 30px; gap: 20px;"):
                # ETL Button
                with ui.card().style("padding: 15px; text-align: center;"):
                    ui.icon("download", size="40px").style("color: #4CAF50;")
                    ui.label("Run ETL").style("font-weight: bold;")
                    ui.button("Start", on_click=self.run_etl).props("color=green")
                
                # View Meals Button
                with ui.card().style("padding: 15px; text-align: center;"):
                    ui.icon("restaurant", size="40px").style("color: #2196F3;")
                    ui.label("View Meals").style("font-weight: bold;")
                    ui.button("Browse", on_click=lambda: tabs.set_value(meals_tab)).props("color=blue")
    
    def create_meals_tab(self):
        """Meals display kare"""
        with ui.column().style("padding: 20px;") as self.meals_column:
            ui.label("🍽️ Available Meals").style("font-size: 24px; margin-bottom: 20px;")
            
            # Filters
            with ui.row().style("margin-bottom: 20px; gap: 10px;"):
                self.search_input = ui.input(
                    placeholder="Search meals...",
                    on_change=self.filter_meals
                ).style("width: 300px;")
                
                ui.select(
                    options=["All", "Beef", "Chicken", "Vegetarian", "Seafood", "Dessert"],
                    value="All",
                    on_change=self.filter_meals,
                    label="Category"
                ).style("width: 150px;")
            
            # Meals grid container
            self.meals_container = ui.column().style("display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;")
    
    def create_search_tab(self):
        """Search functionality"""
        with ui.column().style("padding: 20px;"):
            ui.label("🔍 Search Meals").style("font-size: 24px; margin-bottom: 20px;")
            
            # Search box
            with ui.row().style("margin-bottom: 30px;"):
                self.meal_search = ui.input(
                    placeholder="Enter meal name...",
                    on_change=self.perform_search
                ).props("outlined").style("width: 400px;")
                ui.button("Search", on_click=self.perform_search, icon="search").props("color=primary")
            
            # Search results
            self.search_results = ui.column().style("width: 100%;")
    
    def run_startup_etl(self):
        """Startup par ETL chalao agar CSV nahi hai"""
        try:
            # Check if CSV exists
            import os
            if not os.path.exists("simple_meals.csv"):
                self.run_etl()
            else:
                # Load existing data
                self.load_from_csv()
        except:
            pass
    
    def run_etl(self):
        """ETL pipeline chalao"""
        with ui.dialog() as dialog, ui.card().style("padding: 20px;"):
            ui.label("🔄 Running ETL Pipeline...").style("font-size: 18px; font-weight: bold;")
            ui.linear_progress().props("indeterminate")
            ui.label("Please wait...").style("margin-top: 10px;")
        
        dialog.open()
        
        # Step 1: Extract
        ui.notify("📥 Extracting data from API...")
        raw_data = self.etl.extract_data()
        
        # Step 2: Transform
        ui.notify("⚙️ Transforming data...")
        clean_data = self.etl.transform_data(raw_data)
        
        # Step 3: Load
        ui.notify("💾 Saving to CSV...")
        meal_count, cat_count = self.etl.load_to_csv(clean_data)
        
        # Store in memory
        self.meals = clean_data["meals"]
        self.categories = clean_data["categories"]
        
        # Update UI
        self.display_meals()
        
        dialog.close()
        ui.notify(f"✅ ETL Complete! {meal_count} meals and {cat_count} categories saved.")
    
    def load_from_csv(self):
        """CSV se data load karo"""
        try:
            # Load meals
            df = pd.read_csv("simple_meals.csv")
            self.meals = df.to_dict('records')
            
            # Load categories
            df_cats = pd.read_csv("simple_categories.csv")
            self.categories = df_cats.to_dict('records')
            
            # Display
            self.display_meals()
            
            ui.notify(f"✅ Loaded {len(self.meals)} meals from CSV")
        except:
            ui.notify("⚠️ No CSV found. Please run ETL first.")
    
    def display_meals(self, meals_to_show=None):
        """Meals ko display karo"""
        if meals_to_show is None:
            meals_to_show = self.meals
        
        self.meals_container.clear()
        
        if not meals_to_show:
            with self.meals_container:
                ui.label("No meals found. Run ETL first!").style("color: gray; text-align: center; padding: 40px;")
            return
        
        for meal in meals_to_show[:12]:  # Max 12 meals
            with self.meals_container:
                self.create_meal_card(meal)
    
    def create_meal_card(self, meal):
        """Single meal card banaye"""
        with ui.card().style("padding: 15px;"):
            # Meal image
            if meal.get("image"):
                ui.image(meal["image"]).style("width: 100%; height: 150px; object-fit: cover; border-radius: 8px;")
            else:
                ui.icon("restaurant", size="80px").style("color: #ddd; text-align: center; width: 100%; padding: 35px 0;")
            
            # Meal details
            ui.label(meal.get("name", "Unknown")).style("font-size: 18px; font-weight: bold; margin-top: 10px;")
            
            with ui.row().style("margin-top: 5px; color: #666;"):
                ui.icon("category", size="16px")
                ui.label(meal.get("category", "Unknown"))
                ui.icon("place", size="16px").style("margin-left: 10px;")
                ui.label(meal.get("area", "Unknown"))
            
            # Ingredients (short)
            ingredients = meal.get("ingredients", "")
            if len(ingredients) > 50:
                ingredients = ingredients[:50] + "..."
            ui.label(f"🧂 {ingredients}").style("font-size: 12px; color: #888; margin-top: 5px;")
            
            # View button
            ui.button("View Details", on_click=lambda m=meal: self.show_meal_details(m)).props("color=primary flat").style("width: 100%; margin-top: 10px;")
    
    def filter_meals(self):
        """Meals filter karo"""
        if not self.meals:
            return
        
        search_text = self.search_input.value.lower() if self.search_input.value else ""
        
        filtered = []
        for meal in self.meals:
            # Search in name
            if search_text and search_text not in meal.get("name", "").lower():
                continue
            
            # TODO: Category filter implement karna hai
            
            filtered.append(meal)
        
        self.display_meals(filtered if search_text else self.meals)
    
    def perform_search(self):
        """API se search karo"""
        search_term = self.meal_search.value
        if not search_term:
            return
        
        self.search_results.clear()
        
        with self.search_results:
            ui.label(f"Searching for '{search_term}'...").style("color: #666;")
        
        # Direct API search
        try:
            response = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={search_term}")
            data = response.json()
            
            self.search_results.clear()
            
            if data and "meals" in data:
                with self.search_results:
                    ui.label(f"Found {len(data['meals'])} results:").style("font-weight: bold; margin-bottom: 20px;")
                    
                    for meal in data["meals"][:5]:  # Max 5 results
                        clean_meal = self.etl._clean_meal(meal)
                        self.create_search_result(clean_meal)
            else:
                with self.search_results:
                    ui.label("No results found").style("color: red; padding: 20px;")
        except:
            with self.search_results:
                ui.label("Search failed. Check internet connection.").style("color: red; padding: 20px;")
    
    def create_search_result(self, meal):
        """Search result display karo"""
        with ui.card().style("padding: 15px; margin-bottom: 15px;"):
            with ui.row().style("align-items: center;"):
                if meal.get("image"):
                    ui.image(meal["image"]).style("width: 80px; height: 80px; object-fit: cover; border-radius: 8px;")
                
                with ui.column().style("margin-left: 15px;"):
                    ui.label(meal.get("name", "")).style("font-weight: bold;")
                    ui.label(f"{meal.get('category', '')} • {meal.get('area', '')}").style("color: #666; font-size: 14px;")
                
                ui.space()
                ui.button("View", on_click=lambda m=meal: self.show_meal_details(m)).props("color=green")
    
    def show_meal_details(self, meal):
        """Meal details dikhaye"""
        with ui.dialog() as dialog, ui.card().style("padding: 20px; max-width: 500px;"):
            # Header
            with ui.row().style("align-items: center; margin-bottom: 20px;"):
                if meal.get("image"):
                    ui.image(meal["image"]).style("width: 100px; height: 100px; object-fit: cover; border-radius: 8px;")
                
                with ui.column().style("margin-left: 15px;"):
                    ui.label(meal.get("name", "")).style("font-size: 24px; font-weight: bold;")
                    with ui.row().style("color: #666;"):
                        ui.badge(meal.get("category", "")).props("color=blue")
                        ui.badge(meal.get("area", "")).props("color=green").style("margin-left: 5px;")
            
            # Ingredients
            ui.label("Ingredients:").style("font-weight: bold; margin-top: 15px;")
            ingredients = meal.get("ingredients", "").split(", ")
            for ing in ingredients[:8]:  # Max 8 ingredients
                ui.label(f"• {ing}")
            
            # Instructions
            ui.label("Instructions:").style("font-weight: bold; margin-top: 15px;")
            ui.html(f"<div style='max-height: 150px; overflow-y: auto; padding: 10px; background-color: #f5f5f5; border-radius: 5px;'>{meal.get('instructions', 'No instructions available')}</div>")
            
            # YouTube link
            if meal.get("youtube"):
                ui.link("Watch on YouTube", meal["youtube"], new_tab=True).props("color=red").style("margin-top: 15px;")
            
            # Close button
            ui.button("Close", on_click=dialog.close).props("color=gray").style("margin-top: 20px; width: 100%;")
        
        dialog.open()

# ========== MAIN ==========
def main():
    """App start karo"""
    app = SimpleMealApp()
    app.run()
    
    # Port 8081 use karo (8080 busy hai)
    ui.run(
        title="Simple Meal Finder",
        port=8081,  # Yahaan port change kiya hai
        favicon="🍔",
        reload=False
    )

if __name__ == "__main__":
    main()