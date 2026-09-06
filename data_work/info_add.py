import json
import os
from datetime import datetime
from collections import defaultdict

def load_users_data():
    try:
        if not os.path.exists("data/member_info.json"):
            return []
        with open("data/member_info.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Error loading users data: {e}")
        return []

def load_trainers_data():
    if not os.path.exists("data/trainer_info.json"):
        return []
    with open ('data/trainer_info.json', 'r') as f:
        return json.load(f)

def load_subscription_data():
    """Load subscription information from JSON file"""
    filepath = "data/subscription_info.json"
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def calculate_revenue_data():
    """Calculate total revenue from all subscriptions"""
    members = load_users_data()
    subscription_plans = load_subscription_data()
    
    total_revenue = 0
    revenue_by_plan = defaultdict(int)
    revenue_by_month = defaultdict(int)
    member_details = []
    
    for member in members:
        membership = member.get('membership', '')
        if membership in subscription_plans:
            # Get fee from subscription plan [duration, fee]
            plan_data = subscription_plans[membership]
            if isinstance(plan_data, list) and len(plan_data) >= 2:
                fee = plan_data[1]
            else:
                # Fallback for legacy data
                fee = 1000000
            
            total_revenue += fee
            revenue_by_plan[membership] += fee
            
            # Calculate revenue by month based on joined date
            joined_date_str = member.get('joined_date', '')
            if joined_date_str:
                try:
                    joined_date = datetime.strptime(joined_date_str, '%Y-%m-%d')
                    month_key = joined_date.strftime('%Y-%m')
                    revenue_by_month[month_key] += fee
                except ValueError:
                    pass
            
            # Store member details for detailed report
            member_details.append({
                'name': f"{member.get('f_name', '')} {member.get('l_name', '')}",
                'username': member.get('username', ''),
                'membership': membership,
                'fee': fee,
                'joined_date': joined_date_str,
                'subscription_expiry': member.get('subscription_expiry', '')
            })
    
    return {
        'total_revenue': total_revenue,
        'revenue_by_plan': dict(revenue_by_plan),
        'revenue_by_month': dict(revenue_by_month),
        'member_details': member_details,
        'total_members': len(members)
    }

def search_members_by_name(search_term):
    try:
        with open("data/member_info.json", "r", encoding="utf-8") as f:
            members = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    search_term = search_term.strip().lower()
    found_members = []
    
    if not search_term:  # If search term is empty, return all members
        return members
    
    for member in members:
        f_name = str(member.get('f_name', '')).lower()
        l_name = str(member.get('l_name', '')).lower()
        username = str(member.get('username', '')).lower()
        full_name = f"{f_name} {l_name}".strip()
        
        if (search_term in f_name or 
            search_term in l_name or 
            search_term in full_name or
            search_term in username):
            found_members.append(member)
    
    return found_members

def search_trainer_by_name(search_term):
    """
    Search for trainers by first name, last name, or full name (case-insensitive).
    Returns a list of matching trainer dicts.
    """
    filepath = "data/trainer_info.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            trainers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    search_term = search_term.strip().lower()
    found_trainers = []

    for trainer in trainers:
        f_name = str(trainer.get('f_name', '')).lower()
        l_name = str(trainer.get('l_name', '')).lower()
        full_name = f"{f_name} {l_name}".strip()
        if (
            search_term in f_name
            or search_term in l_name
            or search_term in full_name
        ):
            found_trainers.append(trainer)

    return found_trainers


def update_member_info(username, updated_data):
    filepath = "data/member_info.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            members = json.load(f)
        
        # Find and update the member
        for i, member in enumerate(members):
            if member.get('username') == username:
                members[i].update(updated_data)
                break
        else:
            return False  # Member not found
        
        # Save updated data
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(members, f, indent=4)
        
        return True
    except Exception as e:
        print(f"Error updating member: {e}")
        return False


def add_trainer_to_json(f_name, l_name, gender, phone, date_of_birth, joined_date, address, email, username, height, weight, trainer_id):
    filepath = "data/trainer_info.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    users.append({
        "f_name": f_name,
        "l_name": l_name,
        "gender": gender,
        "phone": phone,
        "date_of_birth": date_of_birth,
        "joined_date": joined_date,
        "address": address,
        "email": email,
        "username": username,
        "height": height,
        "weight": weight,
        "trainer_id": trainer_id
    })  

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def add_user_to_json(
    f_name, l_name, gender, phone, date_of_birth, joined_date, address, email,
    membership, subscription_expiry, username, name, attendance_days, workout_days, trainer_username
):
    filepath = "data/member_info.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    # Optionally auto-increment id
    new_id = 1
    if users and isinstance(users[0], dict) and "id" in users[0]:
        new_id = max((u.get("id", 0) for u in users), default=0) + 1

    users.append({
        "id": new_id,
        "f_name": f_name,
        "l_name": l_name,
        "name": name,
        "gender": gender,
        "phone": phone,
        "date_of_birth": date_of_birth,
        "joined_date": joined_date,
        "address": address,
        "email": email,
        "membership": membership,
        "subscription_expiry": subscription_expiry,
        "username": username,
        "attendance_days": attendance_days,
        "workout_days": workout_days,
        "trainer_username": trainer_username
    })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)



def change_equipment_in_json(equipment_data):
    filepath = "data/equipment_info.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(equipment_data, f, indent=4)


def delete_user_from_json(username):

    # Delete from user.json
    user_filepath = "data/user.json"
    try:
        with open(user_filepath, "r", encoding="utf-8") as f:
            users = json.load(f)
        # Filter out the user with matching username
        users = [user for user in users if user.get("username") != username]
        with open(user_filepath, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading user.json: {e}")
        return

    # Delete from member_info.json
    member_filepath = "data/member_info.json"
    try:
        with open(member_filepath, "r", encoding="utf-8") as f:
            members = json.load(f)
        # Filter out the member with matching username
        members = [member for member in members if member.get("username") != username]
        with open(member_filepath, "w", encoding="utf-8") as f:
            json.dump(members, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading member_info.json: {e}")
        return 

def change_subscription_in_json(subscription_data):
    filepath = "data/subscription_info.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(subscription_data, f, indent=4) 

def add_attendance_day_to_json(username, date):
    filepath = "data/member_info.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            members = json.load(f)
        updated = False
        for member in members:
            if member.get("username") == username:
                if "attendance_days" not in member or not isinstance(member["attendance_days"], list):
                    member["attendance_days"] = []
                if date not in member["attendance_days"]:
                    member["attendance_days"].append(date)
                    updated = True
                break
        if updated:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(members, f, indent=4)
        return updated
    except Exception as e:
        print(f"Error adding attendance day: {e}")
        return False

def add_workout_day_to_json(username, date, workout):
    filepath = "data/member_info.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            members = json.load(f)
        updated = False
        for member in members:
            if member.get("username") == username:
                if "workout_days" not in member or not isinstance(member["workout_days"], list):
                    member["workout_days"] = []
                # Prevent duplicate for same date+workout
                if [date, workout] not in member["workout_days"]:
                    member["workout_days"].append([date, workout])
                    updated = True
                break
        if updated:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(members, f, indent=4)
        return updated
    except Exception as e:
        print(f"Error adding workout day: {e}")
        return False