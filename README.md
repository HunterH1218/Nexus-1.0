# Nexus AI Assistant

Nexus is an AI assistant designed to provide various helpful functionalities like calendaring, file management, weather updates, and more. It utilizes external APIs and Python libraries to enrich its features.

## Features

- **AI Conversation**: Engage with Nexus through an interactive console.
- **Weather Information**: Retrieve current weather updates.
- **File Operations**: Create, read, and delete files and directories.
- **Calendar Management**: Add, edit, and delete plans.
- **Web Search**: Search for information using the Google search engine.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/nexus-ai-assistant.git
   cd nexus-ai-assistant
   ```

2. **Install Dependencies**
   Ensure you have Python 3.11 or later installed. You can check your Python version with:
   ```bash
   python3 --version
   ```
3. **Install Required Packages**
   Use pip to install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the AI assistant with the entry point script:
```bash
python3 main.py
```

Now, you can interact with Nexus by typing in the console. You can try things like:
* "Create a file named test.txt"
* "Add a plan for March 15th: meeting from 10:00 AM to 11:00 AM."
* "What's the weather"
> You will need to configure your latitude and longitude in nexus/weather/current.py for weather to work

## Project Structure
* main.py: The main script to interact with the Nexus AI Assistant.
* nexus/functions/: Directory containing various utility functions (e.g., file operations, calendar management).
* nexus/weather/: Contains modules for fetching and processing weather data.
* pyproject.toml: Project dependency and configuration file.
* .replit: Configuration file for the Replit environment.

## Contributing
We welcome contributions! Please fork the repository and submit a pull request for any bug fixes or enhancements.

