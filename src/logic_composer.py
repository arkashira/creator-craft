import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DataModel:
    name: str
    fields: List[str]

@dataclass
class Node:
    id: int
    type: str
    data_model_name: str
    condition: str = None
    next_node: int = None

class LogicComposer:
    def __init__(self):
        self.data_models = {}
        self.nodes = {}
        self.api_endpoints = {}

    def create_data_model(self, name: str, fields: List[str]):
        self.data_models[name] = DataModel(name, fields)

    def create_node(self, id: int, type: str, data_model_name: str, condition: str = None, next_node: int = None):
        if data_model_name not in self.data_models:
            raise ValueError(f"Data model '{data_model_name}' not found")
        self.nodes[id] = Node(id, type, data_model_name, condition, next_node)

    def add_conditional_branching(self, node_id: int, condition: str, next_node: int):
        node = self.nodes.get(node_id)
        if node is None:
            raise ValueError(f"Node '{node_id}' not found")
        node.condition = condition
        node.next_node = next_node

    def generate_api_endpoints(self):
        for node in self.nodes.values():
            endpoint = f"/api/{node.id}"
            self.api_endpoints[endpoint] = node

    def validate_schema(self):
        for node in self.nodes.values():
            if node.data_model_name not in self.data_models:
                raise ValueError(f"Node '{node.id}' has no data model")
            if node.condition is not None and node.next_node is None:
                raise ValueError(f"Node '{node.id}' has a condition but no next node")

    def save(self):
        data = {
            "data_models": {name: {"name": model.name, "fields": model.fields} for name, model in self.data_models.items()},
            "nodes": {id: {"id": node.id, "type": node.type, "data_model": node.data_model_name, "condition": node.condition, "next_node": node.next_node} for id, node in self.nodes.items()}
        }
        return json.dumps(data)

    def load(self, data: str):
        data = json.loads(data)
        for name, model in data["data_models"].items():
            self.create_data_model(model["name"], model["fields"])
        for id, node in data["nodes"].items():
            self.create_node(node["id"], node["type"], node["data_model"], node["condition"], node["next_node"])
