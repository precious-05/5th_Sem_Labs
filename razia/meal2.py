import pandas as pd
import os
from nicegui import ui

# Sample meal data (completely local - no API calls)
SAMPLE_MEALS = [
    {
        "id": "1",
        "name": "Spaghetti Carbonara",
        "category": "Pasta",
        "area": "Italian",
        "instructions": "Cook pasta. Mix eggs, cheese, pepper. Combine with hot pasta and bacon. Serve immediately.",
        "image": "https://images.unsplash.com/photo-1621996346565-e3dbc353d2c5?w=400",
        "ingredients": "400g spaghetti, 4 eggs, 100g parmesan, 200g bacon, black pepper"
    },
    {
        "id": "2",
        "name": "Chicken Curry",
        "category": "Curry",
        "area": "Indian",
        "instructions": "Cook onions until golden. Add chicken and spices. Simmer with coconut milk for 30 minutes.",
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400",
        "ingredients": "500g chicken, 2 onions, 3 tomatoes, coconut milk, curry spices"
    },
    {
        "id": "3",
        "name": "Caesar Salad",
        "category": "Salad",
        "area": "American",
        "instructions": "Mix lettuce, croutons, parmesan. Add dressing made from mayo, lemon, garlic, anchovies.",
        "image": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400",
        "ingredients": "Romaine lettuce, croutons, parmesan, Caesar dressing, chicken"
    },
    {
        "id": "4",
        "name": "Beef Tacos",
        "category": "Mexican",
        "area": "Mexican",
        "instructions": "Cook beef with taco seasoning. Warm tortillas. Add beef, lettuce, tomatoes, cheese, salsa.",
        "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
        "ingredients": "Ground beef, taco shells, lettuce, tomato, cheese, salsa"
    }
]

