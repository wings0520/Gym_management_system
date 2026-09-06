# Gym Management System

A desktop gym management application built with Python and Tkinter. The system provides role-based workflows for administrators, trainers, and members. Application data is stored locally in JSON files.

## Features

### Authentication

- Login with a username and password.
- User roles are loaded from `data/user.json`.
- Successful login opens the dashboard for the authenticated role.
- New member accounts can be registered through the login window.

### Administrator

Administrators can manage the main gym operations from the administrator dashboard:

- Create and manage member records.
- Create and search trainer records.
- Edit or delete member information.
- Manage equipment information.
- Create and update subscription plans.
- Record and report member attendance.
- Calculate revenue from member subscription data.
- View the most active members.

### Trainer

Trainers can manage member training activities:

- Assign workout plans to members.
- Add attendance records.
- Track attendance.
- View member information.
- Track member progress.

### Member

Members can access their own gym information and services:

- View their profile.
- View their current subscription plan.
- Renew or subscribe to a plan.
- Check their workout schedule.
- Track personal progress.
- Contact trainers or administrators.

## How the System Works

1. `main.py` starts the application and opens the login window.
2. The login window validates the entered credentials against `data/user.json`.
3. The stored role determines which dashboard is opened:
   - `admin` -> administrator dashboard
   - `trainer` -> trainer dashboard
   - `member` -> member dashboard
4. Dashboard buttons open feature-specific Tkinter windows.
5. Feature modules read and update the JSON files in the `data/` directory.
6. The application keeps all records locally; it does not currently use a database or a web server.

## Project Structure

```text
.
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── auth/                      # Authentication helpers
├── data/                      # Local JSON data files
├── data_work/                 # Data loading, searching, and update functions
├── guis/                      # Main role-based windows
│   ├── admin_guis/             # Administrator feature windows
│   ├── member_guis/            # Member feature windows
│   └── trainer_guis/           # Trainer feature windows
├── models/                    # User, admin, trainer, and member models
└── utils/                     # Shared background and icon helpers
```

## Requirements

- Python 3.10 or newer is recommended.
- Tkinter, usually included with standard Python installations.
- Packages listed in `requirements.txt`:
  - `tkcalendar`
  - `ttkthemes`

## Installation

1. Clone or download the project.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Windows Command Prompt:

   ```cmd
   .venv\Scripts\activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

From the project root, run:

```bash
python main.py
```

Use an account from `data/user.json` to sign in. The account's `role` value controls the dashboard that is displayed.

## Data Files

- `data/user.json` stores login credentials and roles.
- `data/member_info.json` stores member profiles, memberships, attendance, workouts, and trainer assignments.
- `data/trainer_info.json` stores trainer profiles.
- `data/subscription_info.json` stores subscription durations and prices.
- `data/equipment_info.json` stores equipment information.
- `data/attendance_records.json` stores attendance-related records used by the application.

Because these files are modified during normal use, create a backup before testing administrative operations or changing sample data.

## Current Limitations and Security Notes

- Data is stored in local JSON files, so the application is intended for local or educational use.
- Passwords are currently stored as plain text in `data/user.json`; production deployment should use password hashing and a protected database.
- There is no database layer, API, multi-user synchronization, or automated backup system.
- Some model methods are placeholders and may require further implementation as the system grows.
