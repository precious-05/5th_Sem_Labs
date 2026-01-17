import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import csv
import pandas as pd
from datetime import datetime
import threading
import time
import os

class OpenLibraryETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenLibrary ETL Application")
        self.root.geometry("900x700")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        # API endpoints
        self.search_url = "https://openlibrary.org/search.json"
        self.works_url = "https://openlibrary.org/works/"
        
        # Create GUI
        self.create_widgets()
        
        # Create data directory if not exists
        if not os.path.exists('data'):
            os.makedirs('data')
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="OpenLibrary ETL Application", 
            font=("Helvetica", 24, "bold"),
            fg=self.primary_color,
            bg=self.bg_color
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Search Section
        search_frame = ttk.LabelFrame(main_frame, text="Search Books", padding="15")
        search_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Search options
        ttk.Label(search_frame, text="Search Type:").grid(row=0, column=0, padx=(0, 5))
        
        self.search_type = tk.StringVar(value="title")
        search_type_combo = ttk.Combobox(
            search_frame, 
            textvariable=self.search_type,
            values=["title", "author", "subject", "isbn"],
            width=15,
            state="readonly"
        )
        search_type_combo.grid(row=0, column=1, padx=(0, 15))
        
        ttk.Label(search_frame, text="Search Query:").grid(row=0, column=2, padx=(0, 5))
        self.search_query = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_query, width=30)
        search_entry.grid(row=0, column=3, padx=(0, 15))
        
        ttk.Label(search_frame, text="Max Results:").grid(row=0, column=4, padx=(0, 5))
        self.max_results = tk.IntVar(value=10)
        max_results_spin = ttk.Spinbox(
            search_frame, 
            textvariable=self.max_results,
            from_=1, 
            to=100,
            width=10
        )
        max_results_spin.grid(row=0, column=5)
        
        # Search button
        search_btn = ttk.Button(
            search_frame, 
            text="Search & Extract", 
            command=self.start_etl_process,
            style="Accent.TButton"
        )
        search_btn.grid(row=0, column=6, padx=(15, 0))
        
        # ETL Process Frame
        etl_frame = ttk.LabelFrame(main_frame, text="ETL Process Status", padding="15")
        etl_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Progress bar
        self.progress = ttk.Progressbar(etl_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status labels
        self.status_label = ttk.Label(etl_frame, text="Ready to start ETL process...")
        self.status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        self.result_label = ttk.Label(etl_frame, text="")
        self.result_label.grid(row=2, column=0, columnspan=3, sticky=tk.W)
        
        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="ETL Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=12,
            width=100,
            font=("Consolas", 10)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Data Preview Frame
        preview_frame = ttk.LabelFrame(main_frame, text="Data Preview", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview for data preview
        self.tree = ttk.Treeview(preview_frame, height=8)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars for treeview
        vsb = ttk.Scrollbar(preview_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(15, 0))
        
        ttk.Button(
            button_frame, 
            text="Load CSV Data", 
            command=self.load_csv_data
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Clear Log", 
            command=self.clear_log
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Export to CSV", 
            command=self.export_to_csv
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Exit", 
            command=self.root.quit
        ).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Configure styles
        self.style.configure('Accent.TButton', background=self.accent_color, foreground='white')
        
        # Data storage
        self.books_data = []
        self.dataframe = None
        
        # Initial log message
        self.log("Application started. Ready to perform ETL operations.")
    
    def log(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)
        self.log("Log cleared.")
    
    def start_etl_process(self):
        """Start the ETL process in a separate thread"""
        query = self.search_query.get().strip()
        
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search query")
            return
        
        # Disable search button during processing
        self.search_btn_state = tk.DISABLED
        
        # Start progress bar
        self.progress.start(10)
        self.status_label.config(text=f"Processing: Searching for '{query}'...")
        
        # Start ETL in separate thread
        thread = threading.Thread(target=self.perform_etl, args=(query,))
        thread.daemon = True
        thread.start()
    
    def perform_etl(self, query):
        """Perform the complete ETL process"""
        try:
            # Step 1: EXTRACT - Fetch data from API
            self.log(f"EXTRACT: Fetching data from OpenLibrary API for query: '{query}'")
            books = self.extract_data_from_api(query)
            
            if not books:
                self.log("ERROR: No data fetched from API. Check your query or try again.")
                self.progress.stop()
                self.status_label.config(text="Error: No data found")
                return
            
            # Step 2: TRANSFORM - Process the data
            self.log(f"TRANSFORM: Processing {len(books)} books")
            transformed_data = self.transform_data(books)
            
            # Step 3: LOAD - Save to CSV
            self.log(f"LOAD: Saving {len(transformed_data)} records to CSV")
            self.load_data_to_csv(transformed_data)
            
            # Update UI
            self.books_data = transformed_data
            self.dataframe = pd.DataFrame(transformed_data)
            
            # Display data in treeview
            self.display_data_in_treeview()
            
            # Update status
            self.progress.stop()
            self.status_label.config(text="ETL process completed successfully!")
            self.result_label.config(text=f"Results: {len(transformed_data)} books processed and saved to 'books_data.csv'")
            
            self.log("ETL process completed successfully!")
            
        except Exception as e:
            self.log(f"ERROR in ETL process: {str(e)}")
            self.progress.stop()
            self.status_label.config(text=f"Error: {str(e)}")
    
    def extract_data_from_api(self, query):
        """Extract data from OpenLibrary API"""
        books = []
        max_results = self.max_results.get()
        search_type = self.search_type.get()
        
        # Build search parameters
        params = {search_type: query, "limit": max_results}
        
        try:
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            docs = data.get("docs", [])
            
            self.log(f"EXTRACT: Found {len(docs)} books from API")
            
            # Get detailed information for each book (limited to max_results)
            for i, doc in enumerate(docs[:max_results]):
                book_info = self.get_book_details(doc)
                if book_info:
                    books.append(book_info)
                    self.log(f"  Extracted: {book_info.get('title', 'Unknown')}")
                
                # Update status periodically
                if i % 5 == 0:
                    self.status_label.config(text=f"Extracting: {i+1}/{min(len(docs), max_results)} books...")
        
        except requests.exceptions.RequestException as e:
            self.log(f"ERROR: Failed to fetch data from API: {e}")
            return []
        
        return books
    
    def get_book_details(self, doc):
        """Get detailed information for a book"""
        try:
            # Basic book information
            book = {
                "title": doc.get("title", "Unknown"),
                "author": ", ".join(doc.get("author_name", ["Unknown"])) if doc.get("author_name") else "Unknown",
                "first_publish_year": doc.get("first_publish_year", "Unknown"),
                "publish_year": doc.get("publish_year", ["Unknown"])[0] if doc.get("publish_year") else "Unknown",
                "isbn": doc.get("isbn", ["Unknown"])[0] if doc.get("isbn") else "Unknown",
                "language": ", ".join(doc.get("language", ["Unknown"])) if doc.get("language") else "Unknown",
                "subject": ", ".join(doc.get("subject", ["Unknown"])[:3]) if doc.get("subject") else "Unknown",
                "publisher": ", ".join(doc.get("publisher", ["Unknown"])) if doc.get("publisher") else "Unknown",
                "pages": doc.get("number_of_pages_median", "Unknown"),
                "edition_count": doc.get("edition_count", 0),
                "cover_id": doc.get("cover_i", "None"),
                "key": doc.get("key", "").replace("/works/", ""),
                "extracted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Get additional details if work key is available
            work_key = doc.get("key")
            if work_key:
                try:
                    work_response = requests.get(f"https://openlibrary.org{work_key}.json")
                    if work_response.status_code == 200:
                        work_data = work_response.json()
                        book["description"] = work_data.get("description", "No description available")
                        if isinstance(book["description"], dict):
                            book["description"] = book["description"].get("value", "No description available")
                        
                        # Get average rating if available
                        book["rating"] = work_data.get("rating", {}).get("average", "No rating")
                except:
                    book["description"] = "No description available"
                    book["rating"] = "No rating"
            else:
                book["description"] = "No description available"
                book["rating"] = "No rating"
            
            return book
        
        except Exception as e:
            self.log(f"WARNING: Could not extract full details for a book: {e}")
            return None
    
    def transform_data(self, books):
        """Transform and clean the extracted data"""
        transformed_books = []
        
        for book in books:
            if book:  # Only process valid books
                # Clean and transform fields
                transformed_book = {}
                
                # Title - capitalize first letter of each word
                title = book.get("title", "Unknown")
                transformed_book["title"] = title.title() if title != "Unknown" else title
                
                # Author - ensure proper formatting
                author = book.get("author", "Unknown")
                transformed_book["author"] = author
                
                # Year - handle missing values
                year = book.get("first_publish_year", book.get("publish_year", "Unknown"))
                transformed_book["year"] = year if year else "Unknown"
                
                # ISBN - get first ISBN
                isbn = book.get("isbn", "Unknown")
                if isinstance(isbn, list):
                    isbn = isbn[0] if isbn else "Unknown"
                transformed_book["isbn"] = isbn
                
                # Language - get first language
                language = book.get("language", "Unknown")
                if isinstance(language, list):
                    language = language[0] if language else "Unknown"
                transformed_book["language"] = language
                
                # Subject - limit to 3 subjects
                subject = book.get("subject", "Unknown")
                if isinstance(subject, list):
                    subject = ", ".join(subject[:3])
                transformed_book["subject"] = subject
                
                # Publisher - get first publisher
                publisher = book.get("publisher", "Unknown")
                if isinstance(publisher, list):
                    publisher = publisher[0] if publisher else "Unknown"
                transformed_book["publisher"] = publisher
                
                # Pages - ensure numeric
                pages = book.get("pages", 0)
                transformed_book["pages"] = pages if isinstance(pages, int) else 0
                
                # Edition count
                transformed_book["edition_count"] = book.get("edition_count", 0)
                
                # Description - truncate if too long
                description = book.get("description", "No description available")
                if len(description) > 200:
                    description = description[:200] + "..."
                transformed_book["description"] = description
                
                # Rating
                transformed_book["rating"] = book.get("rating", "No rating")
                
                # Cover URL
                cover_id = book.get("cover_id")
                if cover_id and cover_id != "None":
                    transformed_book["cover_url"] = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                else:
                    transformed_book["cover_url"] = "No cover available"
                
                # Key and extracted date
                transformed_book["key"] = book.get("key", "")
                transformed_book["extracted_date"] = book.get("extracted_date", "")
                
                transformed_books.append(transformed_book)
        
        self.log(f"TRANSFORM: Processed {len(transformed_books)} books after transformation")
        return transformed_books
    
    def load_data_to_csv(self, books):
        """Load transformed data to CSV file"""
        if not books:
            self.log("WARNING: No data to save to CSV")
            return
        
        filename = "data/books_data.csv"
        
        # Define field names
        fieldnames = [
            "title", "author", "year", "isbn", "language", "subject",
            "publisher", "pages", "edition_count", "description",
            "rating", "cover_url", "key", "extracted_date"
        ]
        
        try:
            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(books)
            
            self.log(f"LOAD: Data successfully saved to {filename}")
            
        except Exception as e:
            self.log(f"ERROR: Failed to save data to CSV: {e}")
            raise
    
    def display_data_in_treeview(self):
        """Display data in treeview widget"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Configure columns
        self.tree["columns"] = ("Title", "Author", "Year", "Language", "Pages")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Title", width=250, anchor=tk.W)
        self.tree.column("Author", width=200, anchor=tk.W)
        self.tree.column("Year", width=80, anchor=tk.CENTER)
        self.tree.column("Language", width=100, anchor=tk.W)
        self.tree.column("Pages", width=80, anchor=tk.CENTER)
        
        # Create headings
        self.tree.heading("Title", text="Title", anchor=tk.W)
        self.tree.heading("Author", text="Author", anchor=tk.W)
        self.tree.heading("Year", text="Year", anchor=tk.CENTER)
        self.tree.heading("Language", text="Language", anchor=tk.W)
        self.tree.heading("Pages", text="Pages", anchor=tk.CENTER)
        
        # Insert data
        for i, book in enumerate(self.books_data[:20]):  # Show first 20 records
            self.tree.insert(
                "", 
                tk.END, 
                values=(
                    book.get("title", "")[:50] + ("..." if len(book.get("title", "")) > 50 else ""),
                    book.get("author", "")[:30] + ("..." if len(book.get("author", "")) > 30 else ""),
                    book.get("year", ""),
                    book.get("language", ""),
                    book.get("pages", 0)
                )
            )
        
        self.log(f"Displaying {min(len(self.books_data), 20)} records in preview")
    
    def load_csv_data(self):
        """Load data from CSV file"""
        filename = "data/books_data.csv"
        
        if not os.path.exists(filename):
            messagebox.showinfo("File Not Found", f"No data file found at {filename}. Please run ETL first.")
            return
        
        try:
            self.dataframe = pd.read_csv(filename)
            self.books_data = self.dataframe.to_dict('records')
            
            # Display in treeview
            self.display_data_in_treeview()
            
            # Update status
            self.status_label.config(text=f"Data loaded from CSV: {len(self.books_data)} records")
            self.result_label.config(text=f"Loaded from: {filename}")
            
            self.log(f"Loaded {len(self.books_data)} records from {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")
            self.log(f"ERROR loading CSV: {e}")
    
    def export_to_csv(self):
        """Export current data to a new CSV file"""
        if not self.books_data:
            messagebox.showwarning("No Data", "No data to export. Please run ETL first.")
            return
        
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/books_export_{timestamp}.csv"
            
            # Create DataFrame and save
            df = pd.DataFrame(self.books_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            
            self.log(f"Data exported to {filename}")
            messagebox.showinfo("Export Successful", f"Data exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {e}")
            self.log(f"ERROR exporting: {e}")

def main():
    root = tk.Tk()
    app = OpenLibraryETLApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()