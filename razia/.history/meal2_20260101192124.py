import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
import os

class MealFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Meal Finder")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFE6E6")  # Light pink background
        
        # Colors
        self.colors = {
            "primary": "#FF6B6B",  # Coral red
            "secondary": "#4ECDC4",  # Turquoise
            "accent": "#FFD166",  # Yellow
            "background": "#FFE6E6",
            "card": "#FFFFFF"
        }
        
        self.meals = []
        self.csv_folder = "meal_data"
        
        # Create folder if not exists
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)
        
        self.load_existing_data()
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🍽️ DELICIOUS MEAL FINDER", 
                              font=("Arial", 28, "bold"), fg="white", 
                              bg=self.colors["primary"])
        title_label.pack(pady=30)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors["background"])
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Left panel - Controls
        control_frame = tk.Frame(main_container, bg=self.colors["card"], 
                                relief="ridge", borderwidth=2)
        control_frame.pack(side="left", fill="y", padx=(0, 20))
        
        # ETL Button
        etl_btn = tk.Button(control_frame, text="🔧 RUN ETL", 
                           font=("Arial", 14, "bold"),
                           bg=self.colors["secondary"], fg="white",
                           width=20, height=2,
                           command=self.run_etl)
        etl_btn.pack(pady=20, padx=20)
        
        # Stats
        stats_frame = tk.Frame(control_frame, bg=self.colors["card"])
        stats_frame.pack(pady=10, padx=20)
        
        self.stats_label = tk.Label(stats_frame, 
                                   text=f"📊 Total Meals: {len(self.meals)}",
                                   font=("Arial", 12),
                                   bg=self.colors["card"])
        self.stats_label.pack()
        
        # Save CSV Button
        save_btn = tk.Button(control_frame, text="💾 SAVE TO CSV", 
                            font=("Arial", 12),
                            bg=self.colors["accent"], fg="black",
                            width=18, height=2,
                            command=self.save_to_csv)
        save_btn.pack(pady=20)
        
        # Right panel - Meals display
        display_frame = tk.Frame(main_container, bg=self.colors["background"])
        display_frame.pack(side="right", fill="both", expand=True)
        
        # Search bar
        search_frame = tk.Frame(display_frame, bg=self.colors["background"])
        search_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Search:", font=("Arial", 12),
                bg=self.colors["background"]).pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                    font=("Arial", 12), width=25)
        self.search_entry.pack(side="left", padx=5)
        
        search_btn = tk.Button(search_frame, text="Search", 
                              command=self.search_meals,
                              bg=self.colors["primary"], fg="white")
        search_btn.pack(side="left", padx=5)
        
        # Canvas for scrollable meals
        canvas = tk.Canvas(display_frame, bg=self.colors["background"], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", 
                                 command=canvas.yview)
        
        self.meals_container = tk.Frame(canvas, bg=self.colors["background"])
        
        self.meals_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.meals_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Display meals
        self.display_meals()
    
    def run_etl(self):
        """Run ETL Process"""
        try:
            # Extract from 3 API endpoints
            api_data = {}
            
            # 1. Random meal
            random_response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
            api_data["random"] = random_response.json()
            
            # 2. Categories
            cat_response = requests.get("https://www.themealdb.com/api/json/v1/1/categories.php")
            api_data["categories"] = cat_response.json()
            
            # 3. Chicken meals
            chicken_response = requests.get("https://www.themealdb.com/api/json/v1/1/filter.php?i=chicken")
            api_data["chicken"] = chicken_response.json()
            
            # Transform data
            new_meals = []
            
            # Process random meal
            if api_data["random"] and "meals" in api_data["random"]:
                for meal in api_data["random"]["meals"]:
                    cleaned = self.clean_meal_data(meal)
                    new_meals.append(cleaned)
            
            # Process 2 chicken meals
            if api_data["chicken"] and "meals" in api_data["chicken"]:
                for meal in api_data["chicken"]["meals"][:2]:
                    detail_response = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal['idMeal']}")
                    if detail_response.ok:
                        detail_data = detail_response.json()
                        if detail_data and "meals" in detail_data:
                            cleaned = self.clean_meal_data(detail_data["meals"][0])
                            new_meals.append(cleaned)
            
            # Load - Add to existing meals
            for meal in new_meals:
                if meal not in self.meals:  # Simple duplicate check
                    self.meals.append(meal)
            
            # Update display
            self.display_meals()
            self.stats_label.config(text=f"📊 Total Meals: {len(self.meals)}")
            
            messagebox.showinfo("Success", f"ETL Complete!\nAdded {len(new_meals)} new meals")
            
        except Exception as e:
            messagebox.showerror("Error", f"ETL Failed:\n{str(e)}")
    
    def clean_meal_data(self, meal):
        """Clean and structure meal data"""
        # Extract ingredients
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
            "instructions": meal.get("strInstructions", "")[:100],
            "image": meal.get("strMealThumb", ""),
            "ingredients": ", ".join(ingredients[:3]),
            "youtube": meal.get("strYoutube", "")
        }
    
    def display_meals(self):
        """Display all meals"""
        # Clear container
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        if not self.meals:
            tk.Label(self.meals_container, 
                    text="No meals yet. Run ETL to get some delicious recipes!",
                    font=("Arial", 14), bg=self.colors["background"],
                    fg="#666666").pack(pady=50)
            return
        
        # Display in 2 columns
        for i, meal in enumerate(self.meals):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(self.meals_container, bg=self.colors["card"],
                            relief="solid", borderwidth=1)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Configure grid
            self.meals_container.grid_columnconfigure(col, weight=1)
            
            # Meal name
            name = meal["name"]
            if len(name) > 25:
                name = name[:22] + "..."
            
            name_label = tk.Label(frame, text=name, 
                                 font=("Arial", 12, "bold"),
                                 bg=self.colors["card"], wraplength=250)
            name_label.pack(pady=10, padx=10)
            
            # Category and area
            info_text = f"🍴 {meal['category']}\n🌍 {meal['area']}"
            info_label = tk.Label(frame, text=info_text,
                                 font=("Arial", 10),
                                 bg=self.colors["card"])
            info_label.pack(pady=5)
            
            # Ingredients preview
            ingredients = meal["ingredients"]
            if len(ingredients) > 40:
                ingredients = ingredients[:37] + "..."
            
            ing_label = tk.Label(frame, text=f"🥗 {ingredients}",
                               font=("Arial", 9),
                               bg=self.colors["card"], wraplength=250)
            ing_label.pack(pady=5, padx=10)
            
            # View button
            view_btn = tk.Button(frame, text="👁️ View Details",
                               command=lambda m=meal: self.show_details(m),
                               bg=self.colors["primary"], fg="white",
                               font=("Arial", 10))
            view_btn.pack(pady=10)
    
    def search_meals(self):
        """Search meals by name or category"""
        query = self.search_var.get().lower()
        
        if not query:
            self.display_meals()
            return
        
        # Clear container
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        # Filter meals
        filtered = [m for m in self.meals 
                   if query in m["name"].lower() or 
                   query in m["category"].lower() or
                   query in m["area"].lower()]
        
        if not filtered:
            tk.Label(self.meals_container, 
                    text=f"No meals found for '{query}'",
                    font=("Arial", 14), bg=self.colors["background"]).pack(pady=50)
            return
        
        # Display filtered results
        for i, meal in enumerate(filtered):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(self.meals_container, bg=self.colors["card"],
                            relief="solid", borderwidth=1)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Meal name
            name = meal["name"]
            if len(name) > 25:
                name = name[:22] + "..."
            
            tk.Label(frame, text=name, font=("Arial", 12, "bold"),
                    bg=self.colors["card"], wraplength=250).pack(pady=10, padx=10)
            
            tk.Label(frame, text=f"🍴 {meal['category']} | 🌍 {meal['area']}",
                    font=("Arial", 10), bg=self.colors["card"]).pack(pady=5)
            
            view_btn = tk.Button(frame, text="👁️ View Details",
                               command=lambda m=meal: self.show_details(m),
                               bg=self.colors["primary"], fg="white")
            view_btn.pack(pady=10)
    
    def show_details(self, meal):
        """Show meal details in a new window"""
        details_win = tk.Toplevel(self.root)
        details_win.title(meal["name"])
        details_win.geometry("500x600")
        details_win.configure(bg=self.colors["background"])
        
        # Title
        tk.Label(details_win, text=meal["name"], 
                font=("Arial", 20, "bold"),
                bg=self.colors["background"]).pack(pady=20)
        
        # Category and area
        tk.Label(details_win, 
                text=f"📁 Category: {meal['category']}\n📍 Area: {meal['area']}",
                font=("Arial", 12),
                bg=self.colors["background"]).pack(pady=10)
        
        # Ingredients
        tk.Label(details_win, text="🥗 Ingredients:",
                font=("Arial", 14, "bold"),
                bg=self.colors["background"]).pack(pady=10)
        
        ingredients = meal["ingredients"].split(", ")
        for ing in ingredients:
            tk.Label(details_win, text=f"• {ing}",
                    font=("Arial", 11),
                    bg=self.colors["background"],
                    anchor="w").pack(fill="x", padx=30)
        
        # Instructions
        tk.Label(details_win, text="📝 Instructions:",
                font=("Arial", 14, "bold"),
                bg=self.colors["background"]).pack(pady=10)
        
        instructions_text = tk.Text(details_win, height=8, width=50,
                                   font=("Arial", 10), wrap="word")
        instructions_text.pack(pady=10, padx=20)
        instructions_text.insert("1.0", meal["instructions"])
        instructions_text.config(state="disabled")
        
        # YouTube link
        if meal["youtube"]:
            tk.Label(details_win, text="🎬 Watch on YouTube:",
                    font=("Arial", 11, "bold"),
                    bg=self.colors["background"]).pack(pady=5)
            
            link_label = tk.Label(details_win, text=meal["youtube"],
                                 fg="blue", cursor="hand2",
                                 font=("Arial", 10),
                                 bg=self.colors["background"])
            link_label.pack()
        
        # Close button
        tk.Button(details_win, text="Close", 
                 command=details_win.destroy,
                 bg=self.colors["primary"], fg="white",
                 width=20).pack(pady=20)
    
    def save_to_csv(self):
        """Save all meals to CSV"""
        if not self.meals:
            messagebox.showwarning("No Data", "No meals to save. Run ETL first.")
            return
        
        try:
            df = pd.DataFrame(self.meals)
            csv_path = os.path.join(self.csv_folder, "meals.csv")
            df.to_csv(csv_path, index=False)
            
            messagebox.showinfo("Success", f"Saved {len(self.meals)} meals to:\n{csv_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV:\n{str(e)}")
    
    def load_existing_data(self):
        """Load meals from existing CSV"""
        csv_path = os.path.join(self.csv_folder, "meals.csv")
        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
            try:
                df = pd.read_csv(csv_path)
                self.meals = df.to_dict('records')
            except:
                self.meals = []

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MealFinderApp(root)
    root.mainloop()