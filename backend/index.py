import os
import sys

# Add current directory to sys.path so 'app' module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set HOME to /tmp for serverless environments
os.environ["HOME"] = "/tmp"

from app.main import app
