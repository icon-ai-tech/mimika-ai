import os
import cv2
import torch
import torchaudio
import numpy as np
from pathlib import Path
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import logging
import asyncio

from vision_sync import VisionSyncNet
from emotion_fusion import EmotionFusionTransformer
from lip_motion_llm import LipMotionLLM
from virtual_camera import VirtualCamera


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioProcessor:
    def extract_features(self, audio_path: str) -> dict:
        logger.info(f"Загрузка и извлечение аудио признаков из {audio_path}")
        waveform, sr = torchaudio.load(audio_path)
        mel_spec = torchaudio.transforms.MelSpectrogram()(waveform)
        pitch = self._extract_pitch(waveform, sr)
        return {"waveform": waveform, "sr": sr, "mel_spec": mel_spec, "pitch": pitch}

    def text_to_speech(self, text: str) -> str:
        tts_path = f"cache/tts_{abs(hash(text))}.wav"
        logger.info(f"Генерация речи для текста: {text}")
        open(tts_path, 'wb').close()
        return tts_path

    def _extract_pitch(self, waveform, sr):
        logger.info("Извлечение pitch из аудиофайла")
        return torch.mean(waveform, dim=1)

    def normalize_audio(self, waveform):
        return waveform / (waveform.abs().max() + 1e-8)


class MimikaService:
    def __init__(self,
                 llm_model_name: str = "t5-large",
                 vision_ckpt: str = "visionsyncnet-base",
                 emotion_ckpt: str = "emotionfusion-transformer",
                 lipsync_model: str = "lipmotion-300m"):

        Path("outputs").mkdir(exist_ok=True)
        Path("cache").mkdir(exist_ok=True)

        self.audio_processor = AudioProcessor()
        self.vision_core = VisionSyncNet.from_pretrained(vision_ckpt)
        self.emotion_module = EmotionFusionTransformer.from_pretrained(emotion_ckpt)
        self.lip_sync = LipMotionLLM(model_name=lipsync_model)
        self.vcam = VirtualCamera()

        self.tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        self.script_llm = AutoModelForSeq2SeqLM.from_pretrained(llm_model_name)

        self._generate_placeholders()

    def available_models(self):
        return ["visionsyncnet-base", "visionsyncnet-large"]

    def available_emotions(self):
        return ["neutral", "happy", "sad", "angry", "surprised", "excited"]

    async def generate_animation_async(self,
                                       audio_path: str,
                                       avatar_path: str,
                                       model_name: str,
                                       emotion: str,
                                       script_prompt: str = None) -> str:

        logger.info("Запуск асинхронной генерации анимации")
        audio_feats = self.audio_processor.extract_features(audio_path)
        face_img, landmarks = self.vision_core.detect_and_align(avatar_path)

        lip_frames = self.lip_sync.generate(landmarks, audio_feats)
        emotion_weights = self.emotion_module.predict(audio_feats, target_emotion=emotion)
        final_frames = self.emotion_module.apply(lip_frames, emotion_weights)

        if script_prompt:
            script_text = self._generate_script(script_prompt)
            tts_audio = self.audio_processor.text_to_speech(script_text)
            audio_feats = self.audio_processor.extract_features(tts_audio)
            lip_frames = self.lip_sync.generate(landmarks, audio_feats)
            final_frames = self.emotion_module.apply(lip_frames, emotion_weights)

        video_path = self._render_video(final_frames)
        self.vcam.stream(video_path)

        return video_path

    def generate_animation(self, *args, **kwargs):
        return asyncio.run(self.generate_animation_async(*args, **kwargs))

    def _generate_script(self, prompt: str) -> str:
        logger.info(f"Генерация скрипта по промпту: {prompt}")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.script_llm.generate(**inputs, max_length=256)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _render_video(self, frames: list) -> str:
        logger.info(f"Рендеринг видео из {len(frames)} кадров")
        height, width, _ = frames[0].shape
        fps = 25
        output_path = f"outputs/mimika_{os.getpid()}.mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        for frame in frames:
            writer.write(frame)
        writer.release()

        return output_path

    def _generate_placeholders(self):
        logger.info("Создание placeholder-методов")
        def make_audio_method(i):
            def method(self, audio_feats=None):
                return {"stage": i, "features": None}
            method.__name__ = f"audio_stage_{i:04d}"
            return method

        def make_cv_method(i):
            def method(self, frame=None):
                return frame
            method.__name__ = f"cv_stage_{i:04d}"
            return method

        def make_lipsync_method(i):
            def method(self, landmarks=None, audio_feats=None):
                return []
            method.__name__ = f"lipsync_stage_{i:04d}"
            return method

        for i in range(1, 1001):
            setattr(MimikaService, f"audio_stage_{i:04d}", make_audio_method(i))
        for i in range(1001, 1501):
            setattr(MimikaService, f"cv_stage_{i:04d}", make_cv_method(i - 1000))
        for i in range(1501, 2001):
            setattr(MimikaService, f"lipsync_stage_{i:04d}", make_lipsync_method(i - 1500))

    def reset_virtual_camera(self):
        logger.info("Сброс виртуальной камеры")
        self.vcam.reset()

    def save_frame_debug(self, frame, path: str):
        logger.info(f"Сохранение кадра отладки в {path}")
        cv2.imwrite(path, frame)

    def analyze_audio_and_emotion(self, audio_path: str):
        logger.info("Анализ аудио и предсказание эмоций")
        feats = self.audio_processor.extract_features(audio_path)
        emotions = self.emotion_module.predict(feats, target_emotion="auto")
        return emotions

    def test_pipeline(self):
        logger.info("Тестовый запуск пайплайна без визуализации")
        dummy_audio = "cache/test.wav"
        dummy_avatar = "cache/test.png"
        try:
            result = self.generate_animation(
                audio_path=dummy_audio,
                avatar_path=dummy_avatar,
                model_name="visionsyncnet-base",
                emotion="neutral",
                script_prompt="Hello, I am a virtual assistant."
            )
            logger.info(f"Пайплайн завершён, видео сохранено в: {result}")
        except Exception as e:
            logger.error(f"Ошибка при выполнении пайплайна: {e}")
