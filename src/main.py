from app import app_system
import logging
import sys
from typing import NoReturn

def configure_logging() -> None:
    """Configura o sistema de logging para a aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

def graceful_exit(message: str, exit_code: int = 0) -> NoReturn:
    """Encerra a aplicação de forma controlada com mensagem apropriada."""
    logging.info(message)
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        configure_logging()
        logging.info("Iniciando aplicação RAG Chat")
        app_system()
        graceful_exit("Aplicação encerrada normalmente")
    except KeyboardInterrupt:
        graceful_exit("\nAplicação interrompida pelo usuário")
    except Exception as e:
        logging.error(f"Erro fatal: {str(e)}", exc_info=True)
        graceful_exit(f"Aplicação encerrada devido a um erro: {str(e)}", 1)