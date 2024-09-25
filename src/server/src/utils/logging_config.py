import logging
import os
from pathlib import Path

# Definir o diretório onde os logs serão armazenados
log_directory = Path("./logs")
log_directory.mkdir(exist_ok=True)

# Definir o caminho do arquivo de log
log_file = log_directory / "system.log"

# Configurar o logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Obter uma instância do logger
logger = logging.getLogger(__name__)
