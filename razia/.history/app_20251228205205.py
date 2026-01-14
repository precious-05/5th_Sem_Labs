"""
Meal Finder Application
Complete ETL Pipeline with NiceGUI Frontend
Fetches data from TheMealDB API (using test key '1')
Stores transformed data in CSV format only
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os
from typing import List, Dict, Optional
from nicegui import ui, app

# ============================================
# CONFIGURATION
# ============================================
class Config:
    """Configuration settings for the application"""
    API_BASE_URL = "https://www.themealdb.com/api/json/v1/1"
    API_KEY = "1"  # Test API key from TheMealDB documentation
    CSV_DIR = "meal_data"
    
    # CSV file names
    MEALS_CSV = "meals.csv"
    CATEGORIES_CSV = "categories.csv"
    INGREDIENTS_CSV = "ingredients.csv"
    
    # API endpoints from TheMealDB documentation
    ENDPOINTS = {
        "random_meal": "/random.php",
        "search_by_name": "/search.php?s=",
        "lookup_by_id": "/lookup.php?i=",
        "categories": "/categories.php",
        "list_categories": "/list.php?c=list",
        "list_areas": "/list.php?a=list",
        "list_ingredients": "/list.php?i=list",
        "filter_by_ingredient": "/filter.php?i=",
        "filter_by_category": "/filter.php?c=",
        "filter_by_area": "/filter.php?a=",
    }

# ============================================
# DATA EXTRACTION (E)
# ============================================
class DataExtractor:
    """Handles data extraction from TheMealDB API"""
    
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.api_key = Config.API_KEY
        
    def _make_api_request(self, endpoint: str, params: str = "") -> Dict:
        """Make API request and return JSON response"""
        try:
            url = f"{self.base_url}{endpoint}{params}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}
            
    def fetch_random_meals(self, count: int = 20) -> List[Dict]:
        """Fetch multiple random meals"""
        meals = []
        for _ in range(count):
            data = self._make_api_request(Config.ENDPOINTS["random_meal"])
            if data and "meals" in data and data["meals"]:
                meals.append(data["meals"][0])
        return meals
        
    def fetch_categories(self) -> List[Dict]:
        """Fetch all meal categories"""
        data = self._make_api_request(Config.ENDPOINTS["categories"])
        return data.get("categories", []) if data else []
        
    def fetch_ingredients_list(self) -> List[str]:
        """Fetch list of all ingredients"""
        data = self._make_api_request(Config.ENDPOINTS["list_ingredients"])
        if data and "meals" in data:
            return [ingredient["strIngredient"] for ingredient in data["meals"]]
        return []
        
    def search_meals_by_name(self, name: str) -> List[Dict]:
        """Search meals by name"""
        data = self._make_api_request(Config.ENDPOINTS["search_by_name"], name)
        return data.get("meals", []) if data else []
        
    def filter_by_category(self, category: str) -> List[Dict]:
        """Filter meals by category"""
        data = self._make_api_request(Config.ENDPOINTS["filter_by_category"], category)
        meals = data.get("meals", []) if data else []
        
        # Fetch full details for each meal
        detailed_meals = []
        for meal in meals[:10]:  # Limit to 10 for performance
            detailed = self.fetch_meal_by_id(meal.get("idMeal"))
            if detailed:
                detailed_meals.append(detailed)
        return detailed_meals
        
    def fetch_meal_by_id(self, meal_id: str) -> Optional[Dict]:
        """Fetch full meal details by ID"""
        data = self._make_api_request(Config.ENDPOINTS["lookup_by_id"], meal_id)
        if data and "meals" in data and data["meals"]:
            return data["meals"][0]
        return None

# ============================================
# DATA TRANSFORMATION (T)
# ============================================
class DataTransformer:
    """Handles data cleaning and transformation"""
    
    @staticmethod
    def clean_meal_data(meal: Dict) -> Dict:
        """Clean and standardize meal data"""
        if not meal:
            return {}
            
        # Extract ingredients and measures
        ingredients = []
        measures = []
        
        for i in range(1, 21):  # TheMealDB has up to 20 ingredients
            ingredient = meal.get(f"strIngredient{i}", "").strip()
            measure = meal.get(f"strMeasure{i}", "").strip()
            
            if ingredient and ingredient.lower() != "null" and ingredient.lower() != "":
                ingredients.append(ingredient)
                measures.append(measure if measure else "To taste")
                
        # Clean instructions - remove excessive whitespace
        instructions = meal.get("strInstructions", "")
        if instructions:
            instructions = ' '.join(instructions.split())
            
        # Create standardized meal dictionary
        cleaned_meal = {
            "id": meal.get("idMeal", ""),
            "name": meal.get("strMeal", "").strip(),
            "category": meal.get("strCategory", "").strip(),
            "area": meal.get("strArea", "").strip(),
            "instructions": instructions[:500] if instructions else "",  # Limit length
            "image_url": meal.get("strMealThumb", ""),
            "youtube_url": meal.get("strYoutube", ""),
            "source_url": meal.get("strSource", ""),
            "ingredients": ", ".join(ingredients),
            "measures": ", ".join(measures),
            "ingredient_count": len(ingredients),
            "difficulty": DataTransformer._estimate_difficulty(meal),
            "vegetarian": DataTransformer._is_vegetarian(ingredients),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return cleaned_meal
        
    @staticmethod
    def _estimate_difficulty(meal: Dict) -> str:
        """Estimate meal difficulty based on ingredients and instructions"""
        ingredient_count = 0
        for i in range(1, 21):
            if meal.get(f"strIngredient{i}", "").strip():
                ingredient_count += 1
                
        instructions = meal.get("strInstructions", "")
        instruction_words = len(instructions.split()) if instructions else 0
        
        if ingredient_count <= 5 and instruction_words <= 100:
            return "Easy"
        elif ingredient_count <= 10 and instruction_words <= 200:
            return "Medium"
        else:
            return "Advanced"
            
    @staticmethod
    def _is_vegetarian(ingredients: List[str]) -> bool:
        """Check if meal is vegetarian (basic check)"""
        non_veg_keywords = ["chicken", "beef", "pork", "fish", "meat", "bacon", 
                           "sausage", "lamb", "shrimp", "prawn", "crab", "lobster"]
        
        for ingredient in ingredients:
            if any(keyword in ingredient.lower() for keyword in non_veg_keywords):
                return False
        return True
        
    @staticmethod
    def clean_category_data(category: Dict) -> Dict:
        """Clean and standardize category data"""
        return {
            "id": category.get("idCategory", ""),
            "name": category.get("strCategory", "").strip(),
            "description": category.get("strCategoryDescription", "").strip()[:200],
            "thumbnail_url": category.get("strCategoryThumb", ""),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# ============================================
# DATA LOADING (L)
# ============================================
class DataLoader:
    """Handles saving transformed data to CSV files"""
    
    @staticmethod
    def ensure_csv_directory():
        """Create CSV directory if it doesn't exist"""
        if not os.path.exists(Config.CSV_DIR):
            os.makedirs(Config.CSV_DIR)
            
    @staticmethod
    def save_to_csv(data: List[Dict], filename: str) -> bool:
        """Save data to CSV file"""
        try:
            DataLoader.ensure_csv_directory()
            
            if not data:
                print(f"No data to save to {filename}")
                return False
                
            df = pd.DataFrame(data)
            filepath = os.path.join(Config.CSV_DIR, filename)
            
            # Check if file exists to append or create new
            if os.path.exists(filepath):
                existing_df = pd.read_csv(filepath)
                df = pd.concat([existing_df, df], ignore_index=True)
                df = df.drop_duplicates(subset=['id'] if 'id' in df.columns else None)
                
            df.to_csv(filepath, index=False)
            print(f"Successfully saved {len(data)} records to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False
            
    @staticmethod
    def load_from_csv(filename: str) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            filepath = os.path.join(Config.CSV_DIR, filename)
            if os.path.exists(filepath):
                return pd.read_csv(filepath)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()

# ============================================
# ETL PIPELINE MANAGER
# ============================================
class ETLPipeline:
    """Orchestrates the complete ETL process"""
    
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        
    def run_full_pipeline(self):
        """Execute complete ETL pipeline"""
        print("Starting ETL Pipeline...")
        
        # Extract data
        print("1. Extracting data from API...")
        random_meals = self.extractor.fetch_random_meals(15)
        categories = self.extractor.fetch_categories()
        
        # Transform data
        print("2. Transforming data...")
        cleaned_meals = [self.transformer.clean_meal_data(meal) for meal in random_meals]
        cleaned_categories = [self.transformer.clean_category_data(cat) for cat in categories]
        
        # Extract ingredients from meals
        all_ingredients = set()
        for meal in cleaned_meals:
            if "ingredients" in meal:
                ingredients = meal["ingredients"].split(", ")
                all_ingredients.update(ingredients)
                
        ingredient_data = [{"name": ing, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 
                          for ing in all_ingredients if ing]
        
        # Load data
        print("3. Loading data to CSV files...")
        self.loader.save_to_csv(cleaned_meals, Config.MEALS_CSV)
        self.loader.save_to_csv(cleaned_categories, Config.CATEGORIES_CSV)
        self.loader.save_to_csv(ingredient_data, Config.INGREDIENTS_CSV)
        
        print("ETL Pipeline completed successfully!")
        return len(cleaned_meals), len(cleaned_categories), len(ingredient_data)

# ============================================
# NICE GUI FRONTEND
# ============================================
class MealFinderApp:
    """NiceGUI frontend for the Meal Finder application"""
    
    def __init__(self):
        self.etl = ETLPipeline()
        self.current_meals = []
        self.categories = []
        self.areas = []
        
    def run_etl_on_startup(self):
        """Run ETL pipeline when app starts"""
        with ui.row().classes('justify-center w-full'):
            with ui.column().classes('items-center'):
                ui.spinner(size='lg', color='primary')
                ui.label('Loading meal data...').classes('text-lg mt-2')
                
        ui.timer(0.1, self._complete_startup, once=True)
        
    def _complete_startup(self):
        """Complete startup process"""
        ui.run_javascript('location.reload()')
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Header
        with ui.header().classes('bg-gradient-to-r from-primary to-secondary text-white'):
            with ui.row().classes('items-center w-full'):
                ui.icon('restaurant', size='2rem')
                ui.label('Meal Finder').classes('text-2xl font-bold ml-2')
                ui.space()
                ui.button('Run ETL', on_click=self.run_etl_manual, icon='refresh').classes('bg-white text-primary')
                
        # Main content
        with ui.tabs().classes('w-full bg-gray-100') as tabs:
            self.browse_tab = ui.tab('Browse Meals', icon='restaurant_menu')
            self.search_tab = ui.tab('Search', icon='search')
            self.categories_tab = ui.tab('Categories', icon='category')
            self.etl_tab = ui.tab('ETL Status', icon='storage')
            
        with ui.tab_panels(tabs, value=self.browse_tab).classes('w-full'):
            # Browse Tab
            with ui.tab_panel(self.browse_tab):
                self.setup_browse_tab()
                
            # Search Tab
            with ui.tab_panel(self.search_tab):
                self.setup_search_tab()
                
            # Categories Tab
            with ui.tab_panel(self.categories_tab):
                self.setup_categories_tab()
                
            # ETL Tab
            with ui.tab_panel(self.etl_tab):
                self.setup_etl_tab()
                
        # Load initial data
        self.load_initial_data()
        
    def setup_browse_tab(self):
        """Setup the browse meals tab"""
        with ui.column().classes('w-full p-4'):
            # Filters
            with ui.row().classes('w-full items-center mb-4'):
                ui.label('Filters:').classes('font-bold mr-2')
                
                # Category filter
                self.category_select = ui.select(
                    label='Category',
                    options=['All'] + self.categories,
                    value='All',
                    on_change=self.apply_filters
                ).classes('w-40')
                
                # Area filter
                self.area_select = ui.select(
                    label='Cuisine',
                    options=['All'] + self.areas,
                    value='All',
                    on_change=self.apply_filters
                ).classes('w-40')
                
                # Difficulty filter
                self.difficulty_select = ui.select(
                    label='Difficulty',
                    options=['All', 'Easy', 'Medium', 'Advanced'],
                    value='All',
                    on_change=self.apply_filters
                ).classes('w-40')
                
                # Vegetarian filter
                self.vegetarian_toggle = ui.toggle(
                    options=['All', 'Vegetarian Only'],
                    value='All',
                    on_change=self.apply_filters
                ).classes('ml-4')
                
                ui.space()
                ui.button('Clear Filters', on_click=self.clear_filters, icon='clear').classes('bg-gray-200')
                
            # Meals grid
            self.meals_container = ui.column().classes('w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6')
            
    def setup_search_tab(self):
        """Setup the search tab"""
        with ui.column().classes('w-full p-4'):
            # Search controls
            with ui.row().classes('w-full items-center mb-6'):
                with ui.column().classes('flex-grow'):
                    self.search_input = ui.input(
                        label='Search meals by name or ingredient',
                        placeholder='Enter meal name or ingredient...',
                        on_change=self.perform_search
                    ).props('outlined').classes('w-full')
                    
                ui.button('Search', on_click=self.perform_search, icon='search').classes('ml-2 h-10')
                
            # Search results
            self.search_results_container = ui.column().classes('w-full')
            
    def setup_categories_tab(self):
        """Setup the categories tab"""
        with ui.column().classes('w-full p-4'):
            ui.label('Meal Categories').classes('text-2xl font-bold mb-6')
            self.categories_container = ui.row().classes('w-full flex-wrap gap-4')
            
    def setup_etl_tab(self):
        """Setup the ETL status tab"""
        with ui.column().classes('w-full p-4'):
            ui.label('ETL Pipeline Status').classes('text-2xl font-bold mb-4')
            
            with ui.card().classes('w-full mb-4'):
                ui.label('Current Data Statistics').classes('text-lg font-bold mb-2')
                self.stats_row = ui.row().classes('w-full justify-around')
                
            with ui.card().classes('w-full'):
                ui.label('Run ETL Pipeline').classes('text-lg font-bold mb-2')
                ui.label('Extract data from API, transform it, and load to CSV files').classes('mb-4')
                
                with ui.row().classes('items-center'):
                    ui.button('Run Full ETL', on_click=self.run_etl_manual, icon='play_arrow')
                    ui.button('View CSV Files', on_click=self.view_csv_files, icon='folder').classes('ml-2')
                    
            # CSV file preview
            with ui.expansion('CSV File Previews', icon='table_chart').classes('w-full mt-4'):
                with ui.tabs().classes('w-full') as csv_tabs:
                    meals_csv_tab = ui.tab('Meals')
                    categories_csv_tab = ui.tab('Categories')
                    
                with ui.tab_panels(csv_tabs, value=meals_csv_tab).classes('w-full'):
                    with ui.tab_panel(meals_csv_tab):
                        self.meals_table = ui.table().classes('w-full')
                    with ui.tab_panel(categories_csv_tab):
                        self.categories_table = ui.table().classes('w-full')
                        
    def load_initial_data(self):
        """Load initial data from CSV files"""
        # Load meals
        meals_df = DataLoader.load_from_csv(Config.MEALS_CSV)
        if not meals_df.empty:
            self.current_meals = meals_df.to_dict('records')
            self.display_meals(self.current_meals)
            
            # Extract unique categories and areas
            self.categories = sorted(meals_df['category'].dropna().unique().tolist())
            self.areas = sorted(meals_df['area'].dropna().unique().tolist())
            
            # Update filter dropdowns
            self.category_select.options = ['All'] + self.categories
            self.area_select.options = ['All'] + self.areas
            
        # Load categories
        categories_df = DataLoader.load_from_csv(Config.CATEGORIES_CSV)
        if not categories_df.empty:
            self.display_categories(categories_df.to_dict('records'))
            
        # Update statistics
        self.update_statistics()
        
    def display_meals(self, meals: List[Dict]):
        """Display meals in a grid"""
        self.meals_container.clear()
        
        if not meals:
            with self.meals_container:
                ui.label('No meals found').classes('text-center text-gray-500 col-span-3')
            return
            
        for meal in meals[:30]:  # Limit display to 30 meals
            with ui.card().classes('w-full h-full'):
                # Meal image
                with ui.column().classes('w-full'):
                    if meal.get('image_url'):
                        ui.image(meal['image_url']).classes('w-full h-48 object-cover rounded-t-lg')
                    else:
                        ui.icon('restaurant', size='4rem').classes('text-gray-300 w-full h-48 flex items-center justify-center')
                        
                # Meal details
                with ui.column().classes('p-4'):
                    ui.label(meal.get('name', 'Unknown Meal')).classes('text-lg font-bold')
                    
                    with ui.row().classes('text-sm text-gray-600'):
                        ui.icon('category', size='xs')
                        ui.label(meal.get('category', 'Unknown'))
                        
                    with ui.row().classes('text-sm text-gray-600'):
                        ui.icon('place', size='xs')
                        ui.label(meal.get('area', 'Unknown'))
                        
                    with ui.row().classes('text-sm text-gray-600'):
                        ui.icon('bar_chart', size='xs')
                        ui.label(f"{meal.get('difficulty', 'Unknown')} • {meal.get('ingredient_count', 0)} ingredients")
                        
                    if meal.get('vegetarian'):
                        ui.badge('Vegetarian', color='green')
                        
                    # View details button
                    ui.button('View Details', on_click=lambda m=meal: self.show_meal_details(m)).classes('w-full mt-2')
                    
    def display_categories(self, categories: List[Dict]):
        """Display categories in a grid"""
        self.categories_container.clear()
        
        for category in categories:
            with ui.card().classes('w-48'):
                if category.get('thumbnail_url'):
                    ui.image(category['thumbnail_url']).classes('w-full h-32 object-cover')
                    
                with ui.column().classes('p-3'):
                    ui.label(category.get('name', 'Unknown')).classes('font-bold text-center')
                    
                    # Show meals count in this category
                    if 'name' in category:
                        count = len([m for m in self.current_meals if m.get('category') == category['name']])
                        ui.label(f'{count} meals').classes('text-sm text-gray-600 text-center')
                        
                    ui.button('Browse', on_click=lambda c=category: self.browse_category(c)).classes('w-full')
                    
    def apply_filters(self):
        """Apply filters to the meals list"""
        if not self.current_meals:
            return
            
        filtered = self.current_meals.copy()
        
        # Category filter
        category = self.category_select.value
        if category != 'All':
            filtered = [m for m in filtered if m.get('category') == category]
            
        # Area filter
        area = self.area_select.value
        if area != 'All':
            filtered = [m for m in filtered if m.get('area') == area]
            
        # Difficulty filter
        difficulty = self.difficulty_select.value
        if difficulty != 'All':
            filtered = [m for m in filtered if m.get('difficulty') == difficulty]
            
        # Vegetarian filter
        vegetarian = self.vegetarian_toggle.value
        if vegetarian == 'Vegetarian Only':
            filtered = [m for m in filtered if m.get('vegetarian') == True]
            
        self.display_meals(filtered)
        
    def clear_filters(self):
        """Clear all filters"""
        self.category_select.value = 'All'
        self.area_select.value = 'All'
        self.difficulty_select.value = 'All'
        self.vegetarian_toggle.value = 'All'
        self.display_meals(self.current_meals)
        
    def perform_search(self):
        """Perform search based on input"""
        query = self.search_input.value.lower().strip()
        if not query:
            return
            
        # Search in loaded meals
        results = []
        for meal in self.current_meals:
            if (query in meal.get('name', '').lower() or 
                query in meal.get('ingredients', '').lower() or
                query in meal.get('category', '').lower() or
                query in meal.get('area', '').lower()):
                results.append(meal)
                
        # If no results in loaded data, search API
        if not results:
            extractor = DataExtractor()
            api_results = extractor.search_meals_by_name(query)
            if api_results:
                transformer = DataTransformer()
                results = [transformer.clean_meal_data(meal) for meal in api_results]
                
        # Display results
        self.search_results_container.clear()
        
        if results:
            with self.search_results_container:
                ui.label(f'Found {len(results)} results for "{query}"').classes('text-lg font-bold mb-4')
                for meal in results[:10]:  # Limit to 10 results
                    self.display_search_result(meal)
        else:
            with self.search_results_container:
                ui.label(f'No results found for "{query}"').classes('text-center text-gray-500')
                
    def display_search_result(self, meal: Dict):
        """Display a single search result"""
        with ui.card().classes('w-full mb-4'):
            with ui.row().classes('w-full items-center'):
                if meal.get('image_url'):
                    ui.image(meal['image_url']).classes('w-24 h-24 object-cover rounded-lg')
                    
                with ui.column().classes('ml-4 flex-grow'):
                    ui.label(meal.get('name', 'Unknown')).classes('text-lg font-bold')
                    with ui.row().classes('text-sm text-gray-600'):
                        ui.label(f"{meal.get('category', '')} • {meal.get('area', '')}")
                        ui.badge(meal.get('difficulty', ''), color='blue').classes('ml-2')
                        
                ui.button('View', on_click=lambda m=meal: self.show_meal_details(m)).classes('ml-2')
                
    def browse_category(self, category: Dict):
        """Browse meals in a specific category"""
        category_name = category.get('name')
        if category_name:
            self.category_select.value = category_name
            self.apply_filters()
            
    def show_meal_details(self, meal: Dict):
        """Show detailed view of a meal"""
        with ui.dialog() as dialog, ui.card().classes('p-6 max-w-2xl'):
            # Meal header
            with ui.row().classes('w-full items-start mb-4'):
                if meal.get('image_url'):
                    ui.image(meal['image_url']).classes('w-48 h-48 object-cover rounded-lg')
                    
                with ui.column().classes('ml-4 flex-grow'):
                    ui.label(meal.get('name', 'Unknown')).classes('text-2xl font-bold')
                    with ui.row().classes('text-sm text-gray-600 mb-2'):
                        ui.icon('category', size='xs')
                        ui.label(meal.get('category', ''))
                        ui.icon('place', size='xs').classes('ml-4')
                        ui.label(meal.get('area', ''))
                        
                    with ui.row().classes('mb-2'):
                        ui.badge(meal.get('difficulty', ''), color='blue')
                        ui.badge(f"{meal.get('ingredient_count', 0)} ingredients", color='gray').classes('ml-2')
                        if meal.get('vegetarian'):
                            ui.badge('Vegetarian', color='green').classes('ml-2')
                            
            # Ingredients section
            ui.label('Ingredients').classes('text-lg font-bold mt-4')
            ingredients = meal.get('ingredients', '').split(', ')
            measures = meal.get('measures', '').split(', ')
            
            with ui.grid(columns=2).classes('w-full gap-2 mb-4'):
                for i in range(min(len(ingredients), 10)):
                    with ui.card().classes('p-2'):
                        ui.label(f"• {ingredients[i]}").classes('font-medium')
                        if i < len(measures) and measures[i]:
                            ui.label(measures[i]).classes('text-sm text-gray-600')
                            
            # Instructions
            ui.label('Instructions').classes('text-lg font-bold mt-4')
            instructions = meal.get('instructions', 'No instructions available.')
            ui.markdown(instructions[:500] + ('...' if len(instructions) > 500 else '')).classes('mb-4')
            
            # Close button
            ui.button('Close', on_click=dialog.close).classes('w-full')
            
        dialog.open()
        
    def run_etl_manual(self):
        """Run ETL pipeline manually"""
        with ui.dialog() as dialog, ui.card().classes('p-6'):
            ui.label('Running ETL Pipeline...').classes('text-lg font-bold mb-4')
            
            with ui.column().classes('items-center'):
                ui.spinner(size='lg', color='primary')
                ui.label('Extracting, transforming, and loading data...').classes('mt-2')
                
            ui.timer(2.0, lambda: self._complete_etl(dialog), once=True)
            
        dialog.open()
        
    def _complete_etl(self, dialog):
        """Complete ETL process"""
        dialog.close()
        
        # Run the pipeline
        meal_count, category_count, ingredient_count = self.etl.run_full_pipeline()
        
        # Show success message
        ui.notify(f'ETL completed: {meal_count} meals, {category_count} categories, {ingredient_count} ingredients')
        
        # Reload data
        self.load_initial_data()
        
    def view_csv_files(self):
        """Display CSV file contents"""
        # Load meals CSV
        meals_df = DataLoader.load_from_csv(Config.MEALS_CSV)
        if not meals_df.empty:
            columns = [{'name': col, 'label': col, 'field': col} for col in meals_df.columns[:6]]
            rows = meals_df.head(10).to_dict('records')
            self.meals_table.columns = columns
            self.meals_table.rows = rows
            
        # Load categories CSV
        categories_df = DataLoader.load_from_csv(Config.CATEGORIES_CSV)
        if not categories_df.empty:
            columns = [{'name': col, 'label': col, 'field': col} for col in categories_df.columns]
            rows = categories_df.head(10).to_dict('records')
            self.categories_table.columns = columns
            self.categories_table.rows = rows
            
    def update_statistics(self):
        """Update ETL statistics display"""
        self.stats_row.clear()
        
        # Count meals
        meals_df = DataLoader.load_from_csv(Config.MEALS_CSV)
        meal_count = len(meals_df) if not meals_df.empty else 0
        
        # Count categories
        categories_df = DataLoader.load_from_csv(Config.CATEGORIES_CSV)
        category_count = len(categories_df) if not categories_df.empty else 0
        
        # Count ingredients
        ingredients_df = DataLoader.load_from_csv(Config.INGREDIENTS_CSV)
        ingredient_count = len(ingredients_df) if not ingredients_df.empty else 0
        
        with self.stats_row:
            with ui.column().classes('items-center'):
                ui.label(str(meal_count)).classes('text-3xl font-bold text-primary')
                ui.label('Meals').classes('text-sm text-gray-600')
                
            with ui.column().classes('items-center'):
                ui.label(str(category_count)).classes('text-3xl font-bold text-secondary')
                ui.label('Categories').classes('text-sm text-gray-600')
                
            with ui.column().classes('items-center'):
                ui.label(str(ingredient_count)).classes('text-3xl font-bold text-accent')
                ui.label('Ingredients').classes('text-sm text-gray-600')

# ============================================
# MAIN APPLICATION
# ============================================
def main():
    """Main application entry point"""
    # Create the app
    app = MealFinderApp()
    
    # Setup dark mode toggle (optional)
    dark = ui.dark_mode()
    ui.button('Toggle Dark Mode', icon='dark_mode', on_click=dark.toggle).classes('fixed bottom-4 right-4 z-50')
    
    # Run initial ETL if no data exists
    if not os.path.exists(os.path.join(Config.CSV_DIR, Config.MEALS_CSV)):
        app.run_etl_on_startup()
    else:
        app.setup_ui()
        
    # Run the application
    ui.run(title='Meal Finder - ETL Pipeline App', favicon='🍔', reload=False)

if __name__ == "__main__":
    main()