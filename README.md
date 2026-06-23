# Rings Atelier — Vue 3 + Vite + FastAPI

Frontend для сайта студии Rings Atelier. Форма заявок отправляет данные на backend (FastAPI), который сохраняет их в SQLite и шлёт уведомление в Telegram.

## Структура

- `src/` — Vue 3 frontend
- `backend/` — FastAPI backend (Python)

## Настройка

### 1. Backend

```bash
cd backend

# создать виртуальное окружение (опционально, но рекомендуется)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# установить зависимости
pip install -r requirements.txt

# скопировать пример env и заполнить
cp .env.example .env
```

Отредактируй `backend/.env`:

```env
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
CORS_ORIGINS=http://localhost:5173,http://localhost:4173
DATABASE_URL=sqlite:///./leads.db
```

- `BOT_TOKEN` — получи у [@BotFather](https://t.me/botfather).
- `CHAT_ID` — свой ID можно узнать через [@userinfobot](https://t.me/userinfobot). Если бот пишет в группу, укажи ID группы (со знаком `-`).

Запуск backend:

```bash
uvicorn main:app --reload --port 8000
```

Документация API будет доступна по адресу: http://localhost:8000/docs

### 2. Frontend

```bash
# в корне проекта
cp .env.example .env
npm install
npm run dev
```

Frontend запустится на http://localhost:5173.

## Продакшен

1. Укажи реальный URL backend в корневом `.env`:
   ```env
   VITE_API_URL=https://your-domain.com
   ```
2. Укажи продакшен-домен frontend в `backend/.env`:
   ```env
   CORS_ORIGINS=https://your-domain.com
   ```
3. Собери frontend: `npm run build`.

## Зависимости

- Frontend: Vue 3, Vue Router, Vite
- Backend: FastAPI, SQLAlchemy, Pydantic Settings, aiohttp, Uvicorn
