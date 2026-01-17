import tkinter as tk
from tkinter import ttk, messagebox
import requests
import csv
import pandas as pd
from datetime import datetime
import threading
import os

class SimpleOpenLibraryETL:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Data ETL")
        self.root.geometry("700x550")
        
        # Beautiful Color Scheme
        self.colors = {
            "bg": "#f8f9fa",
            "primary": "#4361ee",
            "secondary": "#3a0ca3",
            "accent": "#f72585",
            "success": "#4cc9f0",
            "card": "#ffffff",
            "text": "#2b2d42"
        }
        
        self.root.configure(bg=self.colors["bg"])
        
        # API URL
        self.api_url = "https://openlibrary.org/search.json"
        
        # Data storage
        self.books_data = []
        
        # Setup GUI
        self.setup_gui()
        
        # Create data folder
        os.makedirs("data", exist_ok=True)
    
    def setup_gui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors["bg"])
        title_frame.pack(pady=20)
        
        tk.Label(
            title_frame,
            text="📚 Book Data ETL Tool",
            font=("Arial", 24, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["bg"]
        ).pack()
        
        tk.Label(
            title_frame,
            text="Extract • Transform • Load from OpenLibrary",
            font=("Arial", 11),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(pady=5)
        
        # Search Card
        card = tk.Frame(self.root, bg=self.colors["card"], relief=tk.RAISED, bd=2)
        card.pack(pady=15, padx=30, fill=tk.X)
        
        tk.Label(
            card,
            text="Search Books",
            font=("Arial", 14, "bold"),
            fg=self.colors["secondary"],
            bg=self.colors["card"]
        ).pack(pady=(15, 10))
        
        # Search input
        input_frame = tk.Frame(card, bg=self.colors["card"])
        input_frame.pack(pady=10, padx=20)
        
        tk.Label(input_frame, text="Search:", bg=self.colors["card"], font=("Arial", 11)).grid(row=0, column=0, padx=5)
        
        self.search_entry = tk.Entry(input_frame, width=30, font=("Arial", 11))
        self.search_entry.grid(row=0, column=1, padx=10)
        
        tk.Label(input_frame, text="Limit:", bg=self.colors["card"], font=("Arial", 11)).grid(row=0, column=2, padx=5)
        
        self.limit_var = tk.StringVar(value="10")
        limit_spin = tk.Spinbox(input_frame, from_=1, to=50, textvariable=self.limit_var, width=8, font=("Arial", 11))
        limit_spin.grid(row=0, column=3, padx=10)
        
        # Buttons Frame
        btn_frame = tk.Frame(card, bg=self.colors["card"])
        btn_frame.pack(pady=15)
        
        # ETL Button
        self.etl_btn = tk.Button(
            btn_frame,
            text="Start ETL Process",
            command=self.start_etl,
            bg=self.colors["primary"],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.etl_btn.pack(side=tk.LEFT, padx=10)
        
        # Load CSV Button
        tk.Button(
            btn_frame,
            text="Load CSV",
            command=self.load_csv,
            bg=self.colors["success"],
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
        
        # Progress Area
        progress_frame = tk.Frame(self.root, bg=self.colors["bg"])
        progress_frame.pack(pady=20, padx=30, fill=tk.X)
        
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to start...",
            font=("Arial", 10),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        )
        self.status_label.pack(anchor=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate', length=300)
        self.progress.pack(pady=10)
        
        # Results Frame
        results_frame = tk.LabelFrame(
            self.root,
            text=" Results ",
            font=("Arial", 12, "bold"),
            fg=self.colors["secondary"],
            bg=self.colors["bg"],
            bd=2
        )
        results_frame.pack(pady=15, padx=30, fill=tk.BOTH, expand=True)
        
        # Treeview for results
        columns = ("Title", "Author", "Year", "Pages")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def start_etl(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Required", "Please enter a search term!")
            return
        
        # Disable button during processing
        self.etl_btn.config(state=tk.DISABLED, text="⏳ Processing...")
        self.progress.start(10)
        self.status_label.config(text=f"Searching for: {query}")
        
        # Run in thread
        thread = threading.Thread(target=self.run_etl, args=(query,))
        thread.daemon = True
        thread.start()
    
    def run_etl(self, query):
        try:
            limit = int(self.limit_var.get())
            
            # 1. EXTRACT
            self.update_status(" Extracting data from OpenLibrary...")
            raw_data = self.extract_from_api(query, limit)
            
            if not raw_data:
                self.show_error("No books found!")
                return
            
            # 2. TRANSFORM
            self.update_status("🔄 Transforming data...")
            transformed_data = self.transform_data(raw_data)
            
            # 3. LOAD
            self.update_status("💾 Saving to CSV...")
            self.save_to_csv(transformed_data)
            
            # Show results
            self.books_data = transformed_data
            self.display_results(transformed_data)
            
            self.update_status(f"✅ ETL Complete! {len(transformed_data)} books saved to data/books.csv")
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
        finally:
            self.progress.stop()
            self.etl_btn.config(state=tk.NORMAL, text="🚀 Start ETL Process")
    
    def extract_from_api(self, query, limit):
        """Step 1: Extract data from API"""
        params = {"q": query, "limit": limit}
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("docs", [])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {e}")
    
    def transform_data(self, raw_books):
        """Step 2: Transform and clean data"""
        transformed = []
        
        for book in raw_books:
            # Clean each book's data
            clean_book = {
                "title": book.get("title", "Unknown")[:100],  # Limit title length
                "author": ", ".join(book.get("author_name", ["Unknown"]))[:50],
                "year": book.get("first_publish_year", "Unknown"),
                "pages": book.get("number_of_pages_median", 0),
                "isbn": book.get("isbn", ["Unknown"])[0] if book.get("isbn") else "Unknown",
                "publisher": ", ".join(book.get("publisher", ["Unknown"]))[:30],
                "subject": ", ".join(book.get("subject", ["General"])[:3])[:50],
                "cover_id": book.get("cover_i", ""),
                "extracted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            transformed.append(clean_book)
        
        return transformed
    
    def save_to_csv(self, data):
        """Step 3: Load data to CSV"""
        filename = "data/books.csv"
        
        # Define CSV columns
        columns = ["title", "author", "year", "pages", "isbn", 
                  "publisher", "subject", "cover_id", "extracted_date"]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
    
    def display_results(self, data):
        """Display results in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert new data
        for book in data[:20]:  # Show first 20
            self.tree.insert("", tk.END, values=(
                book["title"][:40] + ("..." if len(book["title"]) > 40 else ""),
                book["author"][:30] + ("..." if len(book["author"]) > 30 else ""),
                book["year"],
                book["pages"]
            ))
    
    def load_csv(self):
        """Load data from existing CSV"""
        filename = "data/books.csv"
        
        if not os.path.exists(filename):
            messagebox.showinfo("No Data", "Run ETL first to create data file!")
            return
        
        try:
            df = pd.read_csv(filename)
            self.books_data = df.to_dict('records')
            self.display_results(self.books_data)
            self.update_status(f" Loaded {len(self.books_data)} books from CSV")
        except Exception as e:
            self.show_error(f"Failed to load CSV: {e}")
    
    def update_status(self, message):
        """Update status label from thread"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def show_error(self, message):
        """Show error message"""
        self.root.after(0, lambda: self.status_label.config(text=f"❌ {message}"))
        self.root.after(0, lambda: messagebox.showerror("Error", message))

def main():
    root = tk.Tk()
    app = SimpleOpenLibraryETL(root)
    root.mainloop()

if __name__ == "__main__":
    main()