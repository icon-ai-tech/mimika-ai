from config.loader import load_config
from utils.logger import setup_logger

from audio.audio_input import get_audio_stream
from animation.lipsync import generate_lipsync
from render.virtual_camera import stream_to_virtual_camera

logger = setup_logger()

def run_pipeline() -> None:
    """
    Основной запуск всей цепочки обработки:
    1. Загрузка конфига
    2. Получение аудиопотока
    3. Генерация лицевой анимации (липсинк)
    4. Потоковое отображение в виртуальную камеру
    """
    try:
        logger.info("Инициализация конфигурации")
        cfg = load_config()

        logger.info("Запуск получения аудиопотока")
        audio_data = get_audio_stream(cfg)

        logger.info("Генерация кадров лицевой анимации")
        frames = generate_lipsync(audio_data, cfg)

        logger.info("Запуск потока в виртуальную камеру")
        stream_to_virtual_camera(frames, cfg)

        logger.info("Pipeline завершён успешно")

    except Exception as e:
        logger.exception(f"Ошибка во время выполнения pipeline: {e}")
