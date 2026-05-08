"""
Quick script to check if environment variables are loaded correctly
Run this in Railway to debug environment variable issues
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("Environment Variables Check")
print("=" * 50)

env_vars = [
    "DATABASE_URL",
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "PORT"
]

for var in env_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if var in ["DATABASE_URL", "SECRET_KEY"]:
            masked = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {masked}")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: NOT SET")

print("=" * 50)
