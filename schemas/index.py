from pydantic import BaseModel
from typing import List, Optional

# Weather data model
class WeatherData(BaseModel):
    city: str
    country: str
    temperature: float
    humidity: float
    wind_speed: float

# Todo item model
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
