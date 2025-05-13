# Frida Codeshare

## Description

Frida Codeshare is allows users to share and discover Frida scripts. It provides a platform for developers to collaborate, learn, and enhance their skills in reverse engineering and dynamic instrumentation using Frida.

## Development

### Prerequisites
- Python 3.12 or higher
- pip or uv (I use uv in the below setup)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/frida/frida-codeshare
   cd frida-codeshare
    ```
2. Create a virtual environment:
   ```bash
   uv venv
   source venv/bin/activate
   ```

3. Create an environment file:
   ```bash
    SECRET_KEY="aaaa"
    AUTH0_CLIENT_SECRET="aaaa"
    DEBUG=True
   ```

3. Install the required packages:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
    uv run manage.py runserver
   ```

5. Open your web browser and navigate to `http://localhost:8000` to access the Frida Codeshare web application.