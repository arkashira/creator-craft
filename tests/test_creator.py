import pytest
from creator import Creator, Project

def test_create_project():
    creator = Creator()
    project = creator.create_project("Test Project", "This is a test project")
    assert project.name == "Test Project"
    assert project.description == "This is a test project"

def test_build_project():
    creator = Creator()
    creator.create_project("Test Project", "This is a test project")
    built_project = creator.build_project("Test Project")
    assert built_project["name"] == "Test Project"
    assert built_project["description"] == "This is a test project"
    assert built_project["status"] == "built"

def test_launch_project():
    creator = Creator()
    creator.create_project("Test Project", "This is a test project")
    launched_project = creator.launch_project("Test Project")
    assert launched_project["name"] == "Test Project"
    assert launched_project["description"] == "This is a test project"
    assert launched_project["status"] == "launched"

def test_create_project_edge_case():
    creator = Creator()
    with pytest.raises(ValueError):
        creator.create_project("", "This is a test project")

def test_build_project_edge_case():
    creator = Creator()
    with pytest.raises(ValueError):
        creator.build_project("Non-existent Project")

def test_launch_project_edge_case():
    creator = Creator()
    with pytest.raises(ValueError):
        creator.launch_project("Non-existent Project")
