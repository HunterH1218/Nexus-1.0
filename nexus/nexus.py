from nexus.functions import run_functions
from nexus.functions.argument_model import argument_assignment
from nexus.nexus_base_model import text_model

def main(prompts):
  results = []
  prompt_list = prompts.split(';')

  for prompt in prompt_list:
      prompt = prompt.strip()
      if not prompt:
          continue
      response = argument_assignment.generate_response(prompt)
      if "none" in response.strip():
          results.append(text_model.generate_response(prompt))
      else:
          results.append(run_functions.run_functions(prompt))
      if results == "":
          return "No results returned. Please check if the function that was ran returns the answer, not prints it."
      elif results != "":
          return "\n".join(results)

