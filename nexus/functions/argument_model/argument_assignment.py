import os
import google.generativeai as genai
import datetime
import pytz


def date():
  try:
      today = datetime.datetime.now().strftime("%m/%d/%Y")
  except Exception as e:
      print(e)
      today = False
  return today
def time(timezone='EST'):
  try:
      tz = pytz.timezone(timezone)
      current_time = datetime.datetime.now(tz).strftime("%I:%M %p")
  except Exception as e:
      print(e)
      current_time = False
  return current_time
def tomorrows_date():
  try:
      tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
      return tomorrow.strftime("%m/%d/%Y")
  except Exception as e:
      print(e)
      return False

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

with open("nexus/functions/argument_model/argument_training_data.txt", "r") as f:
  training_data = f.read()

with open("nexus/functions/argument_model/functions.txt", "r") as f:
  functions = f.read()

time_1 = time()
date_1 = date()
tomorrow_date_1 = tomorrows_date()



memory = []

def generate_response(prompt):
  response = model.generate_content([
    functions,
    training_data,
    "input: make an event from 3:00 to 4:00 tommorrow",
    f"output: ```\nfunction_name = add_plan\nname = event\ndate = {tomorrow_date_1}\nstart_time = 3:00 PM\nend_time = 4:00 PM",
    "input: plans for tommorrow",
    f"output: ```\nfunction_name = get_plans_for_date\nrequested_date_str = {tomorrow_date_1}",
    "input: events for today"
    f"output: ```\nfunction_name = get_todays_plans```"
    f"input: {prompt}",
    "output: ",
  ])
  memory.append(f"input: {prompt}")
  memory.append(f"output: {response.text}")
  return response.text