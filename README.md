# 🎭 Mimika-AI

**Многофункциональная платформа для создания реалистичных цифровых аватаров с лицевой анимацией и озвучкой на базе ИИ**

![Demo](assets/portrait.gif)

`Mimika-AI` позволяет превращать аудиопоток в живое видео с синхронизированным движением губ и мимикой. Система ориентирована на реальное применение: цифровые ассистенты, онлайн-встречи, обучение и виртуальное присутствие.

---

## 🧠 Описание

**Mimika-AI** использует модульную архитектуру, чтобы обрабатывать аудиовход, генерировать последовательность лицевых движений, визуализировать результат и выводить его через виртуальную камеру (например, OBS).

Основные компоненты:
- `audio`: работа с аудиовходом и его анализ
- `animation`: генерация лицевой анимации по аудиопотоку
- `model`: обёртки и загрузка моделей, таких как SadTalker
- `render`: отображение и вывод видео
- `core`: общий pipeline и управляющая логика
- `config`: конфигурация и загрузка параметров
- `utils`: логи, хелперы, вспомогательные инструменты

---

## 📁 Структура проекта

```

mimika-ai/
├── assets/                         # Демо-данные и аватары
│   └── portrait.gif
├── data/                           # (пусто) — место для моделей и пользовательских данных
├── docs/                           # Документация проекта
├── mimika\_ai/                      # Основной исходный код
│   ├── audio/
│   │   ├── **init**.py
│   │   ├── audio\_input.py
│   │   └── voice\_analysis.py
│   ├── animation/
│   │   ├── **init**.py
│   │   ├── frame\_generator.py
│   │   └── lipsync.py
│   ├── model/
│   │   ├── **init**.py
│   │   ├── base\_model.py
│   │   └── sadtalker\_wrapper.py
│   ├── render/
│   │   ├── **init**.py
│   │   └── virtual\_camera.py
│   ├── config/
│   │   ├── **init**.py
│   │   └── loader.py
│   ├── core/
│   │   ├── **init**.py
│   │   └── pipeline.py
│   ├── utils/
│   │   ├── **init**.py
│   │   ├── logger.py
│   │   └── helpers.py
│   └── **init**.py
├── tests/                          # Тесты
│   └── test\_instance.py
├── pyproject.toml                  # Настройка Poetry
├── poetry.lock
├── setup.py
├── mkdocs.yml                      # Документация через mkdocs
├── LICENSE
└── README.md

````

---

## 🚀 Быстрый старт

### 1. Установка окружения

```bash
git clone https://github.com/icon-ai-tech/mimika-ai.git
cd mimika-ai
poetry install
````

### 2. Запуск пайплайна

```bash
poetry run python -m mimika_ai.core.pipeline \
    --audio_path assets/demo_audio.wav \
    --avatar_path assets/avatar_samples/avatar1.png
```

---

## 🧩 Возможности

* 🎤 **Генерация лицевой анимации** по аудиопотоку
* 🔁 **Обработка в реальном времени** с сохранением эмоций
* 🧠 **Модульный pipeline**: от звука до видео
* 🎥 **Поддержка виртуальной камеры** (OBS)
* 🎨 **Настраиваемые аватары**: поддержка кастомных изображений
* ⚙️ **Гибкая архитектура**: легко подключить новую модель

---

## 📜 Архитектура

```mermaid
graph TD
    A[Mic input / Audio file] --> B[AudioInput]
    B --> C[VoiceAnalysis]
    C --> D[LipSync Model (SadTalker)]
    D --> E[FrameGenerator]
    E --> F[VirtualCamera / Renderer]
    F --> G[OBS output → Zoom / Meet / etc.]
```

---

## 🧪 Тестирование

```bash
poetry run pytest tests/
```

---

## 📅 Roadmap

* [x] Модуль lip-sync с SadTalker
* [x] OBS-интеграция
* [ ] Рендеринг в реальном времени
* [ ] GUI для выбора аватара и настройки
* [ ] MVP веб-интерфейса
* [ ] Поддержка кастомных моделей и языков

---

## 📘 Документация

Полная документация доступна через [MkDocs](https://www.mkdocs.org/):

```bash
mkdocs serve
```

Откроется на [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🤝 Контакты

Разработка: [icon-ai.tech@yandex.ru](mailto:icon-ai.tech@yandex.ru)
Москва, Россия

---

## 📄 Лицензия

Этот проект лицензирован под MIT License. Подробности — в [LICENSE](LICENSE).

```

---

Готов добавить поддержку CLI-интерфейса или `demo.ipynb`, если ты хочешь показать работу через Jupyter. Хочешь включить его в README?
```
