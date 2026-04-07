# Wallet Tracker

REST API для отслеживания транзакций Solana-кошельков в реальном времени через [Helius](https://helius.dev) webhooks

## Стек

- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Helius** - получение on-chain событий по вебхуку
- **Docker** + **docker-compose**

---

## Настройка перед запуском

### 1. Получи Webhook URL

**Локальная разработка** - запусти туннель (пример для ngrok):

```bash
ngrok http 8000
```

Скопируй выданный HTTPS-адрес, например `https://abc123.ngrok.io` - это и будет твой Webhook URL

**Продакшн** - используй свой домен: `https://yourdomain.com`

### 2. Регистрация на Helius и создание вебхука

1. Зарегистрируйся на [helius.dev](https://helius.dev) и получи **API Key** в дашборде.
2. Перейди в раздел **Webhooks** → **New Webhook**.
3. В поле **Webhook URL** укажи адрес из шага 1: `<your-url>/webhook/helius`
4. Выбери тип транзакций для отслеживания `SWAP` и `TRANSFER`
5. В поле **Auth Header** задай произвольный секретный токен - он будет использоваться для верификации входящих запросов
6. Сохрани вебхук и скопируй его **Webhook ID**

### 3. Заполнение .env

Скопируй `.env.example` и заполни переменные

---

## Запуск

```bash
make up
```

Приложение будет доступно на `http://localhost:8000`
Документация: `http://localhost:8000/docs`

### Другие команды

| Команда | Описание |
|---|---|
| `make up` | Запустить контейнеры |
| `make down` | Остановить контейнеры |
| `make restart` | Перезапустить контейнеры |
| `make build` | Пересобрать образы |

---

## API

| Метод | Путь | Описание |
|---|---|---|
| `POST` | `/subscriptions` | Добавить кошелёк для отслеживания |
| `GET` | `/subscriptions` | Список всех подписок |
| `DELETE` | `/subscriptions/{wallet_address}` | Удалить подписку |
| `GET` | `/transactions/{wallet_address}` | История транзакций кошелька |
| `POST` | `/webhook/helius` | Эндпоинт для входящих событий Helius |


## Тесты

```bash
pytest tests
```
