from dotenv import load_dotenv
import os

load_dotenv()
print("EMAIL_SENDER:", os.getenv("EMAIL_SENDER"))
print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))