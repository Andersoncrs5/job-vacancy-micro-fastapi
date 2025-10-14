import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'emails')

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True,
)

jinja_env.globals.update({
    'now': datetime.now
})

class TemplateManager:
    def render_html(self, template_name: str, data: dict) -> str:
        try:
            template_file = f"{template_name}.html"
            template = jinja_env.get_template(template_file)
            html_content = template.render(data)

            return html_content

        except FileNotFoundError:
            raise ValueError(f"Template '{template_file}' não encontrado na pasta {TEMPLATE_DIR}.")
        except Exception as e:
            raise RuntimeError(f"Erro ao renderizar template '{template_name}': {e}")