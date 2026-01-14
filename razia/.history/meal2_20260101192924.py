import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
import os

class SimpleMealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Finder App")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")
        
        self.meals = []
        self.csv_folder = "meal_data"
        
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)
        
        self.load_existing_data()
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#4a90e2", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Meal Finder", 
                font=("Arial", 28, "bold"), 
                fg="white", bg="#4a90e2").pack(pady=25)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Left panel - Controls
        control_frame = tk.Frame(main_frame, bg="white", 
                                relief="solid", borderwidth=1)
        control_frame.pack(side="left", fill="y", padx=(0, 20))
        
        # ETL Section
        tk.Label(control_frame, text="ETL Process", 
                font=("Arial", 16, "bold"),
                bg="white").pack(pady=20)
        
        self.status_label = tk.Label(control_frame, 
                                    text=f"Meals: {len(self.meals)}",
                                    font=("Arial", 12),
                                    bg="white")
        self.status_label.pack(pady=10)
        
        tk.Button(control_frame, text="Run ETL", 
                 font=("Arial", 12, "bold"),
                 bg="#4a90e2", fg="white",
                 width=15, height=2,
                 command=self.perform_etl).pack(pady=20)
        
        # Right panel - Meals display
        display_frame = tk.Frame(main_frame, bg="#f0f8ff")
        display_frame.pack(side="right", fill="both", expand=True)
        
        # Search
        search_frame = tk.Frame(display_frame, bg="#f0f8ff")
        search_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(search_frame, text="Search:", 
                font=("Arial", 12), bg="#f0f8ff").pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_meals())
        tk.Entry(search_frame, textvariable=self.search_var, 
                font=("Arial", 12), width=25).pack(side="left", padx=5)
        
        # Meals container
        canvas = tk.Canvas(display_frame, bg="#f0f8ff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", 
                                 command=canvas.yview)
        
        self.meals_container = tk.Frame(canvas, bg="#f0f8ff")
        
        self.meals_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.meals_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        self.display_meals()
    
    def perform_etl(self):
        """ETL with single API endpoint"""
        try:
            self.status_label.config(text="Processing...")
            
            # EXTRACT - Single endpoint
            response = requests.get(
                "https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood",
                timeout=10
            )
            
            if not response.ok:
                raise Exception("API request failed")
            
            data = response.json()
            
            if not data.get("meals"):
                raise Exception("No meals found")
            
            # TRANSFORM
            new_meals = []
            for meal in data["meals"][:5]:  # Get first 5 meals
                # Get full details
                detail_response = requests.get(
                    f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal['idMeal']}"
                )
                
                if detail_response.ok:
                    detail_data = detail_response.json()
                    if detail_data.get("meals"):
                        transformed = self.transform_meal(detail_data["meals"][0])
                        new_meals.append(transformed)
            
            # LOAD - Add to meals and save to CSV
            existing_ids = [m["id"] for m in self.meals]
            added_count = 0
            
            for meal in new_meals:
                if meal["id"] not in existing_ids:
                    self.meals.append(meal)
                    existing_ids.append(meal["id"])
                    added_count += 1
            
            # Save to CSV
            self.save_to_csv()
            
            # Update UI
            self.display_meals()
            self.status_label.config(text=f"Meals: {len(self.meals)}")
            
            messagebox.showinfo("Success", 
                              f"ETL Complete\nAdded {added_count} new meals")
            
        except Exception as e:
            self.status_label.config(text=f"Meals: {len(self.meals)}")
            messagebox.showerror("Error", f"ETL failed: {str(e)}")
    
    def transform_meal(self, meal_data):
        """Transform raw meal data"""
        ingredients = []
        for i in range(1, 11):  # First 10 ingredients only
            ing = meal_data.get(f"strIngredient{i}", "").strip()
            measure = meal_data.get(f"strMeasure{i}", "").strip()
            if ing and ing.lower() != "null":
                ingredients.append(f"{measure} {ing}".strip())
        
        instructions = meal_data.get("strInstructions", "")
        if len(instructions) > 150:
            instructions = instructions[:147] + "..."
        
        return {
            "id": meal_data.get("idMeal", ""),
            "name": meal_data.get("strMeal", "").strip(),
            "category": meal_data.get("strCategory", "").strip(),
            "area": meal_data.get("strArea", "").strip(),
            "instructions": instructions,
            "image": meal_data.get("strMealThumb", ""),
            "ingredients": ", ".join(ingredients[:3])  # First 3 ingredients
        }
    
    def save_to_csv(self):
        """Save meals to CSV"""
        if self.meals:
            df = pd.DataFrame(self.meals)
            csv_path = os.path.join(self.csv_folder, "meals.csv")
            df.to_csv(csv_path, index=False)
    
    def load_existing_data(self):
        """Load meals from CSV"""
        csv_path = os.path.join(self.csv_folder, "meals.csv")
        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
            try:
                df = pd.read_csv(csv_path)
                self.meals = df.to_dict('records')
            except:
                self.meals = []
    
    def display_meals(self):
        """Display all meals"""
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        if not self.meals:
            tk.Label(self.meals_container, 
                    text="No meals available\nRun ETL to get meals",
                    font=("Arial", 14),
                    bg="#f0f8ff", fg="#666666").pack(pady=50)
            return
        
        for i, meal in enumerate(self.meals):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(self.meals_container, bg="white",
                            relief="solid", borderwidth=1)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            self.meals_container.grid_columnconfigure(col, weight=1)
            
            # Meal name
            name = meal["name"]
            if len(name) > 25:
                name = name[:22] + "..."
            
            tk.Label(frame, text=name, 
                    font=("Arial", 12, "bold"),
                    bg="white", wraplength=250).pack(pady=10, padx=10)
            
            # Category and area
            tk.Label(frame, text=f"{meal['category']} | {meal['area']}",
                    font=("Arial", 10),
                    bg="white").pack(pady=5)
            
            # Ingredients preview
            ingredients = meal["ingredients"]
            if len(ingredients) > 40:
                ingredients = ingredients[:37] + "..."
            
            tk.Label(frame, text=ingredients,
                    font=("Arial", 9),
                    bg="white", wraplength=250).pack(pady=8, padx=10)
            
            # View button
            tk.Button(frame, text="View Details",
                     command=lambda m=meal: self.show_details(m),
                     bg="#4a90e2", fg="white").pack(pady=10)
    
    def filter_meals(self):
        """Filter meals based on search"""
        query = self.search_var.get().lower()
        
        for widget in self.meals_container.winfo_children():
            widget.destroy()
        
        if not query:
            self.display_meals()
            return
        
        filtered = []
        for meal in self.meals:
            if (query in meal["name"].lower() or 
                query in meal["category"].lower()):
                filtered.append(meal)
        
        if not filtered:
            tk.Label(self.meals_container, 
                    text=f"No meals found for '{query}'",
                    font=("Arial", 14),
                    bg="#f0f8ff").pack(pady=50)
            return
        
        for i, meal in enumerate(filtered):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(self.meals_container, bg="white",
                            relief="solid", borderwidth=1)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            self.meals_container.grid_columnconfigure(col, weight=1)
            
            name = meal["name"]
            if len(name) > 25:
                name = name[:22] + "..."
            
            tk.Label(frame, text=name, 
                    font=("Arial", 12, "bold"), bg="white").pack(pady=10)
            
            tk.Label(frame, text=f"{meal['category']} | {meal['area']}",
                    font=("Arial", 10), bg="white").pack(pady=5)
            
            tk.Button(frame, text="View Details",
                     command=lambda m=meal: self.show_details(m),
                     bg="#4a90e2", fg="white").pack(pady=10)
    
    def show_details(self, meal):
        """Show meal details"""
        details_win = tk.Toplevel(self.root)
        details_win.title(meal["name"])
        details_win.geometry("500x500")
        details_win.configure(bg="white")
        
        tk.Label(details_win, text=meal["name"], 
                font=("Arial", 18, "bold"),
                bg="white").pack(pady=20)
        
        tk.Label(details_win, 
                text=f"Category: {meal['category']}\nArea: {meal['area']}",
                font=("Arial", 12),
                bg="white").pack(pady=10)
        
        tk.Label(details_win, text="Ingredients:",
                font=("Arial", 14, "bold"),
                bg="white").pack(pady=10)
        
        ingredients = meal["ingredients"].split(", ")
        for ing in ingredients:
            tk.Label(details_win, text=f"- {ing}",
                    font=("Arial", 11),
                    bg="white", anchor="w").pack(fill="x", padx=30)
        
        tk.Label(details_win, text="Instructions:",
                font=("Arial", 14, "bold"),
                bg="white").pack(pady=10)
        
        text_widget = tk.Text(details_win, wrap="word", 
                             font=("Arial", 10), height=8)
        text_widget.pack(pady=10, padx=20, fill="both", expand=True)
        text_widget.insert("1.0", meal["instructions"])
        text_widget.config(state="disabled")
        
        tk.Button(details_win, text="Close", 
                 command=details_win.destroy,
                 width=15).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMealApp(root)
    root.mainloop()