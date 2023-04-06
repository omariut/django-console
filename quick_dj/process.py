import os
import quick_dj.utils as utils
from quick_dj.writer import ModelWriter

def start_app(app_name):
    os.system(f'rm -rf {app_name} && python manage.py startapp {app_name}')

def get_option_string(option):
    name=option["name"]
    value=option["value"]
    return f"{name}={value},"


def get_field_string(field_name,type_,options):

    field_header=f"{field_name} = models.{type_}("
    for option in options:
        field_header+=get_option_string(option)
    return field_header + ") \n \t"
    

def get_model_string(model_name,fields):
    model_header= f"class {model_name}(models.Model): \n \t"
    model_body=""
    for field_name,value in fields.items():
        type_=value["type"]
        options=value["options"]
        model_body+=get_field_string(field_name,type_,options)
    
    return model_header + model_body + "\n \n"


def write_models_file(app_name,models):
    for model_name,value in models.items():
        fields=value["fields"]
        model_body = get_model_string(model_name,fields)
        with open(f"{app_name}/models.py", 'a') as f:
            f.write(model_body)


def process_project(apps):

    for app_name,value in apps.items():
        start_app(app_name)
        models=value["models"]
        for model_name,value in models:
            fields=value["fields"]
            ModelWriter(app_name, model_name, fields).write_object()
        
        
        
        







