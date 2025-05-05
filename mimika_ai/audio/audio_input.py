import sounddevice as sd
import numpy as np
from typing import Any, Dict

def get_audio_stream(cfg: Dict[str, Any]) -> np.ndarray:
    """
    Получает аудиопоток с микрофона в виде NumPy массива.

    :param cfg: Конфигурационный словарь
    :return: Аудиоданные
    """
    sample_rate = cfg["audio"].get("sample_rate", 16000)
    duration = cfg["audio"].get("duration", 5)  # секунды

    print("▶ Запись аудио... Говорите!")

    try:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        print("✅ Аудио записано успешно")
        return audio.flatten()
    except Exception as e:
        raise RuntimeError(f"Не удалось записать аудио: {e}")