class MealETL:
    def __init__(self):
        pass
    
    def extract_data(self):
        """Extract data from local sample"""
        return SAMPLE_MEALS.copy()
    
    def transform_data(self, meals):
        """Transform data - add timestamps"""
        import datetime
        
        transformed = []
        for meal in meals:
            meal_copy = meal.copy()
            meal_copy['added_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            if isinstance(meal_copy.get('ingredients', ''), list):
                meal_copy['ingredients'] = ', '.join(meal_copy['ingredients'])
            
            transformed.append(meal_copy)
        
        return transformed
    
    def load_data(self, meals, folder):
        """Load data to CSV"""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        path = os.path.join(folder, "meals.csv")
        
        if meals:
            df = pd.DataFrame(meals)
            
            if os.path.exists(path) and os.path.getsize(path) > 0:
                old_df = pd.read_csv(path)
                df = pd.concat([old_df, df]).drop_duplicates(subset=['id'], keep='last')
            
            df.to_csv(path, index=False)
            return path, len(meals)
        
        return path, 0

# Initialize
etl = MealETL()
meals_data = []
csv_folder = "meal_data"

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

@ui.page('/')
def main_page():
    # Add CSS inside page function
    ui.add_head_html('''
    <style>
        .header-bg {
            background: linear-gradient(135deg, #FF6B6B 0%, #FFA500 100%);
        }
        
        .card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #FF6B6B 0%, #FFA500 100%);
            border: none;
            color: white;
            font-weight: 600;
            border-radius: 6px;
        }
        
        .search-box {
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 8px 12px;
        }
        
        .search-box:focus {
            border-color: #FF6B6B;
            outline: none;
        }
        
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .tag-category {
            background: #E3F2FD;
            color: #1976D2;
        }
        
        .tag-area {
            background: #E8F5E9;
            color: #388E3C;
        }
    </style>
    ''')
    
    # Header
    with ui.header().classes('header-bg h-16'):
        with ui.row().classes('items-center justify-between w-full px-6'):
            ui.label('Meal Finder').classes('text-xl font-bold text-white')
    
    # Main layout
    with ui.row().classes('w-full min-h-screen p-4 gap-4'):
        # Left panel - ETL Controls
        with ui.column().classes('w-1/4 gap-4'):
            # ETL Card
            with ui.card().classes('p-4'):
                ui.label('ETL Process').classes('text-lg font-bold mb-3 text-gray-700')
                
                # ETL Steps
                steps = [
                    ('Extract', 'Get data from local sample'),
                    ('Transform', 'Clean and add metadata'),
                    ('Load', 'Save to CSV file')
                ]
                
                for title, desc in steps:
                    with ui.row().classes('items-start mb-3'):
                        ui.icon('check_circle', size='sm', color='green').classes('mt-1')
                        with ui.column().classes('ml-2'):
                            ui.label(title).classes('font-medium')
                            ui.label(desc).classes('text-sm text-gray-500')
                
                # ETL Button
                def run_etl():
                    try:
                        # Show loading
                        loading = ui.notify('Running ETL process...', type='info')
                        
                        # ETL Process
                        extracted = etl.extract_data()
                        transformed = etl.transform_data(extracted)
                        path, count = etl.load_data(transformed, csv_folder)
                        
                        # Reload data
                        load_existing_data()
                        
                        # Update UI
                        display_meals()
                        
                        # Show success
                        loading.dismiss()
                        ui.notify(f'Added {count} meals', type='positive')
                        
                    except Exception as e:
                        ui.notify(f'Error: {str(e)}', type='negative')
                
                ui.button('Run ETL', on_click=run_etl, color='primary').classes('w-full py-2')
            
            # Info Card
            with ui.card().classes('p-4'):
                ui.label('Information').classes('text-lg font-bold mb-3 text-gray-700')
                
                file_path = os.path.join(csv_folder, "meals.csv")
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path) / 1024
                    ui.label(f'CSV Size: {size:.1f} KB').classes('text-sm mb-2')
                
                ui.label(f'Meals Loaded: {len(meals_data)}').classes('text-sm')
        
        # Right panel - Meals Display
        with ui.column().classes('w-3/4 gap-4'):
            # Search Bar
            with ui.card().classes('p-3'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('search', color='gray')
                    search_input = ui.input(
                        placeholder='Search meals...',
                        on_change=lambda e: filter_meals(e.value)
                    ).classes('search-box flex-1')
            
            # Meals Grid
            meals_container = ui.column().classes('w-full')
            
            def display_meals():
                meals_container.clear()
                
                if not meals_data:
                    with meals_container:
                        with ui.column().classes('items-center justify-center py-8 text-center'):
                            ui.icon('restaurant', size='xl', color='gray')
                            ui.label('No meals available').classes('text-lg font-medium mt-2 text-gray-600')
                            ui.label('Click Run ETL to load meals').classes('text-gray-500')
                    return
                
                with meals_container:
                    with ui.grid(columns=3).classes('w-full gap-4'):
                        for meal in meals_data:
                            create_meal_card(meal)
            
            def create_meal_card(meal):
                with ui.card().classes('p-0 overflow-hidden'):
                    # Image
                    if meal.get('image'):
                        ui.image(meal['image']).classes('w-full h-40 object-cover')
                    
                    # Content
                    with ui.column().classes('p-3'):
                        # Name
                        name = meal.get('name', '')
                        if len(name) > 20:
                            name = name[:17] + '...'
                        ui.label(name).classes('font-bold text-gray-800')
                        
                        # Tags
                        with ui.row().classes('gap-1 mt-1'):
                            if meal.get('category'):
                                ui.label(meal['category']).classes('tag tag-category')
                            if meal.get('area'):
                                ui.label(meal['area']).classes('tag tag-area')
                        
                        # Ingredients preview
                        ingredients = meal.get('ingredients', '')
                        if len(ingredients) > 40:
                            ingredients = ingredients[:37] + '...'
                        
                        ui.label(ingredients).classes('text-sm text-gray-600 mt-2')
                        
                        # View button
                        ui.button('View Details', 
                                on_click=lambda m=meal: show_details(m),
                                color='primary').props('size=sm').classes('w-full mt-3')
            
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
                        query in meal.get('area', '').lower()):
                        filtered.append(meal)
                
                if not filtered:
                    with meals_container:
                        with ui.column().classes('items-center justify-center py-8 text-center'):
                            ui.icon('search_off', size='xl', color='gray')
                            ui.label('No meals found').classes('text-gray-600 mt-2')
                    return
                
                with meals_container:
                    with ui.grid(columns=3).classes('w-full gap-4'):
                        for meal in filtered:
                            create_meal_card(meal)
            
            def show_details(meal):
                with ui.dialog() as dialog, ui.card().classes('p-4 w-full max-w-2xl'):
                    # Title and close
                    with ui.row().classes('items-center justify-between mb-4'):
                        ui.label('Meal Details').classes('text-xl font-bold')
                        ui.button('Close', on_click=dialog.close, icon='close').props('flat')
                    
                    # Image
                    if meal.get('image'):
                        ui.image(meal['image']).classes('w-full h-48 object-cover rounded mb-4')
                    
                    # Info
                    ui.label(meal.get('name', '')).classes('text-2xl font-bold mb-2')
                    
                    with ui.row().classes('gap-2 mb-4'):
                        ui.label(f"Category: {meal.get('category', '')}").classes('font-medium')
                        ui.label('•')
                        ui.label(f"Region: {meal.get('area', '')}").classes('font-medium')
                    
                    # Ingredients
                    ui.label('Ingredients:').classes('font-bold mb-2')
                    ingredients = meal.get('ingredients', '').split(', ')
                    for ing in ingredients:
                        ui.label(f'• {ing.strip()}').classes('ml-2')
                    
                    # Instructions
                    ui.label('Instructions:').classes('font-bold mt-4 mb-2')
                    ui.markdown(meal.get('instructions', ''))
            
            # Initial display
            ui.timer(0.1, lambda: display_meals(), once=True)

# Run app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Meal Finder",
        port=8082,
        reload=False,
        dark=False
    )