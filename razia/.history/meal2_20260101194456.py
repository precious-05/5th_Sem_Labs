import requests
import pandas as pd
import os
from nicegui import ui

class MealETL:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
    
    def get_data(self):
        """Get data from 3 APIs"""
        data = {}
        
        try:
            # 1. Random meal
            random_data = self._api_call("/random.php")
            data["random"] = random_data
            
            # 2. Categories
            cat_data = self._api_call("/categories.php")
            data["categories"] = cat_data
            
            # 3. Chicken meals
            chicken_data = self._api_call("/filter.php?i=chicken")
            data["chicken"] = chicken_data
            
        except:
            pass
        
        return data
    
    def _api_call(self, endpoint):
        """Simple API call"""
        try:
            response = requests.get(self.base_url + endpoint, timeout=10)
            return response.json() if response.ok else {}
        except:
            return {}
    
    def clean_data(self, data):
        """Clean the data"""
        meals = []
        
        # Random meal
        if data.get("random") and "meals" in data["random"]:
            for meal in data["random"]["meals"]:
                meals.append(self._clean_meal(meal))
        
        # Chicken meals (first 3)
        if data.get("chicken") and "meals" in data["chicken"]:
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
            "ingredients": ", ".join(ingredients[:5]),
            "youtube": meal.get("strYoutube", "")
        }
    
    def save_csv(self, meals, folder):
        """Save to CSV"""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        path = os.path.join(folder, "meals.csv")
        
        if meals:
            df = pd.DataFrame(meals)
            
            if os.path.exists(path) and os.path.getsize(path) > 0:
                old_df = pd.read_csv(path)
                df = pd.concat([old_df, df]).drop_duplicates(subset=['id'])
            
            df.to_csv(path, index=False, encoding='utf-8')
            return path, len(meals)
        
        return path, 0

# Initialize ETL
etl = MealETL()
meals_data = []
csv_folder = "meal_data"

# Create folder if not exists
if not os.path.exists(csv_folder):
    os.makedirs(csv_folder)

# Load existing data
def load_existing_data():
    global meals_data
    file_path = os.path.join(csv_folder, "meals.csv")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            meals_data = df.to_dict('records')
        except:
            meals_data = []
    else:
        meals_data = []

load_existing_data()

# Custom CSS for beautiful food-themed colors
ui.add_head_html('''
<style>
    /* Food Theme Colors */
    :root {
        --tomato: #FF6347;
        --olive: #808000;
        --basil: #356244;
        --cheese: #FFA500;
        --cream: #FFFDD0;
        --berry: #8A2BE2;
        --mint: #98FB98;
        --chocolate: #D2691E;
    }
    
    .header-bg {
        background: linear-gradient(135deg, var(--tomato) 0%, var(--cheese) 100%);
    }
    
    .card-bg {
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 99, 71, 0.1);
    }
    
    .meal-card {
        transition: all 0.3s ease;
        border-radius: 12px;
        overflow: hidden;
        background: white;
        border: 1px solid rgba(128, 128, 0, 0.1);
    }
    
    .meal-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255, 99, 71, 0.2);
        border-color: var(--tomato);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--tomato) 0%, var(--cheese) 100%);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 24px;
    }
    
    .btn-primary:hover {
        background: linear-gradient(135deg, #e5533d 0%, #e69500 100%);
        transform: scale(1.02);
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, var(--basil) 0%, var(--olive) 100%);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 20px;
    }
    
    .stat-badge {
        background: linear-gradient(135deg, var(--berry) 0%, var(--mint) 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .search-box {
        border: 2px solid var(--tomato);
        border-radius: 8px;
        padding: 10px 15px;
        transition: all 0.3s;
    }
    
    .search-box:focus {
        border-color: var(--cheese);
        box-shadow: 0 0 0 3px rgba(255, 99, 71, 0.2);
    }
    
    .category-tag {
        background: var(--cream);
        color: var(--chocolate);
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(210, 105, 30, 0.2);
    }
    
    .area-tag {
        background: var(--mint);
        color: var(--basil);
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(53, 98, 68, 0.2);
    }
</style>
''')

