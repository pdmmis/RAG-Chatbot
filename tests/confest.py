# from sys
# from pathlib import Path
# PROJECT_ROOT = Path(__file__).resolve().parent
# sys.path.insert(0, str(PROJECT_ROOT))
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


