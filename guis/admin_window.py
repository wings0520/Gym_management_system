import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter import messagebox
from utils.create_icon import c_icon
from utils.create_background import c_background
from guis.admin_guis.new_member import on_new_member
from guis.admin_guis.new_trainer import on_new_trainer
from guis.admin_guis.equipment_manager import on_equipment_manager
from guis.admin_guis.delete_member import on_delete_member
from guis.admin_guis.search_member import on_search_member
from guis.admin_guis.manage_subscription import on_manage_subscription
from guis.admin_guis.cal_revenue import on_cal_revenue
from guis.admin_guis.search_trainer import on_search_trainer
from guis.admin_guis.add_attendance import on_add_attendance
from guis.admin_guis.top_members import open_top_members

def open_admin_window(admin):
    root = tk.Tk()
    root.title("Gym Management System - Admin")
    
    # --- GỌI BACKGROUND CỦA BẠN LÊN TRÊN ĐẦU ---
    c_icon(root)
    c_background(root) 
    
    root.state('zoomed') 
    
    # --- Cấu hình Kiểu dáng (Styling) ---
    style = ttk.Style()
    style.theme_use('clam')

    # Màu sắc
    sidebar_bg = "#2c3e50"
    button_fg = "#ffffff"
    button_hover_bg = "#34495e"

    style.configure("Sidebar.TFrame", background=sidebar_bg)
    
    # SỬA LỖI: Giảm padding ngang từ 20 xuống 15
    style.configure("Nav.TButton",
                    font=("Arial", 12, "bold"),
                    background=sidebar_bg,
                    foreground=button_fg,
                    borderwidth=0,
                    padding=(15, 10)) # <--- THAY ĐỔI
    style.map("Nav.TButton",
              background=[('active', button_hover_bg)],
              foreground=[('active', button_fg)])

    # SỬA LỖI: Giảm padding ngang từ 20 xuống 15
    style.configure("Exit.TButton",
                    font=("Arial", 12, "bold"),
                    background="#e74c3c",
                    foreground=button_fg,
                    borderwidth=0,
                    padding=(15, 10)) # <--- THAY ĐỔI
    style.map("Exit.TButton",
              background=[('active', "#c0392b")])

    # --- Kết thúc Cấu hình Kiểu dáng ---

    current_sub_window = None

    def close_sub_window():
        nonlocal current_sub_window
        if current_sub_window and current_sub_window.winfo_exists():
            current_sub_window.destroy()
            current_sub_window = None

    def create_sub_window():
        close_sub_window()
        nonlocal current_sub_window
        current_sub_window = tk.Toplevel(root)
        current_sub_window.transient(root)
        current_sub_window.grab_set()
        
        c_icon(current_sub_window)
        c_background(current_sub_window) 
        
        sub_style = ttk.Style(current_sub_window)
        sub_style.theme_use('clam')
        
        sub_style.configure("TFrame", background=current_sub_window["bg"])
        sub_style.configure("TLabel", background=current_sub_window["bg"])
        sub_style.configure("TRadiobutton", background=current_sub_window["bg"])

        sub_style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        
        sub_style.configure("Success.TButton", background="#4CAF50", foreground="white")
        sub_style.map("Success.TButton", background=[('active', '#45a049')])
        
        sub_style.configure("Danger.TButton", background="#f44336", foreground="white")
        sub_style.map("Danger.TButton", background=[('active', '#d32f2f')])
        
        sub_style.configure("Primary.TButton", background="#2196F3", foreground="white")
        sub_style.map("Primary.TButton", background=[('active', '#1e88e5')])
        
        sub_style.configure("Warning.TButton", background="#FF9800", foreground="white")
        sub_style.map("Warning.TButton", background=[('active', '#fb8c00')])

        return current_sub_window

    # --- Các hàm mở cửa sổ con (Không thay đổi) ---
    def open_new_member():
        window = create_sub_window()
        on_new_member(window, admin)
    
    def open_new_trainer():
        window = create_sub_window()
        on_new_trainer(window, admin)
    
    def open_equipment_manager():
        window = create_sub_window()
        on_equipment_manager(window, admin)
    
    def open_search_member():
        window = create_sub_window()
        on_search_member(window, admin)

    def open_manage_subscription():
        window = create_sub_window()
        on_manage_subscription(window, admin)

    def open_cal_revenue():
        window = create_sub_window()
        on_cal_revenue(window, admin)

    def open_search_trainer():
        window = create_sub_window()
        on_search_trainer(window, admin)

    def open_add_attendance():
        window = create_sub_window()
        on_add_attendance(window, admin)

    def open_top_member():
        window = create_sub_window()
        open_top_members(window)

    # --- Bố cục (Layout) ---
    
    # SỬA LỖI: Tăng độ rộng sidebar từ 250 -> 280
    sidebar_frame = ttk.Frame(root, width=280, style="Sidebar.TFrame") # <--- THAY ĐỔI
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_frame.pack_propagate(False) 

    main_frame = tk.Frame(root) 
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # --- Thêm widget vào Sidebar ---
    title_font = tkFont.Font(family="Arial", size=18, weight="bold")
    title_label = tk.Label(sidebar_frame, 
                           text="Admin Menu", 
                           font=title_font, 
                           bg=sidebar_bg, 
                           fg="#ffffff", 
                           pady=20)
    title_label.pack(pady=(10, 20))
    
    # SỬA LỖI: Giảm padx từ 20 -> 15
    btn_new_member = ttk.Button(sidebar_frame, text="New Member", command=open_new_member, style="Nav.TButton")
    btn_new_member.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI
    
    btn_new_trainer = ttk.Button(sidebar_frame, text="New Trainer", command=open_new_trainer, style="Nav.TButton")
    btn_new_trainer.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI
    
    btn_equipment = ttk.Button(sidebar_frame, text="Equipment", command=open_equipment_manager, style="Nav.TButton")
    btn_equipment.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI
    
    btn_search_member = ttk.Button(sidebar_frame, text="Edit/Report Member", command=open_search_member, style="Nav.TButton")
    btn_search_member.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI
    
    btn_subscription_plans = ttk.Button(sidebar_frame, text="Subscription Plans", command=open_manage_subscription, style="Nav.TButton")
    btn_subscription_plans.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI
    
    btn_search_trainer = ttk.Button(sidebar_frame, text="Edit Trainer", command=open_search_trainer, style="Nav.TButton")
    btn_search_trainer.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI
    
    btn_add_attendance = ttk.Button(sidebar_frame, text="Add/Report Attendance", command=open_add_attendance, style="Nav.TButton")
    btn_add_attendance.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI
    
    btn_cal_revenue = ttk.Button(sidebar_frame, text="Revenue Report", command=open_cal_revenue, style="Nav.TButton")
    btn_cal_revenue.pack(fill=tk.X, pady=5, padx=15) # <--- THAY ĐỔI

    btn_top_members = ttk.Button(sidebar_frame, text="Top Active Members", command=open_top_member, style="Nav.TButton")
    btn_top_members.pack(fill=tk.X, pady=5, padx=15)
    
    btn_exit = ttk.Button(sidebar_frame, text="Exit", command=root.destroy, style="Exit.TButton")
    btn_exit.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=15) # <--- THAY ĐỔI
    
    # --- Thêm widget vào Main Frame ---
    welcome_font = tkFont.Font(family="Arial", size=24, weight="bold")
    welcome_label = tk.Label(main_frame, 
                              text="Welcome Admin!", 
                              font=welcome_font,
                              fg="#333333") 
    welcome_label.pack(pady=50)

    info_font = tkFont.Font(family="Arial", size=14)
    info_label = tk.Label(main_frame, 
                           text="Please select a function from the menu on the left.", 
                           font=info_font,
                           fg="#333333")
    info_label.pack(pady=10)

    root.mainloop()
