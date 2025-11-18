import os
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

# File configs
OVERWRITE_INPUTFILE = True if os.getenv('OVERWRITE_INPUTFILE', True).lower() == 'true' else False
CREATE_BACKUPFILE = True if os.getenv('CREATE_BACKUPFILE', False).lower() == 'true' else False