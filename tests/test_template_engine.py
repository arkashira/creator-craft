import pytest
from src.template_engine import TemplateEngine, Template, create_template_engine

def test_select_template():
    engine = TemplateEngine()
    template = engine.select_template("blog")
    assert template.name == "blog"
    assert template.code == "blog_template"

def test_select_template_edge_case():
    engine = TemplateEngine()
    template = engine.select_template("non-existent")
    assert template is None

def test_generate_code():
    engine = TemplateEngine()
    template = engine.select_template("blog")
    code = engine.generate_code(template)
    assert code == "// blog_template code here"

def test_compile_code():
    engine = TemplateEngine()
    code = engine.generate_code(engine.select_template("blog"))
    assert engine.compile_code(code)

def test_deploy_code():
    engine = TemplateEngine()
    code = engine.generate_code(engine.select_template("blog"))
    deployment_url = engine.deploy_code(code)
    assert deployment_url == "https://example.com/deployed-app"

def test_create_template_engine():
    engine = create_template_engine()
    assert isinstance(engine, TemplateEngine)
