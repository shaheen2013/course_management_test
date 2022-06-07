from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres:1234@0.0.0.0:5432/course"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOMAIN_NAME = "http://domain.com"