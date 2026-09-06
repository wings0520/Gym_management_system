import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import json
import os
from datetime import datetime
from tkcalendar import DateEntry

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
            
        # Notify other users of the update (could be extended to real-time notifications)
        try:
            with open("data/progress_updates.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()}: Progress updated\n")
        except:
            pass # Ignore notification errors
            
        return True
    except Exception as e:
        print(f"Error saving members: {e}")
        return False

def load_trainer_members(trainer_username):
    """Get list of members assigned to a specific trainer"""
    if not os.path.exists("data/trainer_info.json"):
        return []
    try:
        with open("data/trainer_info.json", "r", encoding="utf-8") as f:
            trainers = json.load(f)
            for trainer in trainers:
                if trainer.get("username") == trainer_username:
                    return trainer.get("member_username", [])
    except Exception as e:
        print(f"Error loading trainer members: {e}")
    return []

def on_track_member_progress(root, trainer):
    # Configure modern style theme
    style = ThemedStyle(root)
    style.set_theme("arc")

    # Configure custom styles
    style.configure("Title.TLabel", 
                   font=("Helvetica", 24, "bold"),
                   padding=10)
    
    style.configure("Header.TLabel",
                   font=("Helvetica", 12, "bold"),
                   padding=5)
    
    style.configure("Content.TLabel",
                   font=("Helvetica", 11),
                   padding=3)
    
    style.configure("Progress.Treeview",
                   font=("Helvetica", 11),
                   rowheight=30)
    
    style.configure("Progress.Treeview.Heading",
                   font=("Helvetica", 12, "bold"))

    # Set window title
    root.title("Member Progress Tracking")
    
    # Create main container with padding
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(fill=tk.X, pady=(0, 20))
    ttk.Label(title_frame, text="Member Progress Tracking", 
             style="Title.TLabel").pack(side=tk.LEFT)
    
    # Member selection area
    select_frame = ttk.LabelFrame(main_frame, text="Select Member", padding="10")
    select_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Get filtered member list based on trainer's role
    all_members = load_members_data()
    trainer_username = getattr(trainer, "username", trainer)
    
    if hasattr(trainer, "role") and trainer.role == "admin":
        filtered_members = all_members
    else:
        allowed_members = load_trainer_members(trainer_username)

        def member_matches_trainer_list(member, trainer_list):
            uname = (member.get("username") or "").strip()
            full_name = f"{member.get('f_name','')} {member.get('l_name','')}".strip()
            alt_name = (member.get("name") or "").strip()
            return (uname in trainer_list) or (full_name in trainer_list) or (alt_name in trainer_list)

        filtered_members = [m for m in all_members if member_matches_trainer_list(m, allowed_members)]
    
    # Create member selection combobox
    member_var = tk.StringVar()
    member_names = [(f"{m.get('f_name', '')} {m.get('l_name', '')} ({m.get('username', '')})", 
                    m.get('username', '')) for m in filtered_members]
    member_names.sort()  # Sort alphabetically
    
    ttk.Label(select_frame, text="Select Member:", 
             style="Header.TLabel").pack(side=tk.LEFT, padx=(0, 10))
    
    member_combo = ttk.Combobox(select_frame, 
                               textvariable=member_var,
                               values=[name[0] for name in member_names],
                               state="readonly",
                               width=50)
    member_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Progress history view
    history_frame = ttk.LabelFrame(main_frame, text="Workout History", padding="10")
    history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    # Create treeview for history
    columns = ("Date", "Workout Details")
    tree = ttk.Treeview(history_frame, columns=columns, show="headings",
                      selectmode="browse", style="Progress.Treeview")
    
    # Configure columns
    tree.heading("Date", text="Date")
    tree.heading("Workout Details", text="Workout Details")
    
    tree.column("Date", width=150, anchor="center")
    tree.column("Workout Details", width=600)
    
    # Add scrollbars
    vsb = ttk.Scrollbar(history_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(history_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Grid layout for treeview and scrollbars
    tree.grid(column=0, row=0, sticky="nsew")
    vsb.grid(column=1, row=0, sticky="ns")
    hsb.grid(column=0, row=1, sticky="ew")
    
    history_frame.grid_columnconfigure(0, weight=1)
    history_frame.grid_rowconfigure(0, weight=1)
    
    # Add new workout entry
    entry_frame = ttk.LabelFrame(main_frame, text="Add New Workout", padding="10")
    entry_frame.pack(fill=tk.X)
    
    # Date picker
    date_frame = ttk.Frame(entry_frame)
    date_frame.pack(fill=tk.X, pady=(0, 10))
    
    ttk.Label(date_frame, text="Date:", 
             style="Header.TLabel").pack(side=tk.LEFT, padx=(0, 10))
    
    date_picker = DateEntry(date_frame, width=12, background='darkblue',
                          foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_picker.pack(side=tk.LEFT)
    
    # Workout details entry
    details_frame = ttk.Frame(entry_frame)
    details_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(details_frame, text="Workout Details:", 
             style="Header.TLabel").pack(anchor="w")
    
    details_text = tk.Text(details_frame, height=4, wrap=tk.WORD)
    details_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
    
    def refresh_history():
        """Refresh the workout history display"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        # Get selected member's username
        selected = member_var.get()
        if not selected:
            return
            
        username = next((name[1] for name in member_names if name[0] == selected), None)
        if not username:
            return
            
        # Find member's workout history
        member = next((m for m in load_members_data() 
                    if m.get("username") == username), None)
        if not member:
            return
            
        # Display workout history
        workout_days = member.get("workout_days", [])
        for i, (date, details) in enumerate(workout_days):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=(date, details), tags=(tag,))
            
        # Configure row colors
        tree.tag_configure("evenrow", background="#FFFFFF")
        tree.tag_configure("oddrow", background="#F5F5F5")
    
    def add_workout():
        """Add a new workout entry"""
        # Validate member selection
        selected = member_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a member first!")
            return
            
        # Get member username
        username = next((name[1] for name in member_names if name[0] == selected), None)
        if not username:
            return
            
        # Get workout details
        date = date_picker.get_date().strftime("%Y-%m-%d")
        details = details_text.get("1.0", tk.END).strip()
        
        if not details:
            messagebox.showerror("Error", "Please enter workout details!")
            return
            
        # Update member data
        all_members = load_members_data()
        member_index = next((i for i, m in enumerate(all_members) 
                         if m.get("username") == username), None)
        
        if member_index is None:
            messagebox.showerror("Error", "Member not found!")
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
            details_text.delete("1.0", tk.END)  # Clear entry
            refresh_history()  # Refresh display
        else:
            messagebox.showerror("Error", "Failed to save workout entry!")
    
    # Add Save button
    save_btn = ttk.Button(entry_frame, text="Save Workout", command=add_workout)
    save_btn.pack(anchor="e")
    
    # Bind member selection to refresh history
    member_combo.bind("<<ComboboxSelected>>", lambda e: refresh_history())
    
    # Back button
    back_btn = ttk.Button(main_frame, text="Back to Menu", command=root.destroy)
    back_btn.pack(pady=(20, 0))