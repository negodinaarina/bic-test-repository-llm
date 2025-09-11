# Тестовое задание: FastAPI + LLM Benchmark

## Уровни выполнения

### Уровень 1 — Минимально рабочее решение

* [x] Поднять FastAPI-сервер.
* [x] `GET /models` — вернуть список моделей, например:

  ```
  deepseek/deepseek-chat-v3.1:free
  z-ai/glm-4.5-air:free
  moonshotai/kimi-k2:free
  ```
* [x] `POST /generate`:

  * принимает `prompt`, `model`;
  * вызывает OpenRouter (OpenAI-совместимый формат) через `requests.post`;
  * возвращает ответ модели (текст).
* [x] API-ключ: из `.env` (через `dotenv`)
* [x] Логирование ошибок в `server_logs.txt`.

---

### Уровень 2 — Продвинутая реализация

* [x] `POST /generate`:

  * параметр `max_tokens` (по умолчанию 512);
  * вернуть JSON с `response`, `tokens_used`, `latency_seconds`;
  * глобальный обработчик 429 с экспоненциальным `retry`.
* [x] `POST /benchmark`:

  * вход: `prompt_file` (txt, по строкам), `model`, `runs` (int, дефолт 5);
  * метрики latency: `avg`, `min`, `max`, `std_dev`;
  * сохранить `benchmark_results.csv`;
  * вернуть JSON со статистикой.

---

### Уровень 3 — Профессиональное решение

* [ ] `/generate`: при `stream=true` — **SSE-стриминг**.
* [ ] `/benchmark`: при `visualize=true` — вернуть **HTML-таблицу**.
* [X] Провести 10 тестов: 5 для `/generate` (разные модели, включая stream), 5 для `/benchmark` (≥3 промпта, разные `runs`).
* [ ] Замерить общую latency (например, `curl -w "%{time_total}"`).
* [ ] Сравнительная таблица моделей (средняя задержка + `std_dev`).
* [X] Приложить: `benchmark_results.csv`, `server_logs.txt`, скриншоты ответов.

