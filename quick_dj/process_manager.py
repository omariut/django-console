import os
from abc import ABC, abstractmethod
from typing import Dict, List

class ModelBuilder(ABC):
    @abstractmethod
    def create_field(self, field_name: str, field_type: str, options: List[Dict[str, str]]) -> None:
        pass

    @abstractmethod
    def get_model_string(self) -> str:
        pass

class DjangoModelBuilder(ModelBuilder):
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.fields = []

    def create_field(self, field_name: str, field_type: str, options: List[Dict[str, str]]) -> None:
        field_options = ", ".join([f"{opt['name']}={opt['value']}" for opt in options])
        self.fields.append(f"{field_name} = models.{field_type}({field_options})")

    def get_model_string(self) -> str:
        model_header = f"class {self.model_name}(models.Model):\n"
        model_body = "\n".join([f"\t{field}" for field in self.fields])
        return model_header + model_body

class Director:
    def __init__(self, builder: ModelBuilder) -> None:
        self.builder = builder

    def construct_model(self, fields: Dict[str, Dict[str, List[Dict[str, str]]]]) -> None:
        for field_name, value in fields.items():
            field_type = value["type"]
            options = value["options"]
            self.builder.create_field(field_name, field_type, options)

    def get_model(self) -> str:
        return self.builder.get_model_string()

def start_app(app_name: str) -> None:
    os.system(f"rm -rf {app_name} && python manage.py startapp {app_name}")

def write_models_file(app_name: str, models: Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]) -> None:
    for model_name, value in models.items():
        fields = value["fields"]
        django_builder = DjangoModelBuilder(model_name)
        director = Director(django_builder)
        director.construct_model(fields)
        model_body = director.get_model()

        with open(f"{app_name}/models.py", "a") as f:
            f.write(model_body)
            f.write('\n\n')

def process_project(apps: Dict[str, Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]]) -> None:
    for app_name, value in apps.items():
        start_app(app_name)
        models = value["models"]
        write_models_file(app_name, models)
