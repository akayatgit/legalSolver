import os
import json

def create_department_emails():
    """Create or update the department_emails.json file"""
    print("Creating/updating department_emails.json file...")
    
    # Default department emails
    departments = [
        {"department": "Police", "email": "policepetitionhub123@gmail.com"},
        {"department": "Women Protection Cell", "email": "womenprotectioncell52@gmail.com"},
        {"department": "Economic Offences Wing", "email": "economicoffenceswing2@gmail.com"}
    ]
    
    # Check if file already exists
    if os.path.exists("department_emails.json"):
        try:
            with open("department_emails.json", "r", encoding="utf-8") as f:
                existing_departments = json.load(f)
                print(f"Existing departments: {existing_departments}")
                
                # Check if all required departments are present
                existing_dept_names = [dept["department"] for dept in existing_departments]
                for dept in departments:
                    if dept["department"] not in existing_dept_names:
                        print(f"Adding missing department: {dept['department']}")
                        existing_departments.append(dept)
                
                departments = existing_departments
        except Exception as e:
            print(f"Error reading existing file: {e}")
            print("Creating new file with default values")
    else:
        print("File does not exist, creating new file")
    
    # Write the file
    try:
        with open("department_emails.json", "w", encoding="utf-8") as f:
            json.dump(departments, f, indent=2)
        print(f"Successfully created/updated department_emails.json with {len(departments)} departments")
        return True
    except Exception as e:
        print(f"Error creating file: {e}")
        return False

if __name__ == "__main__":
    create_department_emails() 