from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres:1234@0.0.0.0:5432/course"
