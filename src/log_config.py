# src/log_config.py
import logging
import os
import sys

def setup_logging():
    # Caminho dinâmico para garantir que funcione em qualquer OS
    # Sobe dois níveis a partir deste arquivo (src -> root -> logs)
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, 'app_logs.log')

    # Verifica se já tem handlers para não duplicar logs ao recarregar a página
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(LOG_FILE)
            ]
        )
