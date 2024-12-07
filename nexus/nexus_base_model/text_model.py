import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 0.85,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

with open('nexus/nexus_base_model/training_data/text_model.txt', 'r', encoding='UTF-8') as file:
  file_contents = file.read()
  
memory = []

def generate_response(prompt):
  response = model.generate_content([
    file_contents,
    *memory,
    f"input: {prompt}",
    "output: ",
  ])
  memory.append(f"input: {prompt}")
  memory.append(f"output: {response.text}")
  return response.text