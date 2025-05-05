import streamlit as st
from mimika_service import MimikaService
import tempfile
import shutil
import os

service = MimikaService()

st.set_page_config(page_title="Mimika Avatar Generator", layout="centered")

st.title("🧠 Mimika: Генерация цифрового аватара")
st.write("Загрузите аудио и изображение аватара, выберите эмоцию — и получите видео с озвучкой и мимикой!")

audio_file = st.file_uploader("🎧 Загрузите аудиофайл (WAV)", type=["wav"])
avatar_file = st.file_uploader("🧑 Загрузите изображение аватара (JPG/PNG)", type=["jpg", "jpeg", "png"])

model_name = st.selectbox("🧠 Модель Vision", service.available_models())
emotion = st.selectbox("😊 Эмоция", service.available_emotions())
script_prompt = st.text_input("📝 Текстовый промпт (опционально)", "")

generate_button = st.button("🚀 Сгенерировать видео")

if generate_button and audio_file and avatar_file:
    with st.spinner("⏳ Генерация видео..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                shutil.copyfileobj(audio_file, temp_audio)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_avatar:
                shutil.copyfileobj(avatar_file, temp_avatar)

            result_path = service.generate_animation(
                audio_path=temp_audio.name,
                avatar_path=temp_avatar.name,
                model_name=model_name,
                emotion=emotion,
                script_prompt=script_prompt if script_prompt else None
            )

            st.success("✅ Видео успешно сгенерировано!")
            st.video(result_path)
            with open(result_path, "rb") as f:
                st.download_button("📥 Скачать видео", data=f, file_name="mimika_avatar.mp4", mime="video/mp4")

        except Exception as e:
            st.error(f"❌ Ошибка: {e}")
else:
    st.info("⚠️ Пожалуйста, загрузите аудио и изображение.")




