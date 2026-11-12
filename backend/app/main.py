from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="TaskBoard API")


# Pydantic models: describe and validate the data we accept
class TaskCreate(BaseModel):
    title: str
    status: str = "todo"  # todo | doing | done


class Task(TaskCreate):
    id: int


# In-memory "database" for now
tasks: list[Task] = []
next_id = 1


@app.get("/tasks")
def list_tasks():
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate):
    global next_id
    task = Task(id=next_id, **data.model_dump())
    next_id += 1
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskCreate):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = Task(id=task_id, **data.model_dump())
            return tasks[i]
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")