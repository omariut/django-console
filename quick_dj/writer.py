from abc import ABC, abstractmethod
import os
from django.conf import settings


class PrepareFiles:

    def __init__(self,app_name,write_api_views=False):
        self.app_name=app_name
        self.write_api_views=write_api_views
        self.write_import_line_to_view_file()
        self.write_import_line_to_url_file()

    def write_import_line(self,file_name,import_line):

        with open(file_name,'w') as f:
            f.write(import_line + "\n \n")

    def write_import_line_to_view_file(self):
        file_name=f"{self.app_name}/views.py"
        import_line="from django.views import generic \n"
        import_line+=f"from {self.app_name} import models as {self.app_name}_models \n"
        if self.write_api_views:
            import_line+="from rest_framework import generics \n" + f"from {self.app_name} import serializers\n"
        self.write_import_line(file_name,import_line)


    def write_import_line_to_url_file(self):
        file_name=f"{self.app_name}/urls.py"
        import_line="from django.urls import path" + "\n" + f"from {self.app_name} import views"
        self.write_import_line(file_name,import_line)


class BaseWriter(ABC):
    
    def __init__(self,app_name, model_name,file_name):
        self.model_name = model_name
        self.app_name=app_name
        self.file_name=file_name
    
    @abstractmethod
    def get_object_header(self):
        pass

    @abstractmethod
    def get_object_body(self):
        pass

    def get_object_string(self):
        return self.get_object_header() + self.get_object_body() + '\n'
    
    def write_object(self):
        with open(self.file_name,'a') as f:
            f.write(self.get_object_string()+ "\n\n")


class BaseViewWriter(BaseWriter):

    def __init__(self,app_name, model_name):
        file_name=f"{app_name}/views.py"
        return super().__init__(app_name, model_name,file_name)

    @abstractmethod
    def get_object_header(self):
        pass

    @abstractmethod
    def get_object_body(self):
        pass


class BaseAPIViewWriter(BaseViewWriter):


    def get_object_body(self):
        return f"\tserializer_class = serializers.{self.model_name}Serializer\n\tqueryset = {self.model_name}.objects.filter().select_related().prefetch_related()\n\t#authentication_classes=()"


class ListCreateAPIViewWriter(BaseAPIViewWriter):

    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_object_header(self):
        return f"class {self.model_name}ListCreateAPIView(generics.ListCreateAPIView):\n"

class RetrieveUpdateDestroyAPIViewWriter(BaseAPIViewWriter):

    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_object_header(self):
        return f"class {self.model_name}RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):\n"


class BaseURLWriter(BaseWriter):
    def __init__(self,app_name, model_name,):
        file_name=f"{app_name}/urls.py"
        return super().__init__(app_name, model_name,file_name)


    def get_object_header(self):
        pass


    def get_object_body(self):
        pass
    
    @abstractmethod
    def get_url_string(self):
        pass

    def get_object_string(self):
        url_string=self.get_url_string()
        return "urlpatterns = [\n" + url_string + "]\n"

class APIUrlWriter(BaseURLWriter):


    def get_url_string(self):
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}s/', views.{self.model_name}ListCreateAPIView.as_view(), name='{self.model_name.lower()}_list_create'),\n"
        url_string += f"    path('{self.model_name.lower()}s/<int:pk>', views.{self.model_name}RetrieveUpdateDestroyAPIView.as_view(), name='{self.model_name.lower()}_retrieve_update_destroy'),\n"
        return url_string




class APIViewURLWriter:

    def __init__(self,app_name, model_name):
        self.model_name = model_name
        self.app_name=app_name
    
    def write_api_views_and_urls(self):
        app_name=self.app_name
        model_name=self.model_name
        ListCreateAPIViewWriter(app_name, model_name).write_object()
        RetrieveUpdateDestroyAPIViewWriter(app_name, model_name).write_object()
        APIUrlWriter(app_name, model_name).write_object()




class CreateViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}CreateView(generic.CreateView):\n"

    def get_object_body(self):
        return f"\tmodel = {self.app_name}_models.{self.model_name}\n\tfields = '__all__'\n\tsuccess_url= ' \ \' "


class ListViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}ListView(generic.ListView):\n"

    def get_object_body(self):
        return f"\tmodel =  {self.app_name}_models.{self.model_name}\n\tpaginate_by = 10 \n"


class DetailViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}DetailView(generic.DetailView):\n"

    def get_object_body(self):
        return f"\tmodel =  {self.app_name}_models.{self.model_name} \n"

class URLWriter(BaseURLWriter):

    def get_url_string(self):
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}/list/', views.{self.model_name}ListView.as_view(), name='{self.model_name.lower()}_list'),\n"
        url_string += f"    path('{self.model_name.lower()}/create/', views.{self.model_name}CreateView.as_view(), name='{self.model_name.lower()}_create'),\n"
        url_string += f"    path('{self.model_name.lower()}/<int:pk>/', views.{self.model_name}DetailView.as_view(), name='{self.model_name.lower()}_detail'),\n"
        return url_string

class ViewURLWriter:

    def __init__(self,app_name, model_name):
        self.model_name = model_name
        self.app_name=app_name
    
    def write_views_and_urls(self):
        app_name=self.app_name
        model_name=self.model_name
        ListViewWriter(app_name, model_name).write_object()
        CreateViewWriter(app_name, model_name).write_object()
        DetailViewWriter(app_name, model_name).write_object()
        URLWriter(app_name, model_name).write_object()





class ModelWriter(BaseWriter):

    def __init__(self, app_name, model_name, fields,meta_options):
        self.fields=fields
        self.meta_options=meta_options
        file_name = f"{app_name}/models.py"
        super().__init__(app_name, model_name, file_name)
    
    def get_field_options(self,options):
        return ", ".join([f"{opt['name']}={opt['value']}" for opt in options])
    
    def get_field_string(self,field_name,field_type,options):
        field_options=self.get_field_options(options)
        return f"{field_name} = models.{field_type}({field_options})"

        
    def get_object_header(self):
        return f"class {self.model_name}(models.Model):\n"

    def get_object_body(self):
        model_body="\n"
        for field_name,values in self.fields.items():
           
            field_type=values["type"]
            options=values["options"]
            field_string=self.get_field_string(field_name, field_type, options)
            model_body+= "\t" + field_string + "\n"
        
        if self.meta_options:
            meta_body="\n\tclass Meta: \n"
            for key,value in self.meta_options.items():
                meta_body+=f"\t\t{key}={value}\n"

            return model_body + meta_body
        else:
            return model_body


class NewAppsWriter(BaseWriter):
    def __init__(self,app_names):
        self.app_names=app_names
        settings_file=settings.ROOT_URLCONF.split(".")[0] + "/settings.py"
        self.file_name=settings_file

    def get_object_header(self):
        return "INSTALLED_APPS+=["

    def get_object_body(self):
        new_apps = "\n"
        for name in self.app_names:
            new_apps+=f"\t \"{name}\", \n"
        return new_apps + "\n]\n"

class IncludeAppUrlToRootUrlWriter(BaseWriter):

    def __init__(self,app_names):
        self.app_names=app_names
        self.file_name=settings.ROOT_URLCONF.split(".")[0] + "/urls.py"
    
    def get_object_header(self):
        return "urlpatterns+=[\n\t"

    def get_include_app_url(self,app_name):
        return f"path('{app_name}/', include('{app_name}.urls')), \n\t"


    def get_object_body(self):
        app_urls=""
        for name in self.app_names:
            app_urls+=self.get_include_app_url(name)
        
        return app_urls + "\n ]\n"


