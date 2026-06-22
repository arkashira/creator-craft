import pytest
from logic_composer import LogicComposer, DataModel, Node

def test_create_data_model():
    composer = LogicComposer()
    composer.create_data_model("user", ["name", "email"])
    assert composer.data_models["user"].name == "user"
    assert composer.data_models["user"].fields == ["name", "email"]

def test_create_node():
    composer = LogicComposer()
    composer.create_data_model("user", ["name", "email"])
    composer.create_node(1, "create", "user")
    assert composer.nodes[1].id == 1
    assert composer.nodes[1].type == "create"
    assert composer.nodes[1].data_model_name == "user"

def test_add_conditional_branching():
    composer = LogicComposer()
    composer.create_data_model("user", ["name", "email"])
    composer.create_node(1, "create", "user")
    composer.add_conditional_branching(1, "age > 18", 2)
    assert composer.nodes[1].condition == "age > 18"
    assert composer.nodes[1].next_node == 2

def test_generate_api_endpoints():
    composer = LogicComposer()
    composer.create_data_model("user", ["name", "email"])
    composer.create_node(1, "create", "user")
    composer.generate_api_endpoints()
    assert "/api/1" in composer.api_endpoints

def test_validate_schema():
    composer = LogicComposer()
    composer.create_data_model("user", ["name", "email"])
    composer.create_node(1, "create", "user")
    composer.validate_schema()
    # should not raise an error

def test_validate_schema_error():
    composer = LogicComposer()
    with pytest.raises(ValueError):
        composer.create_node(1, "create", "user")

def test_save_and_load():
    composer = LogicComposer()
    composer.create_data_model("user", ["name", "email"])
    composer.create_node(1, "create", "user")
    data = composer.save()
    new_composer = LogicComposer()
    new_composer.load(data)
    assert new_composer.data_models["user"].name == "user"
    assert new_composer.data_models["user"].fields == ["name", "email"]
    assert new_composer.nodes[1].id == 1
    assert new_composer.nodes[1].type == "create"
    assert new_composer.nodes[1].data_model_name == "user"
