import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import uuid
from morphing import count_morphed_usages

responses = []

app = FastAPI()


@app.post("/public/report/export", name="Загрузить файл на сервер", tags=["Работа с файлами 📄"])
async def create_upload_file(file: UploadFile, bg_task: BackgroundTasks):
    file_id = str(uuid.uuid4())
    with open(f"uploads/{file_id}_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    responses.append(
        {
            "status": "processing",
            "name": file.filename,
            "file_id": file_id
        }
    )
    bg_task.add_task(count_morphed_usages, f"uploads/{file_id}_{file.filename}", file_id)
    return {
        "status": "processing",
        "name": file.filename,
        "file_id": file_id
    }


@app.get("/public/report/export/{file_id}", name="Скачать файл", tags=["Работа с файлами 📄"])
async def download_file(file_id: str):
    if os.path.exists(f"send-file/Ответ_{file_id}.xlsx") and os.path.getsize(
            f"send-file/Ответ_{file_id}.xlsx") > 0:
        return FileResponse(path=f"send-file/Ответ_{file_id}.xlsx",
                            filename="Ответ.xlsx", media_type="multipart/form-data")
    else:
        raise HTTPException(status_code=404, detail="Неверный id или файл еще не сгенерирован")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
