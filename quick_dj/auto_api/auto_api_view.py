from abc import ABC, abstractmethod


class BaseAPIViewWriter(ABC):
    def __init__(self,app_name, model_name):
        self.model_name = model_name
        self.file_name=f"{app_name}/views.py"
        self.write_import_line()


    @abstractmethod
    def get_view_header(self):
        pass

    def write_import_line(self):
        with open(self.file_name,'r') as f:
            data = f.read()
            if "from rest_framework import generics" not in data:
                with open(self.file_name,'a') as f:
                    f.write("from rest_framework import generics \n \n")

    def get_view_body(self):
        return f"\tserializer_class = {self.model_name}Serializer\n\tqueryset = {self.model_name}.objects.filter().select_related().prefetch_related()\n\t#authentication_classes=()"

    def get_view_string(self):
        return self.get_view_header() + self.get_view_body() + '\n'
    
    def write_view(self):
        with open(self.file_name,'a') as f:
            f.write(self.get_view_string())


class ListCreateAPIViewWriter(BaseAPIViewWriter):
    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_view_header(self):
        return f"class {self.model_name}ListCreateAPIView(generics.ListCreateAPIView):\n"

class RetrieveUpdateDestroyAPIViewWriter(BaseAPIViewWriter):
    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_view_header(self):
        return f"class {self.model_name}RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):\n"


class UrlWriter:
    def __init__(self,app_name, model_name,):
        self.model_name = model_name
        self.file_name=f"{app_name}/{model_name}/urls.py"


    def write_urls(self):
        
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}s/', {self.model_name}ListCreateAPIView.as_view(), name='{self.model_name.lower()}_list_create'),\n"
        url_string += f"    path('{self.model_name.lower()}s/<int:pk>', {self.model_name}RetrieveUpdateDestroyAPIView.as_view(), name='{self.model_name.lower()}_retrieve_update_destroy'),\n"
        
        with open(self.file_name, 'a') as f:
            f.write("urlpatterns+= [\n")
            f.write(url_string)
            f.write("]\n")

class APIViewBuilder:
    
    def __init__(self,app_name,model_name):
        self.app_name=app_name
        self.model_name=model_name
    
    def write_urls(self):
        url_writer=UrlWriter(app_name, model_name)
        url_writer.write_urls()

    def write_views(self):
        list_create_api_view_writer = ListCreateAPIViewWriter(self.app_name,self.model_name)
        list_create_api_view_writer.write_view()
        retrieve_update_destroy_api_view_writer = RetrieveUpdateDestroyAPIViewWriter(self.app_name, self.model_name)
        retrieve_update_destroy_api_view_writer.write_view()
        


    



    

