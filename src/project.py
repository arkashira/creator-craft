import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Project:
    name: str
    creation_date: str
    live_url: str
    status: str

class ProjectManager:
    def __init__(self):
        self.projects = []

    def add_project(self, name: str, live_url: str, status: str = 'Building'):
        project = Project(name, datetime.now().strftime('%Y-%m-%d'), live_url, status)
        self.projects.append(project)

    def rename_project(self, old_name: str, new_name: str):
        for project in self.projects:
            if project.name == old_name:
                project.name = new_name
                return
        raise ValueError('Project not found')

    def duplicate_project(self, name: str):
        for project in self.projects:
            if project.name == name:
                new_project = Project(f'{name} (copy)', datetime.now().strftime('%Y-%m-%d'), project.live_url, project.status)
                self.projects.append(new_project)
                return
        raise ValueError('Project not found')

    def delete_project(self, name: str):
        for project in self.projects:
            if project.name == name:
                self.projects = [p for p in self.projects if p.name != name]
                return
        raise ValueError('Project not found')

    def get_projects(self) -> List[Project]:
        return self.projects

    def update_status(self, name: str, status: str):
        for project in self.projects:
            if project.name == name:
                project.status = status
                return
        raise ValueError('Project not found')
