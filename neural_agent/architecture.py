"""Pydantic models for neural network architecture description."""

from typing import List, Optional
from pydantic import BaseModel

class Layer(BaseModel):
    name: str
    type: str
    params: dict
    inputs: List[str] = []
    outputs: List[str] = []

class Architecture(BaseModel):
    total_layers: int
    layers: List[Layer]
    connections: List[str]
