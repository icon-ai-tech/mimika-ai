from typing import Any, Dict, List
from model.sadtalker_wrapper import SadTalkerWrapper

def generate_lipsync(audio_data: Any, cfg: Dict[str, Any]) -> List[Any]:
    """
    Генерирует лицевую анимацию (кадры) из аудиоданных.

    :param audio_data: NumPy массив с аудио
    :param cfg: Конфигурация
    :return: Список сгенерированных кадров
    """
    print("🚀 Инициализация модели SadTalker для генерации липсинка...")
    model = SadTalkerWrapper(cfg)

    print("🎬 Генерация кадров из аудио...")
    frames = model.infer(audio_data)

    print(f"✅ Сгенерировано {len(frames)} кадров")
    return frames
