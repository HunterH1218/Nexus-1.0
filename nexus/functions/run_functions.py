import re
from nexus.functions.argument_model import argument_assignment
from nexus.functions.functions import *


def function_call(prompt):
  # Generate a response from the model
  result = argument_assignment.generate_response(prompt)

  def parse_input(input_text):
      lines = input_text.splitlines()
      result = []
      for line in lines:
          match = re.match(r"(.*) = (.*)", line)
          if match:
              key, value = match.groups()
              result.append((key.strip(), value.strip()))
      return result

  # Parse the result
  parsed = parse_input(result)

  # Convert parsed list to dictionary
  args = {key: value for key, value in parsed if key != "function_name"}

  # Initialize function_name
  function_name = None

  # Determine which function to call
  for key, value in parsed:
      if key == "function_name":
          function_name = value
          break

  if function_name is None:
      return "Invalid input: No function name specified"

  # Call the appropriate function with arguments
  if function_name == "write_file":
      result_var = write_file(**args)
  elif function_name == "create_folder":
      result_var = create_folder(**args)
  elif function_name == "delete_file":
      result_var = delete_file(**args)
  elif function_name == "delete_folder":
      result_var = delete_folder(**args)
  elif function_name == "move_item":
      result_var = move_item(**args)
  elif function_name == "read_file":
      result_var = read_file(**args)
  elif function_name == "list_folder_contents":
      result_var = list_folder_contents(**args)
  elif function_name == "date":
      result_var = date()
  elif function_name == "time":
      result_var = time(**args)
  elif function_name == "get_weather":
      result_var = get_weather()
  elif function_name == "add_plan":
      result_var = add_plan(**args)
  elif function_name == "get_todays_plans":
      result_var = get_todays_plans()
  elif function_name == "time_until_next_plan":
      result_var = time_until_next_plan()
  elif function_name == "delete_past_plans":
      result_var = delete_past_plans()
  elif function_name == "edit_plan":
      result_var = edit_plan(**args)
  elif function_name == "get_plans_for_date":
      result_var = get_plans_for_date(**args)
  elif function_name == "search_and_organize_results":
      result_var = search_and_organize_results(**args)
  elif function_name == "get_seven_day_forecast":
      result_var = get_seven_day_forecast(**args)
  elif function_name == "convert_units":
      result_var = convert_units(**args)
  else:
      result_var = "An error has occurred sir, no function found."

  return result_var



def run_functions(prompt):
  return(function_call(prompt))