# Create single page UI
@ui.page('/')
def main_page():
    # Header
    with ui.header().classes('header-bg h-20 shadow-lg'):
        with ui.row().classes('items-center justify-between w-full px-8'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('restaurant', size='2rem', color='white')
                ui.label('FOOD EXPLORER').classes('text-2xl font-bold text-white tracking-wide')
            
            with ui.row().classes('items-center gap-4'):
                ui.badge(f'{len(meals_data)} MEALS', color='positive').props('outline')
    
    # Main content - Single page layout
    with ui.row().classes('w-full min-h-[calc(100vh-80px)] p-6 gap-6'):
        # Left sidebar - ETL Controls
        with ui.column().classes('w-1/4 gap-6'):
            # ETL Process Card
            with ui.card().classes('card-bg p-6'):
                ui.label('ETL PROCESS').classes('text-xl font-bold mb-4 text-[#D2691E]')
                
                # ETL Steps with food icons
                steps = [
                    ('🍅 EXTRACT', 'Fetch from MealDB API'),
                    ('🥑 TRANSFORM', 'Clean & organize data'),
                    ('🧀 LOAD', 'Save to meals.csv')
                ]
                
                for icon, desc in steps:
                    with ui.row().classes('items-center mb-4 p-3 rounded-lg bg-[#FFFDD0]'):
                        ui.label(icon).classes('text-2xl')
                        ui.label(desc).classes('ml-3 text-gray-700 font-medium')
                
                # Run ETL Button
                async def run_etl_process():
                    try:
                        # Show loading dialog
                        with ui.dialog() as loading_dialog, ui.card().classes('p-6'):
                            with ui.column().classes('items-center'):
                                ui.spinner('oval', size='lg', color='primary')
                                ui.label('Cooking up delicious meals...').classes('mt-4 text-lg font-medium')
                        loading_dialog.open()
                        
                        # Perform ETL
                        raw_data = etl.get_data()
                        clean_meals = etl.clean_data(raw_data)
                        
                        if not clean_meals:
                            loading_dialog.close()
                            ui.notify('No meals found. Please try again.', type='warning')
                            return
                        
                        path, count = etl.save_csv(clean_meals, csv_folder)
                        
                        # Reload data
                        load_existing_data()
                        
                        # Update UI
                        await display_meals()
                        loading_dialog.close()
                        
                        # Show success
                        with ui.dialog() as success, ui.card().classes('p-6'):
                            with ui.column().classes('items-center text-center'):
                                ui.icon('check_circle', size='3rem', color='green')
                                ui.label('ETL Complete!').classes('text-xl font-bold mt-4 text-green-600')
                                ui.label(f'🍽️ Added {count} delicious meals').classes('text-lg')
                                ui.button('OK', on_click=success.close, color='primary').classes('mt-4')
                        success.open()
                        
                    except Exception as e:
                        ui.notify(f'Error: {str(e)}', type='negative')
                
                ui.button('🚀 RUN ETL', 
                         on_click=run_etl_process, 
                         color='primary').classes('btn-primary w-full py-3 mt-2')
            
            # Statistics Card
            with ui.card().classes('card-bg p-6'):
                ui.label('STATISTICS').classes('text-xl font-bold mb-4 text-[#356244]')
                
                with ui.column().classes('gap-3'):
                    with ui.row().classes('items-center justify-between'):
                        ui.label('Total Meals:')
                        ui.badge(str(len(meals_data)), color='positive')
                    
                    with ui.row().classes('items-center justify-between'):
                        ui.label('CSV File:')
                        file_path = os.path.join(csv_folder, "meals.csv")
                        if os.path.exists(file_path):
                            size = os.path.getsize(file_path) / 1024
                            ui.label(f'{size:.1f} KB').classes('font-semibold')
                        else:
                            ui.label('Not created').classes('text-gray-500')
                    
                    # Categories count
                    if meals_data:
                        categories = set(m['category'] for m in meals_data if 'category' in m)
                        with ui.row().classes('items-center justify-between'):
                            ui.label('Categories:')
                            ui.badge(str(len(categories)), color='secondary')
        
        # Main content area - Meals Grid
        with ui.column().classes('w-3/4 gap-6'):
            # Search and Info Bar
            with ui.card().classes('card-bg p-4'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('search', size='1.5rem', color='#FF6347')
                        search_input = ui.input(
                            placeholder='Search meals by name, category, or ingredients...',
                            on_change=lambda e: filter_meals(e.value)
                        ).classes('search-box w-96')
                    
                    ui.label(f'Showing {len(meals_data)} meals').classes('font-semibold text-[#808000]')
            
            # Meals Grid Container
            meals_container = ui.column().classes('w-full')
            
            async def display_meals():
                meals_container.clear()
                
                if not meals_data:
                    with meals_container:
                        with ui.column().classes('items-center justify-center py-16 text-center'):
                            ui.icon('restaurant_menu', size='4rem', color='#FFA500')
                            ui.label('No Recipes Yet').classes('text-2xl font-bold mt-4 text-[#D2691E]')
                            ui.label('Click "RUN ETL" to fetch delicious meals').classes('text-gray-500 mt-2')
                    return
                
                with meals_container:
                    with ui.grid(columns=3).classes('w-full gap-6'):
                        for meal in meals_data:
                            create_meal_card(meal)
            
            def create_meal_card(meal):
                with ui.card().classes('meal-card'):
                    # Meal Image
                    if meal.get('image'):
                        ui.image(meal['image']).classes('w-full h-48 object-cover')
                    
                    # Content
                    with ui.column().classes('p-4'):
                        # Meal Name
                        name = meal.get('name', 'Unknown Dish')
                        if len(name) > 25:
                            name = name[:22] + '...'
                        ui.label(name).classes('text-lg font-bold text-gray-800 mb-2')
                        
                        # Category and Area Tags
                        with ui.row().classes('gap-2 mb-3'):
                            if meal.get('category'):
                                ui.label(meal['category']).classes('category-tag')
                            if meal.get('area'):
                                ui.label(meal['area']).classes('area-tag')
                        
                        # Ingredients Preview
                        ingredients = meal.get('ingredients', 'No ingredients listed')
                        if len(ingredients) > 50:
                            ingredients = ingredients[:47] + '...'
                        
                        with ui.row().classes('items-start'):
                            ui.icon('shopping_basket', size='1rem', color='#356244').classes('mt-1')
                            ui.label(ingredients).classes('text-sm text-gray-600 ml-2 flex-1')
                        
                        # View Recipe Button
                        ui.button('VIEW RECIPE', 
                                on_click=lambda m=meal: show_recipe_details(m),
                                color='primary').props('flat').classes('w-full mt-4')
            
            def filter_meals(query):
                meals_container.clear()
                
                if not query:
                    display_meals()
                    return
                
                query = query.lower()
                filtered = []
                for meal in meals_data:
                    if (query in meal.get('name', '').lower() or 
                        query in meal.get('category', '').lower() or
                        query in meal.get('area', '').lower() or
                        query in meal.get('ingredients', '').lower()):
                        filtered.append(meal)
                
                if not filtered:
                    with meals_container:
                        with ui.column().classes('items-center justify-center py-16 text-center'):
                            ui.icon('search_off', size='4rem', color='#FF6347')
                            ui.label(f'No meals found for "{query}"').classes('text-xl font-bold mt-4 text-gray-600')
                            ui.label('Try a different search term').classes('text-gray-500 mt-2')
                    return
                
                with meals_container:
                    with ui.grid(columns=3).classes('w-full gap-6'):
                        for meal in filtered:
                            create_meal_card(meal)
            
            def show_recipe_details(meal):
                with ui.dialog().props('maximized') as dialog, ui.card().classes('w-full h-full'):
                    # Recipe Header with Close button
                    with ui.row().classes('items-center justify-between p-4 border-b'):
                        ui.label('RECIPE DETAILS').classes('text-2xl font-bold text-[#D2691E]')
                        ui.button('CLOSE', on_click=dialog.close, color='primary').props('flat')
                    
                    with ui.row().classes('w-full h-[calc(100vh-100px)] p-6 gap-6'):
                        # Left Column - Image and Info
                        with ui.column().classes('w-1/3'):
                            if meal.get('image'):
                                ui.image(meal['image']).classes('w-full h-64 object-cover rounded-lg shadow-lg')
                            
                            with ui.card().classes('w-full mt-4 p-4 card-bg'):
                                ui.label(meal.get('name', '')).classes('text-xl font-bold mb-3')
                                
                                with ui.column().classes('gap-3'):
                                    with ui.row().classes('items-center'):
                                        ui.icon('category', color='#FF6347')
                                        ui.label(f"Category: {meal.get('category', 'Unknown')}").classes('ml-2 font-medium')
                                    
                                    with ui.row().classes('items-center'):
                                        ui.icon('place', color='#808000')
                                        ui.label(f"Region: {meal.get('area', 'Unknown')}").classes('ml-2 font-medium')
                        
                        # Right Column - Recipe
                        with ui.column().classes('w-2/3'):
                            # Ingredients
                            with ui.card().classes('w-full mb-6 card-bg'):
                                with ui.row().classes('items-center mb-4'):
                                    ui.icon('shopping_basket', color='#356244', size='2rem')
                                    ui.label('INGREDIENTS').classes('text-xl font-bold ml-2 text-[#356244]')
                                
                                ingredients = meal.get('ingredients', '').split(', ')
                                with ui.grid(columns=2).classes('w-full gap-3'):
                                    for ing in ingredients:
                                        with ui.row().classes('items-center p-2 hover:bg-[#FFFDD0] rounded'):
                                            ui.icon('check_circle', size='1rem', color='#98FB98')
                                            ui.label(ing.strip()).classes('ml-2')
                            
                            # Instructions
                            with ui.card().classes('w-full card-bg'):
                                with ui.row().classes('items-center mb-4'):
                                    ui.icon('menu_book', color='#8A2BE2', size='2rem')
                                    ui.label('INSTRUCTIONS').classes('text-xl font-bold ml-2 text-[#8A2BE2]')
                                
                                instructions = meal.get('instructions', 'No instructions available.')
                                ui.markdown(f'<div class="prose max-w-none p-4">{instructions}</div>')
            
            # Display initial meals
            ui.timer(0.1, lambda: display_meals(), once=True)

# Run the application
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Food Explorer - Meal Finder",
        port=8082,
        reload=False,
        dark=False,
        show=True
    )