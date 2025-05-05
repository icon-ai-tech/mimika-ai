from typing import List, Dict, Any
import time

def stream_to_virtual_camera(frames: List[Any], cfg: Dict[str, Any]) -> None:
    """
    Потоковая подача сгенерированных кадров в виртуальную камеру (например, через OBS).

    :param frames: Список кадров (например, PIL.Image)
    :param cfg: Конфиг
    """
    frame_rate = cfg["output"].get("frame_rate", 30)
    delay = 1.0 / frame_rate

    print(f"📡 Начинаем отправку кадров в виртуальную камеру с частотой {frame_rate} fps")

    for i, frame in enumerate(frames):
        # Здесь должна быть интеграция с OBS или pyvirtualcam
        print(f"Кадр {i + 1} отправлен")
        time.sleep(delay)

    print("✅ Все кадры отправлены")
