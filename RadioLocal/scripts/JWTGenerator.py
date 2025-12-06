import jwt
import os
import pyperclip
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Path to .env in the parent directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

# Load environment variables if .env exists
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

# Get secret key from env or fallback
secret_key = os.getenv("JWT_SECRET", "supersecretkey")

# Define payload
payload = {
    "company_id": "0",
    "exp": datetime.utcnow() + timedelta(hours=1)
}

# Generate JWT
token = jwt.encode(payload, secret_key, algorithm="HS256")
print(token)

# Copy to clipboard
pyperclip.copy(token)

print("token copied to clipboard")

