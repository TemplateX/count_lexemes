# count_lexemes
FastAPI сервис для частотного анализа txt. Выделяет словоформы, считает вхождения в каждой строке и во всем файле, генерирует .xlsx отчет. Два эндпоинта: POST /public/report/export (загрузить файл, получить file_id) и GET /public/report/export/{file_id} (скачать отчет). Развертывание через Uvicorn.
