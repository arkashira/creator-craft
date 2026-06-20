import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Project:
    name: str
    description: str

class Creator:
    def __init__(self):
        self.projects = {}

    def create_project(self, name: str, description: str) -> Project:
        if not name:
            raise ValueError("Project name cannot be empty")
        project = Project(name, description)
        self.projects[name] = project
        return project

    def build_project(self, name: str) -> Dict:
        if name not in self.projects:
            raise ValueError("Project not found")
        project = self.projects[name]
        return {
            "name": project.name,
            "description": project.description,
            "status": "built"
        }

    def launch_project(self, name: str) -> Dict:
        if name not in self.projects:
            raise ValueError("Project not found")
        project = self.projects[name]
        return {
            "name": project.name,
            "description": project.description,
            "status": "launched"
        }
