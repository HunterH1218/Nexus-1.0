import os
import shutil
import datetime
import pytz
import json
import requests
import requests
from bs4 import BeautifulSoup
from nexus.weather import current
import random
import pandas as pd


def write_file(name, type, contents, location):
    filename = f"{name}.{type}"
    filepath = os.path.join(location, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(contents)
        return f"File '{filename}' was successfully created at '{location}'."
    except Exception as e:
        return f"An error occurred: {e}"


def create_folder(name, location):
    folder_path = os.path.join(location, name)
    try:
        os.makedirs(folder_path)
        return "Folder created successfully."
    except Exception as e:
        return f"An error occurred: {e}"


def delete_file(name, location):
    file_path = os.path.join(location, name)
    try:
        os.remove(file_path)  # Make sure file_path is correct and accessible
        return "File deleted successfully."
    except Exception as e:
        # Consider printing/logging the exception message to diagnose
        return f"An error occurred: {e}"


def delete_folder(name, location):
    folder_path = os.path.join(location, name)
    try:
        shutil.rmtree(folder_path)
        return "Folder deleted successfully."
    except Exception as e:
        return f"An error occurred: {e}"



def move_item(source, destination):
    try:
        shutil.move(source, destination)
        return "Item moved successfully."
    except Exception as e:
        return f"An error occurred: {e}"


def read_file(name, location):
    file_path = os.path.join(location, name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        return contents
    except Exception as e:
        return f"An error occurred: {e}"


def list_folder_contents(location):
    try:
        return os.listdir(location)
    except Exception as e:
        return f"An error occurred: {e}"


def date():
    try:
        date = datetime.datetime.now().strftime("%b %d %Y")
    except Exception as e:
        print(e)
        date = False
    return date


def time(timezone='EST'):
    try:
        # Define the timezone
        tz = pytz.timezone(timezone)

        # Get the current time in the specified timezone in 12-hour format
        time = datetime.datetime.now(tz).strftime("%I:%M %p")
    except Exception as e:
        print(e)
        time = False
        print(time)
    return time


def get_weather():
    return current.main()


def add_plan(name, date, start_time, end_time):
    if not os.path.exists('my_calendar/calendar.json'):
        with open('my_calendar/calendar.json', 'w') as file:
            json.dump({"plans": []}, file)

    with open('my_calendar/calendar.json', 'r') as file:
        data = json.load(file)

    new_plan = {
        "name": name,
        "date": date,
        "start_time": start_time,
        "end_time": end_time
    }
    data['plans'].append(new_plan)

    with open('my_calendar/calendar.json', 'w') as file:
        json.dump(data, file, indent=5)

    return f"Plan '{name}' was successfully added to the calendar."


def delete_past_plans():
    # Define the path to the calendar file
    file_path = 'my_calendar/calendar.json'
    if not os.path.exists(file_path):
        print("Calendar file does not exist.")
        return "Calendar file does not exist."

    # Load existing data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Define the EST timezone
    est = pytz.timezone('US/Eastern')
    # Get the current time in UTC and convert to EST
    current_time = datetime.datetime.now(pytz.utc).astimezone(est)

    # Filter out past plans based on their recurrence and time
    updated_plans = []
    for plan in data.get('plans', []):
        try:
            plan_end_time_str = f"{plan['date']} {plan['end_time']}"
            plan_end_time = datetime.datetime.strptime(plan_end_time_str,
                                                       "%m/%d/%Y %I:%M %p")

            # Localize plan end time to the EST
            if not plan_end_time.tzinfo:
                plan_end_time = est.localize(plan_end_time)
            else:
                plan_end_time = plan_end_time.astimezone(est)
            if plan_end_time > current_time:
                updated_plans.append(plan)
        except ValueError as e:
            print(f"Error parsing date for {plan['name']}: {e}")

    # Update the data with non-past plans
    data['plans'] = updated_plans

    # Write updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=5)

    print("Updated plans saved.")
    return "Updated plans saved."


def get_todays_plans():
    # Define the path to the calendar file
    file_path = 'my_calendar/calendar.json'
    if not os.path.exists(file_path):
        print("Calendar file does not exist.")
        return []
    # Load existing data
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Define the EST timezone
    est = pytz.timezone('US/Eastern')
    # Get today's date in EST
    current_time = datetime.datetime.now(pytz.utc).astimezone(est)
    today_date_str = current_time.strftime('%m/%d/%Y')

    # Filter and handle today's plans
    todays_plans = []
    for plan in data.get('plans', []):
        if plan['date'] == today_date_str:
            # Extract variables for each component of the plan
            plan_name = plan['name']
            plan_date = plan['date']
            plan_start_time = plan['start_time']
            plan_end_time = plan['end_time']
            # Add to today's plans list
            todays_plans.append(plan)

            final = (
                f"Here are your plans for today:\nName: {plan_name}\nDate: {plan_date}\nStart Time: {plan_start_time}\nEnd Time: {plan_end_time}\n"
            )
    if not todays_plans:
        final = ("No plans for today sir.")
    return (final)


def time_until_next_plan():
    # Define the path to the calendar file
    file_path = 'my_calendar/calendar.json'
    if not os.path.exists(file_path):
        print("Calendar file does not exist.")
        return None
    # Load existing data
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Define the EST timezone
    est = pytz.timezone('US/Eastern')
    # Get the current time in EST
    current_time = datetime.datetime.now(pytz.utc).astimezone(est)
    today_date_str = current_time.strftime('%m/%d/%Y')
    # Find future plans for today
    future_plans = []
    for plan in data.get('plans', []):
        plan_date = plan['date']
        plan_start_time_str = f"{plan['date']} {plan['start_time']}"
        plan_start_time = datetime.datetime.strptime(plan_start_time_str,
                                                     "%m/%d/%Y %I:%M %p")
        plan_start_time = est.localize(
            plan_start_time
        ) if not plan_start_time.tzinfo else plan_start_time.astimezone(est)
        if plan_date == today_date_str and plan_start_time > current_time:
            future_plans.append(plan_start_time)
    if not future_plans:
        print("No upcoming plans for today.")
        return None
    # Find the next upcoming plan
    next_plan_time = min(future_plans)
    # Calculate the time difference
    time_difference = next_plan_time - current_time
    # Convert the time difference to hours and minutes
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes = remainder // 60
    if hours == 0:
        return f"The next plan is in {minutes} minutes."
    elif minutes == 0:
        return f"The next plan is in {hours} hours."
    else:
        return f"The next plan is in {hours} hours and {minutes} minutes."


def edit_plan(plan_name,
              new_name=None,
              new_date=None,
              new_start_time=None,
              new_end_time=None):
    # Define the path to the calendar file
    file_path = 'my_calendar/calendar.json'

    if not os.path.exists(file_path):
        print("Calendar file does not exist.")
        return "Calendar file does not exist."

    # Load existing data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Look for the plan by name
    plan_found = False
    for plan in data.get('plans', []):
        if plan['name'] == plan_name:
            plan_found = True
            # Update with new details if provided
            if new_name:
                plan['name'] = new_name
            if new_date:
                plan['date'] = new_date
            if new_start_time:
                plan['start_time'] = new_start_time
            if new_end_time:
                plan['end_time'] = new_end_time
            break

    if not plan_found:
        print(f"Plan with name '{plan_name}' not found.")
        return f"Plan with name '{plan_name}' not found."

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=5)

    return f"Plan '{plan_name}' has been successfully updated."




def get_plans_for_date(requested_date_str):
    file_path = 'my_calendar/calendar.json'
    if not os.path.exists(file_path):
        print("Calendar file does not exist.")
        return []
    with open(file_path, 'r') as file:
        data = json.load(file)

    try:
        requested_date = datetime.datetime.strptime(requested_date_str,
                                                    '%m/%d/%Y')
    except ValueError:
        print("Invalid date format. Use MM/DD/YYYY.")
        return []

    plans_for_date = []
    for plan in data.get('plans', []):
        plan_date = datetime.datetime.strptime(plan['date'], '%m/%d/%Y')

        if plan_date.date() == requested_date.date():
            plans_for_date.append(plan)

    if plans_for_date:
        plan_details = "Here are your plans for {}:\n".format(
            requested_date_str)
        for plan in plans_for_date:
            plan_details += f"Name: {plan['name']}, Start Time: {plan['start_time']}, End Time: {plan['end_time']}\n"
        return plan_details
    else:
        return f"No plans for {requested_date_str}."






def search_and_organize_results(query, save_path="nexus/database/compiled_database.csv", num_results=20):
    try:
        # Prepare the search URL
        google_url = "https://www.google.com/search"
        params = {"q": query, "num": num_results}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

        # Send the request
        response = requests.get(google_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the search results with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.select(".tF2Cxc")  # Google search result container

        # Extract and organize results
        data = []
        for result in search_results[:num_results]:
            title = result.select_one("h3").text if result.select_one("h3") else "No title"
            link = result.select_one("a")["href"] if result.select_one("a") else "No link"
            snippet = result.select_one(".VwiC3b").text if result.select_one(".VwiC3b") else "No snippet"

            data.append({"Title": title, "Link": link, "Snippet": snippet})

        df = pd.DataFrame(data)

        # Save data to a file
        if save_path.endswith('.csv'):
            df.to_csv(save_path, index=False)
        elif save_path.endswith('.json'):
            df.to_json(save_path, orient='records', indent=4)
        elif save_path.endswith('.xlsx'):
            df.to_excel(save_path, index=False)
        else:
            raise ValueError("Unsupported file format. Use .csv, .json, or .xlsx.")

        return f"Results saved to {save_path}."

    except Exception as e:
        return f"Error: {e}"