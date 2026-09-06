import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def load_members_data():
    """Load all members from member_info.json"""
    if not os.path.exists("data/member_info.json"):
        return []
    try:
        with open("data/member_info.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading members: {e}")
        return []

def save_members_data(members_data):
    """Save members data back to member_info.json"""
    try:
        with open("data/member_info.json", "w", encoding="utf-8") as f:
            json.dump(members_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving members: {e}")
        return False

class ProgressTracker(ttk.Frame):
    def __init__(self, parent, member):
        super().__init__(parent)
        self.parent = parent
        self.member = member
        
        # Configure style
        self.style = ThemedStyle(self)
        self.style.set_theme("arc")
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configure custom styles"""
        self.style.configure("Title.TLabel", 
                           font=("Helvetica", 24, "bold"),
                           padding=10)
        
        self.style.configure("Header.TLabel",
                           font=("Helvetica", 12, "bold"),
                           padding=5)
        
        self.style.configure("Tab.TNotebook", 
                           background="#ffffff",
                           padding=5)
        
        self.style.configure("Progress.Treeview",
                           font=("Helvetica", 11),
                           rowheight=30)
        
        self.style.configure("Progress.Treeview.Heading",
                           font=("Helvetica", 12, "bold"))
        
    def create_widgets(self):
        """Create all widgets"""
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(title_frame, text="My Progress Tracking", 
                 style="Title.TLabel").pack(side=tk.LEFT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self, style="Tab.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.workout_tab = ttk.Frame(self.notebook, padding=20)
        self.stats_tab = ttk.Frame(self.notebook, padding=20)
        
        self.notebook.add(self.workout_tab, text="Workout Log")
        self.notebook.add(self.stats_tab, text="Body Stats")
        
        # Setup each tab
        self.setup_workout_tab()
        self.setup_stats_tab()
        
    def setup_workout_tab(self):
        """Setup the workout log tab"""
        # History view
        history_frame = ttk.LabelFrame(self.workout_tab, text="Workout History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create treeview for history
        columns = ("Date", "Workout Details")
        self.workout_tree = ttk.Treeview(history_frame, columns=columns, 
                                       show="headings", style="Progress.Treeview")
        
        # Configure columns
        self.workout_tree.heading("Date", text="Date")
        self.workout_tree.heading("Workout Details", text="Workout Details")
        
        self.workout_tree.column("Date", width=150, anchor="center")
        self.workout_tree.column("Workout Details", width=600)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(history_frame, orient="vertical", 
                           command=self.workout_tree.yview)
        hsb = ttk.Scrollbar(history_frame, orient="horizontal", 
                           command=self.workout_tree.xview)
        self.workout_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.workout_tree.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")
        
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(0, weight=1)
        
        # New entry area
        entry_frame = ttk.LabelFrame(self.workout_tab, text="Add Today's Workout", padding=10)
        entry_frame.pack(fill=tk.X)
        
        # Workout details entry
        self.workout_text = tk.Text(entry_frame, height=4, wrap=tk.WORD)
        self.workout_text.pack(fill=tk.X, pady=10)
        
        # Save button
        save_btn = ttk.Button(entry_frame, text="Save Workout", command=self.save_workout)
        save_btn.pack(anchor="e")
        
        # Load initial data
        self.refresh_workout_history()
        
    def setup_stats_tab(self):
        """Setup the body stats tab"""
        # Graph area
        graph_frame = ttk.LabelFrame(self.stats_tab, text="Weight Progress", padding=10)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create figure for graph
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.plot = self.figure.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # New entry area
        entry_frame = ttk.LabelFrame(self.stats_tab, text="Add Today's Stats", padding=10)
        entry_frame.pack(fill=tk.X)
        
        # Weight entry
        weight_frame = ttk.Frame(entry_frame)
        weight_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(weight_frame, text="Weight (kg):", 
                 style="Header.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        
        self.weight_var = tk.StringVar()
        weight_entry = ttk.Entry(weight_frame, textvariable=self.weight_var, width=10)
        weight_entry.pack(side=tk.LEFT)
        
        # Body fat entry (optional)
        fat_frame = ttk.Frame(entry_frame)
        fat_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fat_frame, text="Body Fat (%):", 
                 style="Header.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        
        self.fat_var = tk.StringVar()
        fat_entry = ttk.Entry(fat_frame, textvariable=self.fat_var, width=10)
        fat_entry.pack(side=tk.LEFT)
        
        # Save button
        save_btn = ttk.Button(entry_frame, text="Save Stats", command=self.save_stats)
        save_btn.pack(anchor="e", pady=(10, 0))
        
        # Load initial data and update graph
        self.refresh_stats()
        
    def refresh_workout_history(self):
        """Refresh the workout history display"""
        # Clear existing items
        for item in self.workout_tree.get_children():
            self.workout_tree.delete(item)
            
        # Get member data
        all_members = load_members_data()
        member_data = next((m for m in all_members 
                        if m.get("username") == self.member.username), None)
        
        if not member_data:
            return
            
        # Display workout history
        workout_days = member_data.get("workout_days", [])
        for i, (date, details) in enumerate(workout_days):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.workout_tree.insert("", "end", values=(date, details), tags=(tag,))
            
        # Configure row colors
        self.workout_tree.tag_configure("evenrow", background="#FFFFFF")
        self.workout_tree.tag_configure("oddrow", background="#F5F5F5")
        
    def save_workout(self):
        """Save new workout entry"""
        details = self.workout_text.get("1.0", tk.END).strip()
        
        if not details:
            messagebox.showerror("Error", "Please enter workout details!")
            return
            
        # Get today's date
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Update member data
        all_members = load_members_data()
        member_index = next((i for i, m in enumerate(all_members) 
                         if m.get("username") == self.member.username), None)
        
        if member_index is None:
            messagebox.showerror("Error", "Member data not found!")
            return
            
        # Add new workout entry
        if "workout_days" not in all_members[member_index]:
            all_members[member_index]["workout_days"] = []
            
        all_members[member_index]["workout_days"].append([date, details])
        
        # Sort workout days by date
        all_members[member_index]["workout_days"].sort(key=lambda x: x[0])
        
        # Save changes
        if save_members_data(all_members):
            messagebox.showinfo("Success", "Workout entry added successfully!")
            self.workout_text.delete("1.0", tk.END)  # Clear entry
            self.refresh_workout_history()  # Refresh display
        else:
            messagebox.showerror("Error", "Failed to save workout entry!")
            
    def refresh_stats(self):
        """Refresh the stats display and graph"""
        # Get member data
        all_members = load_members_data()
        member_data = next((m for m in all_members 
                        if m.get("username") == self.member.username), None)
        
        if not member_data or "body_stats" not in member_data:
            return
            
        # Prepare data for plotting
        dates = []
        weights = []
        
        for stat in member_data["body_stats"]:
            dates.append(datetime.strptime(stat["date"], "%Y-%m-%d"))
            weights.append(float(stat["weight"]))
            
        # Clear previous plot
        self.plot.clear()
        
        # Create new plot
        if dates and weights:
            self.plot.plot(dates, weights, 'b-o')
            self.plot.set_xlabel('Date')
            self.plot.set_ylabel('Weight (kg)')
            self.plot.grid(True)
            plt.setp(self.plot.xaxis.get_majorticklabels(), rotation=45)
            self.figure.tight_layout()
            
        # Update canvas
        self.canvas.draw()
        
    def save_stats(self):
        """Save new body stats entry"""
        try:
            weight = float(self.weight_var.get())
            if weight <= 0:
                raise ValueError("Weight must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid weight!")
            return
            
        try:
            fat = self.fat_var.get()
            if fat:
                fat = float(fat)
                if fat < 0 or fat > 100:
                    raise ValueError("Body fat percentage must be between 0 and 100")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid body fat percentage!")
            return
            
        # Get today's date
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Update member data
        all_members = load_members_data()
        member_index = next((i for i, m in enumerate(all_members) 
                         if m.get("username") == self.member.username), None)
        
        if member_index is None:
            messagebox.showerror("Error", "Member data not found!")
            return
            
        # Create new stats entry
        stats_entry = {"date": date, "weight": weight}
        if fat:
            stats_entry["body_fat"] = fat
            
        # Add new stats entry
        if "body_stats" not in all_members[member_index]:
            all_members[member_index]["body_stats"] = []
            
        all_members[member_index]["body_stats"].append(stats_entry)
        
        # Sort stats by date
        all_members[member_index]["body_stats"].sort(key=lambda x: x["date"])
        
        # Save changes
        if save_members_data(all_members):
            messagebox.showinfo("Success", "Body stats added successfully!")
            self.weight_var.set("")  # Clear entries
            self.fat_var.set("")
            self.refresh_stats()  # Refresh display
        else:
            messagebox.showerror("Error", "Failed to save body stats!")

def on_track_progress(root, member):
    # Configure window
    root.title("My Progress Tracking")
    
    # Create and pack the tracker
    tracker = ProgressTracker(root, member)
    tracker.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Back button
    back_btn = ttk.Button(root, text="Back to Menu", command=root.destroy)
    back_btn.pack(pady=10)