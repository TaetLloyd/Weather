from fastapi import FastAPI, HTTPException, status
from schemas.index import WeatherData,TodoItem
from typing import List, Optional
import json
import os

app = FastAPI()

# Weather data storage
weather_data = []

# Todo item storage
todos = []

# Load data from files (if available)
if os.path.exists("weather_data.json"):
    with open("weather_data.json", "r") as f:
        weather_data = [WeatherData(**data) for data in json.load(f)]

if os.path.exists("todos.json"):
    with open("todos.json", "r") as f:
        todos = [TodoItem(**todo) for todo in json.load(f)]

# Save data to files
def save_data():
    with open("weather_data.json", "w") as f:
        json.dump([data.dict() for data in weather_data], f)
    with open("todos.json", "w") as f:
        json.dump([todo.dict() for todo in todos], f)

# Get weather data for a city
@app.get("/weather/{city}", response_model=WeatherData)
def get_weather(city: str):
    for data in weather_data:
        if data.city.lower() == city.lower():
            return data
    raise HTTPException(status_code=404, detail=f"Weather data for {city} not found")

# Get all weather data
@app.get("/weather", response_model=List[WeatherData])
def get_all_weather():
    return weather_data

# Create new weather data
@app.post("/weather", response_model=WeatherData, status_code=status.HTTP_201_CREATED)
def create_weather(weather_data_in: WeatherData):
    for data in weather_data:
        if data.city.lower() == weather_data_in.city.lower():
            raise HTTPException(status_code=400, detail=f"Weather data for {weather_data_in.city} already exists")
    weather_data.append(weather_data_in)
    save_data()
    return weather_data_in

# Get all todo items
@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return todos

# Create a new todo item
@app.post("/todos", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoItem):
    todo.id = len(todos) + 1
    todos.append(todo)
    save_data()
    return todo

# Update a todo item
@app.put("/todos/{id}", response_model=TodoItem)
def update_todo(id: int, todo: TodoItem):
    for i, t in enumerate(todos):
        if t.id == id:
            todo.id = id
            todo.created_at = t.created_at
            todos[i] = todo
            save_data()
            return todo
    raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")

# Delete a todo item
@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):
    for i, t in enumerate(todos):
        if t.id == id:
            del todos[i]
            save_data()
            return
    raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


