import pytest
from project import Project, ProjectManager

def test_add_project():
    manager = ProjectManager()
    manager.add_project('Test Project', 'https://example.com')
    assert len(manager.get_projects()) == 1
    assert manager.get_projects()[0].name == 'Test Project'

def test_rename_project():
    manager = ProjectManager()
    manager.add_project('Test Project', 'https://example.com')
    manager.rename_project('Test Project', 'New Name')
    assert manager.get_projects()[0].name == 'New Name'

def test_duplicate_project():
    manager = ProjectManager()
    manager.add_project('Test Project', 'https://example.com')
    manager.duplicate_project('Test Project')
    assert len(manager.get_projects()) == 2
    assert manager.get_projects()[1].name == 'Test Project (copy)'

def test_delete_project():
    manager = ProjectManager()
    manager.add_project('Test Project', 'https://example.com')
    manager.delete_project('Test Project')
    assert len(manager.get_projects()) == 0

def test_get_projects():
    manager = ProjectManager()
    manager.add_project('Test Project 1', 'https://example1.com')
    manager.add_project('Test Project 2', 'https://example2.com')
    projects = manager.get_projects()
    assert len(projects) == 2
    assert projects[0].name == 'Test Project 1'
    assert projects[1].name == 'Test Project 2'

def test_update_status():
    manager = ProjectManager()
    manager.add_project('Test Project', 'https://example.com')
    manager.update_status('Test Project', 'Live')
    assert manager.get_projects()[0].status == 'Live'

def test_project_not_found():
    manager = ProjectManager()
    with pytest.raises(ValueError):
        manager.rename_project('Non-existent Project', 'New Name')
    with pytest.raises(ValueError):
        manager.duplicate_project('Non-existent Project')
    with pytest.raises(ValueError):
        manager.delete_project('Non-existent Project')
    with pytest.raises(ValueError):
        manager.update_status('Non-existent Project', 'Live')
