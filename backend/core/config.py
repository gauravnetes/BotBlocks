import os 
from dotenv import load_dotenv

load_dotenv()

class Settings: 
    PROJECT_NAME: str = "BotBlocks"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
settings = Settings()