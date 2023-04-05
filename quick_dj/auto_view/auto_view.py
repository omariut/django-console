from abc import ABC, abstractmethod
# from django.views import generic


class BaseViewWriter(ABC):
    def __init__(self,app_name, model_name):
        self.model_name = model_name
        self.file_name=f"{app_name}/views.py"

        with open(self.file_name,'r') as f:
            data=f.read()

        if "from django.views import generic" not in data:
            with open(self.file_name,'w') as f:
                f.write("from django.views import generic \n \n")

    @abstractmethod
    def get_view_header(self):
        pass

    @abstractmethod
    def get_view_body(self):
        pass

    def get_view_string(self):
        return self.get_view_header() + self.get_view_body() + '\n \n'
    
    def write_view(self):
        with open(self.file_name,'a') as f:
            f.write(self.get_view_string())

class CreateViewWriter(BaseViewWriter):
    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_view_header(self):
        return f"class {self.model_name}CreateView(generic.CreateView):\n"

    def get_view_body(self):
        return f"\tmodel = {self.model_name}\n\tfields = '__all__'\n\tsuccess_url= ' \ \' "


class ListViewWriter(BaseViewWriter):
    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_view_header(self):
        return f"class {self.model_name}ListView(generic.ListView):\n"

    def get_view_body(self):
        return f"\tmodel = {self.model_name}\n\tpaginate_by = 10 \n"


class DetailViewWriter(BaseViewWriter):
    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_view_header(self):
        return f"class {self.model_name}DetailView(generic.DetailView):\n"

    def get_view_body(self):
        return f"\tmodel = {self.model_name} \n"



class UrlWriter:
    def __init__(self,app_name, model_name):
        self.model_name = model_name
        self.file_name=f"{app_name}/urls.py"
        self.import_string="from django.urls import path"

        with open(self.file_name,'r') as f:
            data=f.read()
        if self.import_string not in data:
            with open(self.file_name,'w') as f:
                f.write(self.import_string + "\n \n")

    def write_views_urls(self):
        
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}/list/', {self.model_name}ListView.as_view(), name='{self.model_name.lower()}_list'),\n"
        url_string += f"    path('{self.model_name.lower()}/create/', {self.model_name}CreateView.as_view(), name='{self.model_name.lower()}_create'),\n"
        url_string += f"    path('{self.model_name.lower()}/<int:pk>/', {self.model_name}DetailView.as_view(), name='{self.model_name.lower()}_detail'),\n"
        
        with open(self.file_name, 'a') as f:
            
            f.write("urlpatterns+= [\n")
            f.write(url_string)
            f.write("]\n")


class GenericViewWriter:
    
    def __init__(self,app_name,model_name):
        self.app_name=app_name
        self.model_name=model_name
    
    def write_urls(self):
        url_writer=UrlWriter(app_name, model_name)
        url_writer.write_urls()


    def write_views(self):
        app_name=self.app_name
        model_name=self.model_name
        create_view_writer=CreateViewWriter(app_name, model_name)
        list_view_writer=ListViewWriter(app_name, model_name)
        detail_view_writer=DetailViewWriter(app_name, model_name)
        create_view_writer.write_view()
        list_view_writer.write_view()
        detail_view_writer.write_view()
        url_writer=UrlWriter(app_name, model_name)
        url_writer.write_views_urls()

        
        

    

