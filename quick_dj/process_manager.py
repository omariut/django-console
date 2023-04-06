
import os
from django.conf import settings




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

def get_settings_file():
    return settings.ROOT_URLCONF.split(".")[0] + "/settings.py"
 


def write_additional_apps_string(app_names):
    file=get_settings_file()
    apps_list = get_additional_apps_string(app_names)
    data=get_file_context(file)
    new_installed_app_string = f"INSTALLED_APPS+=[{apps_list}] \n \n"
    last_line_of_installed_app_variable = get_line_number_of_text(file,"MIDDLEWARE")
    data.insert(last_line_of_installed_app_variable,new_installed_app_string)
    data = "".join(data)
    
    with open(file,'w') as file:
        file.write(data)
    
def start_app(app_name: str) -> None:
    os.system(f"rm -rf {app_name} && python manage.py startapp {app_name}")


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

from quick_dj.writer import ModelWriter,APIViewURLWriter,ViewURLWriter,NewAppsWriter,IncludeAppUrlToRootUrlWriter,PrepareFiles
def process_project(apps,write_template_views=False,write_api_views=False)-> None:
    app_names=[]
    for app_name, value in apps.items():
        start_app(app_name)
        models = value["models"]
        PrepareFiles(app_name,write_api_views)

        for model_name,value in models.items():
            app_names.append(app_name)
            fields=value["fields"]
            meta_options=value["meta_options"]
            
            ModelWriter(app_name, model_name, fields,meta_options).write_object()

            if write_api_views:
                app_names.append('rest_framework')
                APIViewURLWriter(app_name, model_name).write_api_views_and_urls()
            if write_template_views:
                ViewURLWriter(app_name, model_name).write_views_and_urls()
        
    if write_api_views or write_template_views:
        IncludeAppUrlToRootUrlWriter(app_names).write_object()
    NewAppsWriter(app_names).write_object()



