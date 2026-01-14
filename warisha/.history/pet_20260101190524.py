import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import pandas as pd
import json
from datetime import datetime

class MuseumETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Met Museum Art ETL Tool")
        self.root.geometry("800x650")
        self.root.configure(bg="#f8f9fa")
        
        # Data storage
        self.art_data = []
        
        # Departments data (static - no live API needed for dropdown)
        self.departments = [
            "1", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", 
            "13", "14", "15", "16", "17", "18", "19", "21"
        ]
        
        self.department_names = {
            "1": "American Decorative Arts",
            "3": "Ancient Near Eastern Art",
            "4": "Arms and Armor",
            "5": "Arts of Africa, Oceania, and the Americas",
            "6": "Asian Art",
            "7": "The Cloisters",
            "8": "The Costume Institute",
            "9": "Drawings and Prints",
            "10": "Egyptian Art",
            "11": "European Paintings",
            "12": "European Sculpture and Decorative Arts",
            "13": "Greek and Roman Art",
            "14": "Islamic Art",
            "15": "The Robert Lehman Collection",
            "16": "The Libraries",
            "17": "Medieval Art",
            "18": "Musical Instruments",
            "19": "Photographs",
            "21": "Modern and Contemporary Art"
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#4a6572", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🏛️ Met Museum Art ETL", 
                font=("Arial", 24, "bold"), fg="white", bg="#4a6572").pack(pady=30)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f8f9fa", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Control Panel
        control_frame = tk.LabelFrame(main_frame, text=" ETL Process ", 
                                     font=("Arial", 12, "bold"), 
                                     bg="#f8f9fa", fg="#4a6572", padx=15, pady=15)
        control_frame.pack(fill="x", pady=(0, 15))
        
        # Department Selection
        tk.Label(control_frame, text="Select Department:", 
                font=("Arial", 10), bg="#f8f9fa").grid(row=0, column=0, sticky="w", pady=5)
        
        self.dept_var = tk.StringVar()
        self.dept_combo = ttk.Combobox(control_frame, textvariable=self.dept_var, 
                                      values=[f"{id}: {name}" for id, name in self.department_names.items()],
                                      width=50, state="readonly")
        self.dept_combo.grid(row=0, column=1, padx=10, pady=5)
        self.dept_combo.set("1: American Decorative Arts")
        
        # Number of objects
        tk.Label(control_frame, text="Number of Artworks:", 
                font=("Arial", 10), bg="#f8f9fa").grid(row=1, column=0, sticky="w", pady=5)
        
        self.num_var = tk.StringVar(value="10")
        ttk.Spinbox(control_frame, from_=1, to=100, textvariable=self.num_var, 
                   width=15).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(control_frame, bg="#f8f9fa")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="📥 Extract Data", 
                  command=self.extract_data, width=15).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Transform Data", 
                  command=self.transform_data, width=15).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="💾 Save to CSV", 
                  command=self.save_to_csv, width=15).pack(side="left", padx=5)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready to start ETL process")
        self.status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                                  bg="#e9ecef", fg="#495057", font=("Arial", 10),
                                  relief="sunken", anchor="w", padx=10)
        self.status_bar.pack(fill="x", pady=(10, 0))
        
        # Data Display Area
        display_frame = tk.LabelFrame(main_frame, text=" Art Data Preview ", 
                                     font=("Arial", 12, "bold"), 
                                     bg="#f8f9fa", fg="#4a6572", padx=15, pady=15)
        display_frame.pack(fill="both", expand=True)
        
        # Create Treeview
        self.create_treeview(display_frame)
        
    def create_treeview(self, parent):
        # Create scrollbars
        v_scroll = ttk.Scrollbar(parent)
        v_scroll.pack(side="right", fill="y")
        
        h_scroll = ttk.Scrollbar(parent, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")
        
        # Create treeview
        self.tree = ttk.Treeview(parent, 
                                columns=("ID", "Title", "Artist", "Date", "Department", "Popularity"),
                                show="headings",
                                yscrollcommand=v_scroll.set,
                                xscrollcommand=h_scroll.set)
        
        # Configure scrollbars
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)
        
        # Define headings
        self.tree.heading("ID", text="Object ID")
        self.tree.heading("Title", text="Artwork Title")
        self.tree.heading("Artist", text="Artist")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Popularity", text="Popularity")
        
        # Define columns
        self.tree.column("ID", width=80)
        self.tree.column("Title", width=200)
        self.tree.column("Artist", width=150)
        self.tree.column("Date", width=100)
        self.tree.column("Department", width=150)
        self.tree.column("Popularity", width=100)
        
        self.tree.pack(fill="both", expand=True)
    
    def extract_data(self):
        """Extract data from Met Museum API"""
        try:
            # Get selected department
            dept_selection = self.dept_var.get()
            dept_id = dept_selection.split(":")[0].strip()
            num_objects = int(self.num_var.get())
            
            self.status_var.set(f"Extracting data from Department {dept_id}...")
            self.root.update()
            
            # API endpoint for objects by department
            url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects"
            
            # First get object IDs for the department
            params = {'departmentIds': dept_id}
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                messagebox.showerror("Error", "Failed to fetch data from API")
                return
            
            data = response.json()
            object_ids = data.get('objectIDs', [])[:num_objects]
            
            if not object_ids:
                messagebox.showwarning("No Data", "No artworks found for this department")
                return
            
            # Extract detailed data for each object
            self.art_data = []
            for i, obj_id in enumerate(object_ids):
                # Update status
                self.status_var.set(f"Extracting artwork {i+1}/{len(object_ids)}...")
                self.root.update()
                
                # Get object details
                obj_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
                obj_response = requests.get(obj_url)
                
                if obj_response.status_code == 200:
                    obj_data = obj_response.json()
                    
                    # Extract relevant fields
                    artwork = {
                        'objectID': obj_data.get('objectID', ''),
                        'title': obj_data.get('title', 'Unknown Title'),
                        'artist': obj_data.get('artistDisplayName', 'Unknown Artist'),
                        'date': obj_data.get('objectDate', 'Unknown Date'),
                        'department': obj_data.get('department', ''),
                        'culture': obj_data.get('culture', ''),
                        'medium': obj_data.get('medium', ''),
                        'classification': obj_data.get('classification', ''),
                        'isHighlight': obj_data.get('isHighlight', False),
                        'isPublicDomain': obj_data.get('isPublicDomain', False),
                        'primaryImage': obj_data.get('primaryImage', ''),
                        'objectURL': obj_data.get('objectURL', '')
                    }
                    self.art_data.append(artwork)
            
            # Update treeview
            self.update_treeview()
            self.status_var.set(f"✅ Extraction complete! Found {len(self.art_data)} artworks")
            
        except Exception as e:
            messagebox.showerror("Extraction Error", f"Error during extraction: {str(e)}")
            self.status_var.set("❌ Extraction failed")
    
    def transform_data(self):
        """Transform the extracted data"""
        if not self.art_data:
            messagebox.showwarning("No Data", "Please extract data first!")
            return
        
        try:
            self.status_var.set("Transforming data...")
            self.root.update()
            
            # Apply transformations
            for artwork in self.art_data:
                # Clean title
                title = artwork['title']
                if title == '':
                    artwork['title'] = 'Untitled'
                elif len(title) > 50:
                    artwork['title'] = title[:47] + '...'
                
                # Clean artist name
                artist = artwork['artist']
                if artist == '':
                    artwork['artist'] = 'Unknown Artist'
                elif artist.lower() == 'unknown':
                    artwork['artist'] = 'Unknown Artist'
                
                # Clean date
                date = str(artwork['date'])
                if date == '' or date.lower() == 'unknown':
                    artwork['date'] = 'Date Unknown'
                
                # Add popularity score (simple calculation)
                popularity_score = 0
                if artwork['isHighlight']:
                    popularity_score += 10
                if artwork['isPublicDomain']:
                    popularity_score += 5
                if artwork['primaryImage']:
                    popularity_score += 3
                
                # Add derived field
                artwork['popularity'] = popularity_score
                
                # Add department name
                dept_id = artwork['department']
                artwork['department_name'] = self.department_names.get(dept_id, 'Unknown Department')
            
            # Update treeview
            self.update_treeview()
            self.status_var.set("✅ Transformation complete! Data cleaned and enhanced")
            
        except Exception as e:
            messagebox.showerror("Transformation Error", f"Error during transformation: {str(e)}")
            self.status_var.set("❌ Transformation failed")
    
    def update_treeview(self):
        """Update the treeview with current data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new data
        for artwork in self.art_data[:20]:  # Show first 20 records
            self.tree.insert("", "end", values=(
                artwork.get('objectID', ''),
                artwork.get('title', ''),
                artwork.get('artist', ''),
                artwork.get('date', ''),
                artwork.get('department_name', ''),
                artwork.get('popularity', '')
            ))
    
    def save_to_csv(self):
        """Save transformed data to CSV file"""
        if not self.art_data:
            messagebox.showwarning("No Data", "Please extract and transform data first!")
            return
        
        try:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"met_art_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            )
            
            if not filename:
                return
            
            self.status_var.set("Saving data to CSV...")
            self.root.update()
            
            # Convert to DataFrame
            df = pd.DataFrame(self.art_data)
            
            # Select columns for CSV
            csv_columns = [
                'objectID', 'title', 'artist', 'date', 'department_name',
                'culture', 'medium', 'classification', 'popularity',
                'isHighlight', 'isPublicDomain', 'objectURL'
            ]
            
            # Reorder and save
            df = df[[col for col in csv_columns if col in df.columns]]
            df.to_csv(filename, index=False, encoding='utf-8')
            
            self.status_var.set(f"✅ Data saved successfully to: {filename}")
            messagebox.showinfo("Success", f"Data saved to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving CSV: {str(e)}")
            self.status_var.set("❌ Save failed")

def main():
    root = tk.Tk()
    app = MuseumETLApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()