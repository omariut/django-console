import os
from abc import ABC, abstractmethod
from typing import Dict, List
from auto_api.auto_api_view import APIViewBuilder

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


def get_additional_apps_string(app_names):
    additional_apps = "\n"
    for name in app_names:
        additional_apps+=f"\t \"{name}\", \n"
    return additional_apps

def get_file_context(file):
    with open(file,'r') as file:
        data = file.readlines()
    
    return data

def get_line_number_of_text(file,text):
    data=get_file_context(file)
    
    for linenumber,line in enumerate(data):
        if text in line:
            return linenumber
 


def write_additional_apps_string(app_names,file):
    apps_list = get_additional_apps_string(app_names)
    data=get_file_context(file)
    new_installed_app_string = f"INSTALLED_APPS+=[{apps_list}] \n \n"
    last_line_of_installed_app_variable = get_line_number_of_text(file,"MIDDLEWARE")
    data.insert(last_line_of_installed_app_variable,new_installed_app_string)
    data = "".join(data)
    
    with open(file,'w') as file:
        file.write(data)

def get_app_url(app_name):
    return f"path('{app_name}/', include('{app_name}.urls')), \n"

def write_include_app_urls(app_names):
    file = "config/urls.py"
    app_urls=""
    
    for name in app_names:
        app_urls+=get_app_url(name)
    
    new_urls = f"urlpatterns+=[\n{app_urls}\n]"

    with open(file,'a') as file:
        file.write(new_urls)
    


def edit_settings_file(app_names):
    pass



    


def process_project(apps: Dict[str, Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]]) -> None:
    for app_name, value in apps.items():
        start_app(app_name)
        models = value["models"]
        write_models_file(app_name, models)
