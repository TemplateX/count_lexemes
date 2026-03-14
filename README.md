# Анализатор словоформ (TXT → XLSX)

Сервис на **FastAPI** для морфологического анализа текстовых файлов.  
Загрузите `.txt` файл — получите Excel-отчёт с частотой употребления каждой словоформы (по всему файлу и построчно).

## Как это работает

1. Вы отправляете текстовый файл через POST-запрос на `/public/report/export`.
2. Сервер возвращает уникальный идентификатор (`file_id`).
3. Файл асинхронно обрабатывается:
   - текст разбивается на строки;
   - выделяются **словоформы** (с помощью `pymorphy2`);
   - подсчитывается количество вхождений каждой словоформы в каждой строке и суммарно по файлу.
4. Результат сохраняется в `.xlsx` файл с тремя столбцами:
   - **Словоформа**
   - **Всего (по файлу)**
   - **В каждой строке** (подробная разбивка по строкам)
5. Готовый отчёт можно скачать по ссылке:  
   `GET /public/report/export/{file_id}`

## Технологии

- Python 3.9+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) (ASGI-сервер)
- [OpenPyXL](https://openpyxl.readthedocs.io/) + [pandas](https://pandas.pydata.org/) (для генерации Excel)
- [pymorphy2](https://pymorphy2.readthedocs.io/) (морфологический анализ)

## Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/TemplateX/count_lexemes.git
cd count_lexemes
```

### 2. Создайте виртуальное окружение и установите зависимости
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
pip install -r requirements.txt
```

### 3. Запустите сервер
```bash
python main.py
```
Сервер будет доступен по адресу `http://127.0.0.1:8000`.

Документация API (Swagger) автоматически доступна по `/docs`.

## Использование API

### Загрузить файл и получить `file_id`

**Запрос:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/public/report/export' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@example.txt;type=text/plain'
```
**Ответ:**
```json
{
  "status": "processing",
  "name": "example.txt",
  "file_id": "bd0e864f-eaac-4db7-8519-69f0f20066c8"
}
```

### Скачать готовый отчёт

**Запрос:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/public/report/export/bd0e864f-eaac-4db7-8519-69f0f20066c8' \
  -H 'accept: application/json'
```
Файл `Ответ.xlsx` будет сохранён в загрузки.

## Примечания

- Для корректной работы морфологического анализатора может потребоваться скачать словари `pymorphy2`. Обычно они устанавливаются автоматически вместе с библиотекой.
- Если вы планируете развернуть сервер на удалённой машине, не забудьте настроить CORS и использовать `--host 0.0.0.0` при запуске uvicorn.

## Лицензия

MIT
