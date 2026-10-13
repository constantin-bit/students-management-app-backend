from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from lab.processing import Students
from lab import io_utils
from lab import errors
import csv

app = FastAPI(title="Students Lab API")

# НАСТРОЙКА CORS: разрешает React-приложению с любого адреса слать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Единый объект кэша студентов на время работы сервера
tracker = Students()

# Описываем структуры данных, которые присылает React
class PathPayload(BaseModel):
    path: str

class StudentPayload(BaseModel):
    id: str
    name: str
    grades: List[str]

class UpdateMarkPayload(BaseModel):
    id: str
    mark_number: str
    mark: str

class DelMarkPayload(BaseModel):
    id: str
    mark_number: str

class ExportPayload(BaseModel):
    n: str
    path: str


# --- ЭНДПОИНТЫ ---

# Команда 1: Загрузка из CSV файла
@app.post("/api/load")
def load_from_csv(payload: PathPayload):
    try:
        tracker.clear()
        io_utils.pathCSV = payload.path.strip()
        if not os.path.exists(io_utils.pathCSV):
            raise HTTPException(status_code=404, detail=f"Файл {io_utils.pathCSV} не найден")
            
        with open(io_utils.pathCSV, encoding='utf-8') as f:
            reader = csv.reader(f)
            lineNumber = -1
            for row in reader:
                if not row: continue
                lineNumber += 1
                if lineNumber == 0: continue # Пропускаем заголовок
                tracker.addStudent(row)
                
        tracker.state = True
        return {"message": f"Данные загружены. Найдено студентов: {len(tracker.students)}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Команда 2 & 8: Сохранение / Обновление оценок в текущий CSV файл
@app.post("/api/save")
def save_to_csv():
    if not tracker.state:
        raise HTTPException(status_code=400, detail="Прежде чем сохранять данные, загрузите файл")
    io_utils.saveToCSV(tracker)
    return {"message": "Данные успешно сохранены в файл на ноутбуке"}

# Команда 3 & 9: Показ всех студентов с деталями
@app.get("/api/students")
def get_students():
    if not tracker.state:
        return {"state": False, "students": [], "message": "Файл еще не загружен"}
    
    result = []
    for s in tracker.students:
        result.append({
            "id": s.getID(),
            "name": s.getName(),
            "average": round(s.getAverage(), 2),
            "grades": [str(g) if g != -100 else " " for g in s.grades]
        })
    return {"state": True, "students": result}

# Команда 4: Добавление студента
@app.post("/api/students/add")
def add_student(payload: StudentPayload):
    if not tracker.state:
        raise HTTPException(status_code=400, detail="Сначала загрузите файл")
    try:
        raw_data = [payload.id, payload.name] + payload.grades
        tracker.addStudent(raw_data)
        return {"message": "Студент добавлен в кэш"}
    except errors.InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Команда 5: Обновление оценки
@app.put("/api/students/mark")
def update_mark(payload: UpdateMarkPayload):
    try:
        tracker.updateMark([payload.id, payload.mark_number, payload.mark])
        return {"message": "Оценка обновлена"}
    except errors.InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Команда 6: Удаление оценки
@app.delete("/api/students/mark")
def delete_mark(payload: DelMarkPayload):
    try:
        tracker.delMark([payload.id, payload.mark_number])
        return {"message": "Оценка удалена (выставлен пустой маркер)"}
    except errors.InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Команда 7: Удаление студента по ID
@app.delete("/api/students/{student_id}")
def delete_student(student_id: str):
    try:
        tracker.delStudentByID(student_id)
        return {"message": f"Студент с ID {student_id} удален из кэша"}
    except errors.InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Команда 10: Экспорт ТОП-N студентов
@app.post("/api/export")
def export_top(payload: ExportPayload):
    try:
        tracker.sortAVG()
        top_n = tracker.getTopN(payload.n)
        io_utils.exportToCSV(top_n, payload.path.strip())
        return {"message": f"Успешный экспорт ТОП-{payload.n} в файл {payload.path}"}
    except errors.InvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Команды 11, 12, 13: Сортировки
@app.post("/api/sort/{criteria}")
def sort_students(criteria: str):
    if tracker.is_empty():
        raise HTTPException(status_code=400, detail="Кэш пустой")
    if criteria == "avg":
        tracker.sortAVG()
    elif criteria == "name":
        tracker.sortName()
    elif criteria == "id":
        tracker.sortID()
    else:
        raise HTTPException(status_code=400, detail="Неверный критерий сортировки")
    return {"message": f"Данные отсортированы по {criteria}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
