import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import json
import os

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

def on_view_member_info(root, trainer):
    # Initialize field_vars at function scope
    field_vars = {}

    # Configure modern style theme
    style = ThemedStyle(root)
    style.set_theme("arc")  # Clean, modern theme

    # Configure custom styles
    style.configure("Title.TLabel", 
                   font=("Helvetica", 24, "bold"),
                   padding=10)
    
    style.configure("Header.TLabel",
                   font=("Helvetica", 12, "bold"),
                   padding=5)
    
    style.configure("Search.TEntry",
                   font=("Helvetica", 11),
                   padding=5)
    
    style.configure("MemberList.Treeview",
                   font=("Helvetica", 11),
                   rowheight=30)
    
    style.configure("MemberList.Treeview.Heading",
                   font=("Helvetica", 12, "bold"))
    
    style.configure("Details.TLabelframe",
                   font=("Helvetica", 12, "bold"))
    
    style.configure("Details.TLabel",
                   font=("Helvetica", 11),
                   padding=3)
    
    style.configure("Details.TEntry",
                   font=("Helvetica", 11),
                   padding=5)

    # Set window title
    root.title("Member Information")
    
    # Create main container with modern padding
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title with modern font
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(fill=tk.X, pady=(0, 20))
    ttk.Label(title_frame, text="Member Information", style="Title.TLabel").pack(side=tk.LEFT)
    
    # Split into left and right panes
    paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
    paned.pack(fill=tk.BOTH, expand=True)
    
    # Left pane: Modern search and member list
    left_frame = ttk.LabelFrame(paned, text="Member List", padding="10")
    paned.add(left_frame, weight=1)
    
    # Search bar with icon
    search_frame = ttk.Frame(left_frame)
    search_frame.pack(fill=tk.X, padx=5, pady=(5, 10))
    
    ttk.Label(search_frame, text="🔍", font=("Segoe UI Emoji", 12)).pack(side=tk.LEFT, padx=(0, 5))
    search_var = tk.StringVar()
    
    search_entry = ttk.Entry(search_frame, textvariable=search_var, style="Search.TEntry")
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Member list with modern styling
    list_frame = ttk.Frame(left_frame)
    list_frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    columns = ("ID", "Name", "Username")
    tree = ttk.Treeview(list_frame, columns=columns, show="headings",
                      selectmode="browse", yscrollcommand=scrollbar.set,
                      height=20, style="MemberList.Treeview")
    
    # Configure modern column styling
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Username", text="Username")
    
    tree.column("ID", width=80, anchor="center")
    tree.column("Name", width=250)
    tree.column("Username", width=180)
    
    # Style alternating rows
    tree.tag_configure("oddrow", background="#F5F5F5")
    tree.tag_configure("evenrow", background="#FFFFFF")
    tree.tag_configure("selected", background="#2196F3", foreground="white")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=tree.yview)
    
    # Right pane with card-like design
    right_frame = ttk.LabelFrame(paned, text="Member Details", padding="15")
    paned.add(right_frame, weight=2)
    
    # Create scrollable canvas for details
    canvas = tk.Canvas(right_frame, highlightthickness=0)
    details_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    details_frame = ttk.Frame(canvas)
    
    canvas.configure(yscrollcommand=details_scroll.set)
    
    # Initialize variables for detail fields
    field_vars = {}
    current_row = 0
    
    # Organize fields into sections with improved layout
    sections = [
        ("Personal Information", [
            "ID:", "First Name:", "Last Name:", "Gender:"
        ]),
        ("Contact Details", [
            "Phone:", "Email:", "Address:"
        ]),
        ("Membership Details", [
            "Date of Birth:", "Joined Date:", "Username:", 
            "Trainer:", "Membership:"
        ])
    ]
    
    for section_title, section_fields in sections:
        # Section header with improved styling
        ttk.Label(details_frame, text=section_title,
                 font=("Helvetica", 14, "bold"),
                 padding=(0, 15, 0, 5)).grid(row=current_row,
                                           column=0,
                                           columnspan=4,
                                           sticky="w")
        current_row += 1
        
        # Create a separator under section title
        ttk.Separator(details_frame, orient="horizontal").grid(
            row=current_row, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        current_row += 1
        
        for i, field in enumerate(section_fields):
            ttk.Label(details_frame, text=field,
                     style="Details.TLabel").grid(row=current_row + i//2,
                                                column=i%2 * 2,
                                                sticky="e",
                                                padx=10,
                                                pady=5)
            var = tk.StringVar(value="")
            field_vars[field] = var
            entry = ttk.Entry(details_frame,
                            textvariable=var,
                            state="readonly",
                            style="Details.TEntry",
                            width=35)
            entry.grid(row=current_row + i//2,
                      column=i%2 * 2 + 1,
                      sticky="w",
                      padx=10,
                      pady=5)
        
        current_row += len(section_fields)//2 + 1
    
    # Configure scrolling for details panel
    canvas.create_window((0, 0), window=details_frame, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
    details_scroll.pack(side="right", fill="y")
    
    def populate_member_list():
        """Load and display members in the tree"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        # Load fresh data
        all_members = load_members_data()
        trainer_username = getattr(trainer, "username", trainer)
        
        # Filter members based on role
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
        
        # Sort members by ID for consistent display
        filtered_members.sort(key=lambda x: int(x.get("id", 0)))
        
        for i, member in enumerate(filtered_members):
            # Construct full name properly
            first_name = member.get("f_name", "").strip()
            last_name = member.get("l_name", "").strip()
            full_name = f"{first_name} {last_name}".strip()
            
            # Alternate row colors
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            
            # Insert with complete member data
            tree.insert("", "end", values=(
                str(member.get("id", "N/A")),  # Ensure ID is string
                full_name,
                member.get("username", "")
            ), tags=(tag,))
    
    def on_member_selected(event):
        """Handle member selection from tree with visual feedback"""
        selection = tree.selection()
        if not selection:
            return
            
        # Update row styling for visual feedback
        for item in tree.get_children():
            tags = list(tree.item(item, "tags"))
            if "selected" in tags:
                tags.remove("selected")
            tree.item(item, tags=tags)
            
        item = selection[0]
        current_tags = list(tree.item(item, "tags"))
        current_tags.append("selected")
        tree.item(item, tags=current_tags)
            
        # Get selected member data
        values = tree.item(selection[0])["values"]
        if not values or len(values) < 3:
            return
            
        username = values[2]
        
        # Load fresh data to ensure synchronization
        all_members = load_members_data()
        member = next((m for m in all_members if m.get("username") == username), None)
        if not member:
            messagebox.showerror("Error", "Member data not found. Please refresh the list.")
            return
            
        # Update fields with smooth animation effect
        def update_field(field, value, index=0):
            if index < len(value):
                field_vars[field].set(value[:index+1])
                root.after(5, update_field, field, value, index+1)
            
        # Update fields
        field_vars["ID:"].set(member.get("id", ""))
        field_vars["First Name:"].set(member.get("f_name", ""))
        field_vars["Last Name:"].set(member.get("l_name", ""))
        field_vars["Gender:"].set(member.get("gender", ""))
        field_vars["Phone:"].set(member.get("phone", ""))
        field_vars["Email:"].set(member.get("email", ""))
        field_vars["Address:"].set(member.get("address", ""))
        field_vars["Date of Birth:"].set(member.get("date_of_birth", ""))
        field_vars["Joined Date:"].set(member.get("joined_date", ""))
        field_vars["Username:"].set(member.get("username", ""))
        field_vars["Trainer:"].set(member.get("trainer_username", ""))
        field_vars["Membership:"].set(member.get("membership", ""))
        
        # Scroll canvas to top
        canvas.yview_moveto(0)

        # Update assign/unassign button based on current assignment
        def update_assign_button():
            trainer_name = getattr(trainer, "username", trainer)
            assigned = member.get("trainer_username") == trainer_name
            if assigned:
                assign_btn.config(text="Unassign from me", style="Warning.TButton")
            else:
                assign_btn.config(text="Assign to me", style="Accent.TButton")

        update_assign_button()
    
    def on_search(*args):
        """Filter member list based on search text with highlight"""
        search_text = search_var.get().lower().strip()
        for item in tree.get_children():
            values = tree.item(item)["values"]
            if not values:
                continue
                
            name = str(values[1]).lower()
            username = str(values[2]).lower()
            
            if search_text in name or search_text in username:
                tree.reattach(item, "", "end")
            else:
                tree.detach(item)
    
    # Bind events
    tree.bind("<<TreeviewSelect>>", on_member_selected)
    search_var.trace_add("write", on_search)
    
    # Action buttons with modern styling (Back + Assign/Unassign)
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=(20, 0))

    # Helper functions to update data files
    def _write_json(path, data):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True, None
        except Exception as e:
            return False, str(e)

    def assign_trainer_to_member(member_username, trainer_username):
        # Update member_info.json
        try:
            with open("data/member_info.json", "r", encoding="utf-8") as f:
                members = json.load(f)
        except Exception as e:
            return False, f"Failed to read members: {e}"

        found = False
        for m in members:
            if m.get("username") == member_username:
                m["trainer_username"] = trainer_username
                found = True
                break

        if not found:
            return False, "Member not found"

        ok, err = _write_json("data/member_info.json", members)
        if not ok:
            return False, f"Failed to write member info: {err}"

        # Update trainer_info.json -> ensure member_username list contains the member
        trainers = []
        if os.path.exists("data/trainer_info.json"):
            try:
                with open("data/trainer_info.json", "r", encoding="utf-8") as f:
                    trainers = json.load(f)
            except Exception:
                trainers = []

        trainer_found = False
        for t in trainers:
            if t.get("username") == trainer_username:
                trainer_found = True
                members_list = t.get("member_username") or []
                if member_username not in members_list:
                    members_list.append(member_username)
                    t["member_username"] = members_list
                break

        if not trainer_found:
            # create new trainer record minimally
            trainers.append({"username": trainer_username, "member_username": [member_username]})

        ok, err = _write_json("data/trainer_info.json", trainers)
        if not ok:
            return False, f"Failed to write trainer info: {err}"

        return True, None

    def unassign_trainer_from_member(member_username, trainer_username):
        # Update member_info.json -> remove trainer_username or set to empty
        try:
            with open("data/member_info.json", "r", encoding="utf-8") as f:
                members = json.load(f)
        except Exception as e:
            return False, f"Failed to read members: {e}"

        found = False
        for m in members:
            if m.get("username") == member_username:
                # only clear if currently assigned to this trainer
                if m.get("trainer_username") == trainer_username:
                    m["trainer_username"] = ""
                found = True
                break

        if not found:
            return False, "Member not found"

        ok, err = _write_json("data/member_info.json", members)
        if not ok:
            return False, f"Failed to write member info: {err}"

        # Update trainer_info.json -> remove member_username from trainer list
        trainers = []
        if os.path.exists("data/trainer_info.json"):
            try:
                with open("data/trainer_info.json", "r", encoding="utf-8") as f:
                    trainers = json.load(f)
            except Exception:
                trainers = []

        for t in trainers:
            if t.get("username") == trainer_username:
                members_list = t.get("member_username") or []
                if member_username in members_list:
                    members_list.remove(member_username)
                    t["member_username"] = members_list
                break

        ok, err = _write_json("data/trainer_info.json", trainers)
        if not ok:
            return False, f"Failed to write trainer info: {err}"

        return True, None

    # Commands for assign/unassign button
    def on_assign_unassign():
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a member first.")
            return
        username = tree.item(selection[0])["values"][2]
        trainer_name = getattr(trainer, "username", trainer)

        # Determine current state
        with open("data/member_info.json", "r", encoding="utf-8") as f:
            members = json.load(f)
        member = next((m for m in members if m.get("username") == username), None)
        if not member:
            messagebox.showerror("Error", "Member record not found.")
            return

        if member.get("trainer_username") == trainer_name:
            # unassign
            ok, err = unassign_trainer_from_member(username, trainer_name)
            if not ok:
                messagebox.showerror("Error", err)
                return
            messagebox.showinfo("Success", f"Member '{username}' unassigned from you.")
        else:
            ok, err = assign_trainer_to_member(username, trainer_name)
            if not ok:
                messagebox.showerror("Error", err)
                return
            messagebox.showinfo("Success", f"Member '{username}' assigned to you.")

        # refresh list and details
        populate_member_list()
        # re-select the updated member row
        for item in tree.get_children():
            if tree.item(item)["values"][2] == username:
                tree.selection_set(item)
                tree.see(item)
                break

    back_btn = ttk.Button(btn_frame,
                         text="Back to Menu",
                         style="Accent.TButton",
                         command=root.destroy)
    back_btn.pack(side=tk.RIGHT)

    assign_btn = ttk.Button(btn_frame, text="Assign to me", command=on_assign_unassign)
    assign_btn.pack(side=tk.RIGHT, padx=(0, 10))
    
    # Initial population
    populate_member_list()
    
    # Set focus to search entry
    search_entry.focus()