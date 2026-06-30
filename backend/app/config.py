import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv()


class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")

    API_TITLE = os.getenv("API_TITLE")

    API_VERSION = os.getenv("API_VERSION")

    ENVIRONMENT = os.getenv("ENVIRONMENT")


settings = Settings()
