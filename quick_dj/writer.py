from abc import ABC, abstractmethod
import os


class PrepareFiles:

    def __init__(self,app_name):
        self.app_name=app_name
        self.write_import_line_to_view_file()
        self.write_import_line_to_url_file()

    def write_import_line(self,file_name,import_line):

        with open(file_name,'w') as f:
            f.write(import_line + "\n \n")

    def write_import_line_to_view_file(self):
        file_name=f"{self.app_name}/views.py"
        import_line="from rest_framework import generics \n" + f"from {self.app_name} import serializers\n" + "from django.views import generic"
        self.write_import_line(file_name,import_line)


    def write_import_line_to_url_file(self):
        file_name=f"{self.app_name}/urls.py"
        import_line="from django.urls import path"
        self.write_import_line(file_name,import_line)

        with open(file_name,'a') as f:
            f.write("urlpatterns=[\n]\n")


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
        return "urlpatterns+= [\n" + url_string + "]\n"

class APIUrlWriter(BaseURLWriter):


    def get_url_string(self):
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}s/', {self.model_name}ListCreateAPIView.as_view(), name='{self.model_name.lower()}_list_create'),\n"
        url_string += f"    path('{self.model_name.lower()}s/<int:pk>', {self.model_name}RetrieveUpdateDestroyAPIView.as_view(), name='{self.model_name.lower()}_retrieve_update_destroy'),\n"
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
        return f"\tmodel = {self.model_name}\n\tfields = '__all__'\n\tsuccess_url= ' \ \' "


class ListViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}ListView(generic.ListView):\n"

    def get_object_body(self):
        return f"\tmodel = {self.model_name}\n\tpaginate_by = 10 \n"


class DetailViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}DetailView(generic.DetailView):\n"

    def get_object_body(self):
        return f"\tmodel = {self.model_name} \n"

class URLWriter(BaseURLWriter):

    def get_url_string(self):
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}/list/', {self.model_name}ListView.as_view(), name='{self.model_name.lower()}_list'),\n"
        url_string += f"    path('{self.model_name.lower()}/create/', {self.model_name}CreateView.as_view(), name='{self.model_name.lower()}_create'),\n"
        url_string += f"    path('{self.model_name.lower()}/<int:pk>/', {self.model_name}DetailView.as_view(), name='{self.model_name.lower()}_detail'),\n"
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
        