# Template Engine
A simple template engine that generates deployable web app skeletons.

## Usage
1. Create a template engine instance: `engine = create_template_engine()`
2. Select a template based on intent: `template = engine.select_template("blog")`
3. Generate code for the selected template: `code = engine.generate_code(template)`
4. Compile and deploy the code: `deployment_url = engine.deploy_code(code)`

## Testing
Run tests using `pytest`: `python -m pytest tests/test_template_engine.py`
