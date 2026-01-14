import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
import pandas as pd
import os
from datetime import datetime

# ========== ETL CLASS ==========
class MealETL:
    """ETL with 3 API endpoints"""
    
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
    
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
            "instructions": meal.get("strInstructions", "")[:200],
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
            
            if os.path.exists(path):
                old_df = pd.read_csv(path)
                df = pd.concat([old_df, df]).drop_duplicates(subset=['id'])
            
            df.to_csv(path, index=False)
            return path, len(meals)
        
        return path, 0

# ========== MAIN APPLICATION ==========
class MealFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Finder Application")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize ETL
        self.etl = MealETL()
        self.meals = []
        self.csv_folder = "meal_data"
        
        # Create default folder
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)
        
        # Load existing data
        self.load_existing_data()
        
        # Create GUI
        self.create_widgets()
    
    def create_widgets(self):
        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Tabs
        self.create_home_tab()
        self.create_browse_tab()
        self.create_search_tab()
        self.create_settings_tab()
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_home_tab(self):
        # Home Tab
        home_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(home_frame, text="Home")
        
        # Title
        title_label = tk.Label(home_frame, text="Meal Finder Application", 
                              font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(home_frame, 
                             text="Simple application to find and save meal recipes",
                             font=("Arial", 12), bg="#f0f0f0")
        desc_label.pack(pady=10)
        
        # Stats Frame
        stats_frame = tk.Frame(home_frame, bg="#f0f0f0")
        stats_frame.pack(pady=20)
        
        tk.Label(stats_frame, text=f"Total Meals Loaded: {len(self.meals)}", 
                font=("Arial", 11), bg="#f0f0f0").pack()
        
        # CSV info
        csv_path = os.path.join(self.csv_folder, "meals.csv")
        if os.path.exists(csv_path):
            size = os.path.getsize(csv_path) / 1024
            tk.Label(stats_frame, text=f"CSV File Size: {size:.1f} KB", 
                    font=("Arial", 11), bg="#f0f0f0").pack()
        
        # Buttons Frame
        button_frame = tk.Frame(home_frame, bg="#f0f0f0")
        button_frame.pack(pady=40)
        
        # ETL Button
        etl_btn = tk.Button(button_frame, text="Run ETL Process", 
                           font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                           width=20, height=2, command=self.run_etl)
        etl_btn.pack(pady=10)
        
        # Browse Button
        browse_btn = tk.Button(button_frame, text="Browse Meals", 
                              font=("Arial", 12), bg="#2196F3", fg="white",
                              width=20, height=2, 
                              command=lambda: self.notebook.select(1))
        browse_btn.pack(pady=10)
        
        # View CSV Button
        csv_btn = tk.Button(button_frame, text="View CSV Folder", 
                           font=("Arial", 12), bg="#FF9800", fg="white",
                           width=20, height=2, command=self.open_csv_folder)
        csv_btn.pack(pady=10)
    
    def create_browse_tab(self):
        # Browse Tab
        browse_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(browse_frame, text="Browse Meals")
        
        # Search Frame
        search_frame = tk.Frame(browse_frame, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text="Search:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_meals)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Meals Frame
        meals_frame = tk.Frame(browse_frame, bg="#f0f0f0")
        meals_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas and Scrollbar for meals
        canvas = tk.Canvas(meals_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(meals_frame, orient="vertical", command=canvas.yview)
        self.meals_container = tk.Frame(canvas, bg="#f0f0f0")
        
        self.meals_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.meals_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display meals
        self.display_meals()
    
    def create_search_tab(self):
        # Search Tab
        search_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(search_frame, text="Search API")
        
        # Search Frame
        search_top = tk.Frame(search_frame, bg="#f0f0f0")
        search_top.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(search_top, text="Search Meal:", font=("Arial", 12), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.api_search_var = tk.StringVar()
        api_entry = tk.Entry(search_top, textvariable=self.api_search_var, width=30)
        api_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_top, text="Search", command=self.search_api)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Results Frame
        results_frame = tk.Frame(search_frame, bg="#f0f0f0")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas for results
        results_canvas = tk.Canvas(results_frame, bg="#f0f0f0", highlightthickness=0)
        results_scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=results_canvas.yview)
        self.results_container = tk.Frame(results_canvas, bg="#f0f0f0")
        
        self.results_container.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )
        
        results_canvas.create_window((0, 0), window=self.results_container, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        results_canvas.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")
    
    def create_settings_tab(self):
        # Settings Tab
        settings_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(settings_frame, text="Settings")
        
        # CSV Path Frame
        path_frame = tk.LabelFrame(settings_frame, text="CSV Storage Path", 
                                  bg="#f0f0f0", padx=20, pady=20)
        path_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(path_frame, text="Current Path:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        
        self.path_var = tk.StringVar(value=self.csv_folder)
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=50)
        path_entry.grid(row=0, column=1, padx=10, pady=5)
        
        browse_btn = tk.Button(path_frame, text="Browse", command=self.change_path)
        browse_btn.grid(row=0, column=2, padx=5)
        
        update_btn = tk.Button(path_frame, text="Update Path", command=self.update_path)
        update_btn.grid(row=1, column=1, pady=10)
        
        # Info Frame
        info_frame = tk.LabelFrame(settings_frame, text="Information", 
                                  bg="#f0f0f0", padx=20, pady=20)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # File info
        csv_path = os.path.join(self.csv_folder, "meals.csv")
        if os.path.exists(csv_path):
            size = os.path.getsize(csv_path) / 1024
            row_count = len(pd.read_csv(csv_path)) if os.path.getsize(csv_path) > 0 else 0
            
            tk.Label(info_frame, text=f"CSV File: meals.csv", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=2)
            tk.Label(info_frame, text=f"Size: {size:.1f} KB", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=2)
            tk.Label(info_frame, text=f"Records: {row_count} meals", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=2)
            tk.Label(info_frame, text=f"Path: {csv_path}", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=2)
        else:
            tk.Label(info_frame, text="No CSV file created yet", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        
        # Export Button
        export_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        export_frame.pack(pady=20)
        
        export_btn = tk.Button(export_frame, text="Export Current Data", 
                              command=self.export_data, bg="#673AB7", fg="white")
        export_btn.pack()
    
    def load_existing_data(self):
        """Load existing CSV data"""
        csv_path = os.path.join(self.csv_folder, "meals.csv")
        
        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
            try:
                df = pd.read_csv(csv_path)
                self.meals = df.to_dict('records')
            except:
                self.meals = []
        else:
            self.meals = []
    
    def display_meals(self):
        """Display meals in browse tab"""
        # Clear container
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        if not self.meals:
            tk.Label(self.meals_container, text="No meals found. Run ETL first.", 
                    bg="#f0f0f0", font=("Arial", 12)).pack(pady=50)
            return
        
        # Display meals in grid
        row, col = 0, 0
        for meal in self.meals[:12]:  # Show first 12
            self.create_meal_card(meal, row, col)
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
    
    def create_meal_card(self, meal, row, col):
        """Create a card for a single meal"""
        card_frame = tk.Frame(self.meals_container, bg="white", relief=tk.RAISED, borderwidth=1)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        self.meals_container.grid_columnconfigure(col, weight=1)
        
        # Meal name
        name = meal.get("name", "Unknown")
        if len(name) > 30:
            name = name[:27] + "..."
        
        name_label = tk.Label(card_frame, text=name, font=("Arial", 11, "bold"), 
                             bg="white", wraplength=200)
        name_label.pack(pady=10, padx=10)
        
        # Category and Area
        info_text = f"{meal.get('category', '')}\n{meal.get('area', '')}"
        info_label = tk.Label(card_frame, text=info_text, bg="white", 
                             font=("Arial", 9))
        info_label.pack(pady=5)
        
        # Ingredients preview
        ingredients = meal.get("ingredients", "")
        if len(ingredients) > 50:
            ingredients = ingredients[:47] + "..."
        
        ing_label = tk.Label(card_frame, text=ingredients, bg="white", 
                            font=("Arial", 8), wraplength=200, justify=tk.LEFT)
        ing_label.pack(pady=5, padx=10)
        
        # View Details Button
        details_btn = tk.Button(card_frame, text="View Details", 
                               command=lambda m=meal: self.show_meal_details(m))
        details_btn.pack(pady=10)
    
    def filter_meals(self, *args):
        """Filter meals based on search"""
        query = self.search_var.get().lower()
        
        if not query:
            self.display_meals()
            return
        
        # Clear container
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        filtered = []
        for meal in self.meals:
            if (query in meal.get("name", "").lower() or 
                query in meal.get("category", "").lower() or
                query in meal.get("area", "").lower()):
                filtered.append(meal)
        
        if not filtered:
            tk.Label(self.meals_container, text="No matching meals found", 
                    bg="#f0f0f0", font=("Arial", 12)).pack(pady=50)
            return
        
        # Display filtered meals
        row, col = 0, 0
        for meal in filtered[:12]:
            self.create_meal_card(meal, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def run_etl(self):
        """Run the ETL process"""
        self.status_bar.config(text="Extracting data from API...")
        self.root.update()
        
        try:
            # Extract
            raw_data = self.etl.get_data()
            
            self.status_bar.config(text="Transforming data...")
            self.root.update()
            
            # Transform
            clean_meals = self.etl.clean_data(raw_data)
            
            self.status_bar.config(text="Saving to CSV...")
            self.root.update()
            
            # Load
            path, count = self.etl.save_csv(clean_meals, self.csv_folder)
            
            # Reload data
            self.load_existing_data()
            
            # Update display
            self.display_meals()
            
            self.status_bar.config(text=f"ETL Complete! Added {count} meals to CSV")
            messagebox.showinfo("Success", f"ETL process completed!\n\nAdded {count} meals to:\n{path}")
            
        except Exception as e:
            self.status_bar.config(text="ETL Failed")
            messagebox.showerror("Error", f"ETL process failed:\n{str(e)}")
    
    def search_api(self):
        """Search API for meals"""
        query = self.api_search_var.get().strip()
        
        if not query:
            messagebox.showwarning("Input Required", "Please enter a search term")
            return
        
        # Clear results
        for widget in self.results_container.winfo_children():
            widget.destroy()
        
        tk.Label(self.results_container, text=f"Searching for: {query}...", 
                bg="#f0f0f0", font=("Arial", 11)).pack(pady=10)
        
        self.root.update()
        
        try:
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            # Clear the "searching..." label
            for widget in self.results_container.winfo_children():
                widget.destroy()
            
            if data and "meals" in data:
                for meal in data["meals"][:5]:  # Show first 5
                    clean_meal = self.etl._clean_meal(meal)
                    
                    result_frame = tk.Frame(self.results_container, bg="white", 
                                           relief=tk.GROOVE, borderwidth=1)
                    result_frame.pack(fill=tk.X, padx=10, pady=5)
                    
                    # Meal info
                    info_frame = tk.Frame(result_frame, bg="white")
                    info_frame.pack(side=tk.LEFT, padx=10, pady=10)
                    
                    tk.Label(info_frame, text=clean_meal.get("name", ""), 
                            font=("Arial", 11, "bold"), bg="white").pack(anchor=tk.W)
                    
                    tk.Label(info_frame, 
                            text=f"{clean_meal.get('category')} - {clean_meal.get('area')}", 
                            bg="white").pack(anchor=tk.W)
                    
                    # Save button
                    save_btn = tk.Button(result_frame, text="Save to CSV", 
                                        command=lambda m=clean_meal: self.save_single_meal(m))
                    save_btn.pack(side=tk.RIGHT, padx=10, pady=10)
            else:
                tk.Label(self.results_container, text="No results found", 
                        bg="#f0f0f0", font=("Arial", 12)).pack(pady=20)
                
        except Exception as e:
            for widget in self.results_container.winfo_children():
                widget.destroy()
            
            tk.Label(self.results_container, text=f"Search failed: {str(e)}", 
                    bg="#f0f0f0", font=("Arial", 12)).pack(pady=20)
    
    def save_single_meal(self, meal):
        """Save a single meal to CSV"""
        try:
            # Add to current meals
            self.meals.append(meal)
            
            # Save to CSV
            df = pd.DataFrame([meal])
            path = os.path.join(self.csv_folder, "meals.csv")
            
            if os.path.exists(path) and os.path.getsize(path) > 0:
                old = pd.read_csv(path)
                df = pd.concat([old, df]).drop_duplicates(subset=['id'])
            
            df.to_csv(path, index=False)
            
            # Update display
            self.display_meals()
            
            self.status_bar.config(text=f"Saved: {meal['name']}")
            messagebox.showinfo("Saved", f"Meal saved to CSV:\n{meal['name']}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save meal:\n{str(e)}")
    
    def show_meal_details(self, meal):
        """Show detailed view of a meal"""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Meal Details: {meal.get('name', '')}")
        details_window.geometry("600x500")
        details_window.configure(bg="#f0f0f0")
        
        # Main frame
        main_frame = tk.Frame(details_window, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text=meal.get("name", ""), 
                              font=("Arial", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)
        
        # Category and Area
        cat_area = f"{meal.get('category', '')} | {meal.get('area', '')}"
        cat_label = tk.Label(main_frame, text=cat_area, 
                            font=("Arial", 12), bg="#f0f0f0")
        cat_label.pack(pady=5)
        
        # Ingredients
        ing_frame = tk.LabelFrame(main_frame, text="Ingredients", 
                                 bg="#f0f0f0", padx=10, pady=10)
        ing_frame.pack(fill=tk.X, pady=10)
        
        ingredients = meal.get("ingredients", "").split(", ")
        for ing in ingredients:
            tk.Label(ing_frame, text=f"• {ing}", bg="#f0f0f0", 
                    anchor="w").pack(fill=tk.X, pady=2)
        
        # Instructions
        instr_frame = tk.LabelFrame(main_frame, text="Instructions", 
                                   bg="#f0f0f0", padx=10, pady=10)
        instr_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        instr_text = scrolledtext.ScrolledText(instr_frame, wrap=tk.WORD, 
                                              width=60, height=10, font=("Arial", 10))
        instr_text.pack(fill=tk.BOTH, expand=True)
        instr_text.insert(tk.END, meal.get("instructions", ""))
        instr_text.config(state=tk.DISABLED)
        
        # YouTube link
        youtube = meal.get("youtube", "")
        if youtube:
            link_frame = tk.Frame(main_frame, bg="#f0f0f0")
            link_frame.pack(pady=10)
            
            tk.Label(link_frame, text="YouTube: ", bg="#f0f0f0").pack(side=tk.LEFT)
            link_label = tk.Label(link_frame, text=youtube, fg="blue", 
                                 cursor="hand2", bg="#f0f0f0")
            link_label.pack(side=tk.LEFT)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", 
                             command=details_window.destroy, width=20)
        close_btn.pack(pady=10)
    
    def change_path(self):
        """Change CSV storage path"""
        folder = filedialog.askdirectory(initialdir=self.csv_folder)
        if folder:
            self.path_var.set(folder)
    
    def update_path(self):
        """Update the CSV path"""
        new_path = self.path_var.get().strip()
        
        if not new_path:
            messagebox.showwarning("Invalid Path", "Please enter a valid path")
            return
        
        self.csv_folder = new_path
        
        # Create folder if it doesn't exist
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        
        # Reload data
        self.load_existing_data()
        
        # Update display
        self.display_meals()
        
        self.status_bar.config(text=f"Path updated to: {new_path}")
        messagebox.showinfo("Path Updated", f"CSV storage path updated to:\n{new_path}")
    
    def export_data(self):
        """Export current data to a new CSV"""
        if not self.meals:
            messagebox.showwarning("No Data", "No meals to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"meals_export_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if filename:
            try:
                df = pd.DataFrame(self.meals)
                df.to_csv(filename, index=False)
                
                self.status_bar.config(text=f"Data exported to: {filename}")
                messagebox.showinfo("Export Complete", f"Data exported to:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
    
    def open_csv_folder(self):
        """Open the CSV folder in file explorer"""
        if os.path.exists(self.csv_folder):
            os.startfile(self.csv_folder)
        else:
            messagebox.showwarning("Folder Not Found", "CSV folder does not exist")

# ========== MAIN FUNCTION ==========
def main():
    root = tk.Tk()
    app = MealFinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()