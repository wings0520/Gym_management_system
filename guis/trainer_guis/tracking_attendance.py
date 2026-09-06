import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

_refresh_callback = None

def register_refresh_callback(cb):
    """Register a callback (callable) which will be called to refresh the tracking view.
    Other modules can import this module and call refresh_tracking() or rely on this registration.
    """
    global _refresh_callback
    _refresh_callback = cb

def refresh_tracking():
    """Call the registered refresh callback if available."""
    try:
        if _refresh_callback:
            _refresh_callback()
    except Exception:
        pass

def load_all_members():
    if not os.path.exists("data/member_info.json"):
        return []
    with open("data/member_info.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_trainer_members(trainer_username):
    if not os.path.exists("data/trainer_info.json"):
        return []
    with open("data/trainer_info.json", "r", encoding="utf-8") as f:
        trainers = json.load(f)
        for trainer in trainers:
            if trainer.get("username") == trainer_username:
                return trainer.get("member_username", [])
    return []

def get_user_role(username):
    if not os.path.exists("data/user.json"):
        return None
    with open("data/user.json", "r", encoding="utf-8") as f:
        users = json.load(f)
        for user in users:
            if user.get("username") == username:
                return user.get("role")
    return None

def export_attendance_to_csv():
    members = load_all_members()
    rows = []
    for m in members:
        username = m.get("username", "")
        name = m.get("name") or f"{m.get('f_name', '')} {m.get('l_name', '')}".strip()
        for day in m.get("attendance_days", []):
            rows.append([username, name, day])
    if not rows:
        messagebox.showinfo("No Data", "No attendance data to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Attendance Report")
    if not file_path:
        return
    import csv
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Name", "Attendance Day"])
        writer.writerows(rows)
    messagebox.showinfo("Success", f"Attendance report saved to {file_path}")

def on_add_attendance(root, admin, current_user):
    root.title("Attendance Tracking")
    text_label = tk.Label(root, text="Attendance Tracking", font=("Arial", 24), bg=root["bg"])
    text_label.pack(pady=20)

    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Date picker frame
    date_frame = tk.Frame(main_frame, bg=root["bg"])
    date_frame.pack(fill="x", pady=(0, 15))
    
    date_label = tk.Label(date_frame, text="Select Date:", font=("Arial", 12), bg=root["bg"])
    date_label.pack(side="left", padx=5)
    
    date_entry = DateEntry(date_frame, width=20, background='darkblue', foreground='white', 
                          borderwidth=2, date_pattern='yyyy-mm-dd',
                          year=datetime.now().year, month=datetime.now().month,
                          day=datetime.now().day, firstweekday='sunday',
                          showweeknumbers=False, selectmode='day')
    date_entry.pack(side="left", padx=5)

    # Add Attendance area (Member selector + Add button)
    add_frame = tk.Frame(main_frame, bg=root["bg"]) 
    add_frame.pack(fill="x", pady=(0, 10))

    member_label = tk.Label(add_frame, text="Member:", font=("Arial", 11), bg=root["bg"])
    member_label.pack(side="left", padx=(5, 2))

    # load members for combobox (trainers see only their members)
    all_members = load_all_members()
    user_role = get_user_role(current_user)

    def member_matches_trainer_list(member, trainer_list):
        uname = (member.get("username") or "").strip()
        full_name = f"{member.get('f_name','')} {member.get('l_name','')}".strip()
        alt_name = (member.get("name") or "").strip()
        return (uname in trainer_list) or (full_name in trainer_list) or (alt_name in trainer_list)

    if user_role == "trainer":
        allowed_list = load_trainer_members(current_user)
        combo_members = [m for m in all_members if member_matches_trainer_list(m, allowed_list)]
    else:
        combo_members = all_members

    member_usernames = [m.get("username", "") for m in combo_members]
    member_names = [m.get("name") or f"{m.get('f_name','')} {m.get('l_name','')}".strip() for m in combo_members]
    member_display = [f"{n} ({u})" for n, u in zip(member_names, member_usernames)]

    member_var = tk.StringVar(value=member_display[0] if member_display else "")
    member_combo = ttk.Combobox(add_frame, textvariable=member_var, values=member_display, state="readonly", width=35)
    member_combo.pack(side="left", padx=5)

    def add_attendance_from_ui():
        sel = member_combo.get()
        if not sel:
            messagebox.showerror("Error", "Please select a member to add attendance.")
            return
        # extract username from display "Name (username)"
        if sel.endswith(')') and '(' in sel:
            username = sel[sel.rfind('(')+1:-1]
        else:
            username = sel
        date_str = date_entry.get_date().strftime('%Y-%m-%d')
        try:
            success = admin.add_attendance_day(username, date_str)
        except Exception as e:
            success = False
            print("Error adding attendance:", e)
        if success:
            messagebox.showinfo("Success", f"Added attendance for {username} on {date_str}")
            # refresh member list immediately
            update_attendance_list()
            # visually select the newly added row
            for iid in tree.get_children():
                vals = tree.item(iid, "values")
                if vals and vals[2] == username:
                    tree.selection_set(iid)
                    tree.see(iid)
                    break
        else:
            messagebox.showerror("Error", "Failed to add attendance. Maybe already exists.")

    add_btn = tk.Button(add_frame, text="Add Attendance", command=add_attendance_from_ui, font=("Arial", 11, "bold"), bg="#2196F3", fg="white", relief="raised", bd=2)
    add_btn.pack(side="left", padx=8)

    # Search bar + Create Treeview for member list
    search_frame = tk.Frame(main_frame, bg=root["bg"]) 
    search_frame.pack(fill="x", pady=(0, 6))
    tk.Label(search_frame, text="Search:", font=("Arial", 11), bg=root["bg"]).pack(side="left", padx=(2,6))
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=40)
    search_entry.pack(side="left", padx=(0,6))

    # keep last loaded attended members so search/sort can operate on them
    last_attended_members = []

    def apply_search(*_args):
        # filter last_attended_members by search_var and repopulate tree
        qry = search_var.get().strip().lower()
        # clear
        tree.delete(*tree.get_children())
        if not last_attended_members:
            tree.pack_forget()
            no_data_label.config(text="No members attended on selected date")
            no_data_label.pack(pady=20)
            return
        filtered = []
        if not qry:
            filtered = last_attended_members
        else:
            for item in last_attended_members:
                # item is tuple (id, name, username, trainer)
                if qry in str(item[1]).lower() or qry in str(item[2]).lower() or qry in str(item[3]).lower():
                    filtered.append(item)
        if not filtered:
            tree.pack_forget()
            no_data_label.config(text=f"No members matched '{qry}'")
            no_data_label.pack(pady=20)
        else:
            no_data_label.pack_forget()
            tree.pack(fill="both", expand=True)
            for member_data in filtered:
                tree.insert("", "end", values=member_data)

    search_var.trace_add('write', apply_search)

    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    columns = ("ID", "Name", "Username", "Trainer")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10,
                        yscrollcommand=tree_scroll.set)
    
    tree_scroll.config(command=tree.yview)

    # Configure columns (adjust widths)
    tree.heading("ID", text="ID")
    tree.column("ID", width=60, anchor="center")
    tree.heading("Name", text="Name")
    tree.column("Name", width=220, anchor="w")
    tree.heading("Username", text="Username")
    tree.column("Username", width=140, anchor="w")
    tree.heading("Trainer", text="Trainer")
    tree.column("Trainer", width=120, anchor="w")

    # Support sorting by clicking on headings
    def tree_sort(col, reverse=False):
        data = [(tree.set(k, col), k) for k in tree.get_children('')]
        try:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        except Exception:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)
        for index, (val, k) in enumerate(data):
            tree.move(k, '', index)
        # reverse next time
        tree.heading(col, command=lambda: tree_sort(col, not reverse))

    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: tree_sort(c, False))

    # Do not pack tree immediately; we'll show it when data exists
    # tree.pack(fill="both", expand=True)

    # Label shown when there's no data for selected date
    no_data_label = tk.Label(tree_frame, text="", font=("Arial", 12), bg=root["bg"], fg="#444")

    def update_attendance_list(*args):
        nonlocal last_attended_members
        tree.delete(*tree.get_children())
        selected_date = date_entry.get_date().strftime('%Y-%m-%d')
        
        # Get all members
        all_members = load_all_members()
        user_role = get_user_role(current_user)
        
        # Filter members based on role
        if user_role == "trainer":
            trainer_members = load_trainer_members(current_user)
            filtered_members = [m for m in all_members if m.get("username") in trainer_members]
        else:  # Admin sees all members
            filtered_members = all_members

        # Filter members who attended on selected date
        attended_members = []
        for member in filtered_members:
            if selected_date in member.get("attendance_days", []):
                # Find trainer name for this member
                trainer_name = "Not Assigned"
                if os.path.exists("data/trainer_info.json"):
                    with open("data/trainer_info.json", "r", encoding="utf-8") as f:
                        trainers = json.load(f)
                        for trainer in trainers:
                            # trainer.get("member_username") may contain usernames or display/full names.
                            tlist = trainer.get("member_username", [])
                            uname = member.get("username")
                            full = f"{member.get('f_name','')} {member.get('l_name','')}".strip()
                            alt = member.get("name") or ""
                            if (uname in tlist) or (full in tlist) or (alt in tlist):
                                trainer_name = trainer.get("username", "Not Assigned")
                                break
                
                member_name = member.get("name") or f"{member.get('f_name', '')} {member.get('l_name', '')}".strip()
                attended_members.append((
                    member.get("id", "N/A"),
                    member_name,
                    member.get("username", ""),
                    trainer_name
                ))

        # store for search/sort
        last_attended_members = attended_members

        if not attended_members:
            # show message
            tree.pack_forget()
            no_data_label.config(text=f"No members attended on {selected_date}")
            no_data_label.pack(pady=20)
        else:
            # show tree and populate
            no_data_label.pack_forget()
            tree.pack(fill="both", expand=True)
            for member_data in attended_members:
                tree.insert("", "end", values=member_data)

    # Register our update function so external add-attendance screens can refresh tracking
    try:
        register_refresh_callback(update_attendance_list)
    except Exception:
        pass

    # Bind the date picker to update the list
    date_entry.bind("<<DateEntrySelected>>", update_attendance_list)

    # Export button
    export_btn = tk.Button(main_frame, text="Export Attendance Report",
                          command=export_attendance_to_csv,
                          font=("Arial", 12, "bold"), bg="#4CAF50",
                          fg="white", relief="raised", bd=2)
    export_btn.pack(pady=10)

    # Back button
    def back_to_menu():
        root.destroy()
    back_btn = tk.Button(main_frame, text="Back to Menu",
                        command=back_to_menu,
                        font=("Arial", 12, "bold"), bg="#2196F3",
                        fg="white", relief="raised", bd=2)
    back_btn.pack(pady=10)

    # Initial load of attendance data
    update_attendance_list()
