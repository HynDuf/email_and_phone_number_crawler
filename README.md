# Emails and Phone number Crawler 

Given a root URL and a depth, it crawls all emails and phone numbers.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)

### Steps to Setup

1. **Clone the repository:**
   
   If you haven't already cloned the repository, do so with the following command:
   
   ```sh
   git clone https://github.com/HynDuf/email_and_phone_number_crawler.git
   cd email_and_phone_number_crawler
   ```

2. **Create a virtual environment:**

   Create a virtual environment to isolate the project dependencies.
   
   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:
     
     ```sh
     venv\Scripts\activate
     ```
   
   - On macOS and Linux:
     
     ```sh
     source venv/bin/activate
     ```

4. **Install the required packages:**

   Install the required packages using `pip` and the `requirements.txt` file.
   
   ```sh
   pip install -r requirements.txt
   ```

5. **Run the main script:**

   Run the `main.py` script.
   
   ```sh
   python main.py
   ```

### Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment with:

```sh
deactivate
```

## Additional Information

### Requirements

The `requirements.txt` file contains the following dependencies:

```
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.2
openpyxl==3.0.10
```

### Project Structure

A brief explanation of the project structure:

```
yourproject/
│
├── crawler.py          -> The main crawler algorithm
├── database.py         -> Sqlite3 database operations
├── gui.py              -> The Tkinter GUI
├── main.py             -> Run this to start the program
├── requirements.txt
└── README.md
```
### Export to .exe on Windows

```
pip install pyinstaller
```
Then
```
pyinstaller --onefile main.py
```
You will see a `/dist/main.exe` file. Run and enjoy.

### Docker
```
docker build -t my-python-gui-app .
```

Run the app
```
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix my-python-gui-app
```

The "Export to Excel" functionality will export file to the docker directory.
- On Windows, the path looks like this: `\\wsl.localhost\docker-desktop-data\data\docker\overlay2\4aaf2f0d5484890425d98f17a2790072694941acc07f9f154a33bf08f1fcedce\diff\usr\src\app`
