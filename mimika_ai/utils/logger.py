import logging

def setup_logger(name: str = "MimikaAI") -> logging.Logger:
    """
    Устанавливает и возвращает логгер для проекта.

    :param name: Имя логгера
    :return: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
