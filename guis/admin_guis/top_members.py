from tkinter import *
from tkinter import ttk
import json
import os
from datetime import datetime

class TopMembers:
    def __init__(self, window):
        self.window = window
        self.window.title("Top Active Members")
        self.window.geometry("800x600")
        self.setup_gui()
        self.load_data()

    def setup_gui(self):
        # Configuring the main window
        self.window.configure(bg="#f0f0f0")
        
        # Main Frame with padding and background
        self.main_frame = Frame(self.window, bg="#f0f0f0")
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Title with better styling
        title_frame = Frame(self.main_frame, bg="#f0f0f0")
        title_frame.pack(fill=X, pady=(0, 20))
        
        title_label = Label(title_frame, 
                          text="Top Active Members",
                          font=("Arial", 24, "bold"),
                          bg="#f0f0f0",
                          fg="#2c3e50")
        title_label.pack()

        # Subtitle
        subtitle_label = Label(title_frame,
                             text="Ranked by attendance frequency",
                             font=("Arial", 12),
                             bg="#f0f0f0",
                             fg="#7f8c8d")
        subtitle_label.pack()

        # Frame for Treeview with a white background
        tree_frame = Frame(self.main_frame, bg="white", relief=RIDGE, borderwidth=1)
        tree_frame.pack(fill=BOTH, expand=True)

        # Create Treeview with adjusted columns
        columns = ("Rank", "Name", "Username", "Attendance Count", "Last Attendance")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Style for Treeview
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=30, fieldbackground="white")
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#2c3e50", foreground="white")

        # Configure column headings and widths
        widths = [80, 200, 150, 150, 200]  # Adjusted column widths
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Style configuration
        style = ttk.Style()
        style.configure("Treeview.Heading", 
                       font=("Arial", 12, "bold"),
                       background="#2c3e50",
                       foreground="white",
                       padding=10)
        
        style.configure("Treeview", 
                       font=("Arial", 11),
                       rowheight=30,
                       background="#ffffff",
                       fieldbackground="#ffffff")

        # Add striped rows with better colors
        self.tree.tag_configure("oddrow", background="#ecf0f1")
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("top3", background="#e3f2fd")

    def load_data(self):
        try:
            # Get the absolute path for member_info.json
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            json_path = os.path.join(current_dir, "data", "member_info.json")

            # Load member data with explicit UTF-8 encoding
            with open(json_path, "r", encoding='utf-8') as f:
                member_data = json.load(f)

            # Process and sort members by attendance count
            member_stats = []
            for member in member_data:
                attendance_count = len(member.get("attendance_days", []))
                attendance_dates = member.get("attendance_days", [])
                
                # Get last attendance date
                last_attendance = "Never"
                if attendance_dates:
                    last_date = max(attendance_dates)
                    # Convert date string to datetime for formatting
                    try:
                        date_obj = datetime.strptime(last_date, "%Y-%m-%d")
                        last_attendance = date_obj.strftime("%d %b %Y")
                    except:
                        last_attendance = last_date

                if attendance_count > 0:  # Only include members with attendance
                    member_stats.append({
                        "name": f"{member['f_name']} {member['l_name']}",
                        "username": member["username"],
                        "attendance_count": attendance_count,
                        "last_attendance": last_attendance
                    })

            # Sort by attendance count in descending order
            member_stats.sort(key=lambda x: x["attendance_count"], reverse=True)

            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert data into treeview
            for idx, member in enumerate(member_stats, 1):
                # Use the 'name' field prepared earlier when building member_stats
                values = (
                    f"#{idx}",
                    member.get('name', member.get('username', 'Unknown')),
                    member.get("username", "-"),
                    f"{member['attendance_count']} days",
                    member["last_attendance"]
                )
                
                # Apply row styling
                if idx <= 3:  # Top 3 members get special highlighting
                    row_tags = ("top3",)
                else:
                    row_tags = ("evenrow",) if idx % 2 == 0 else ("oddrow",)
                
                self.tree.insert("", END, values=values, tags=row_tags)

            # Display a message if no data
            if not member_stats:
                no_data_label = Label(self.main_frame,
                                    text="No attendance records found",
                                    font=("Arial", 14),
                                    fg="#666666",
                                    bg="#f0f0f0")
                no_data_label.pack(pady=20)

        except Exception as e:
            error_label = Label(self.main_frame,
                              text=f"Error loading data: {str(e)}",
                              font=("Arial", 12),
                              fg="red",
                              bg="#f0f0f0")
            error_label.pack(pady=20)

def open_top_members(window):
    TopMembers(window)