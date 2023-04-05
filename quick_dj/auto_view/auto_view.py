from abc import ABC, abstractmethod


class BaseViewWriter(ABC):
    def __init__(self, model_name):
        self.model_name = model_name

    @abstractmethod
    def get_view_header(self):
        pass

    @abstractmethod
    def get_view_body(self):
        pass

    def get_view_string(self):
        return self.get_view_header() + self.get_view_body() + '\n'


class CreateViewWriter(BaseViewWriter):
    def __init__(self, model_name):
        super().__init__(model_name)

    def get_view_header(self):
        return f"class {self.model_name}CreateView(generic.CreateView):\n"

    def get_view_body(self):
        return f"\tmodel = {self.model_name}\n\tfields = '__all__'\n\tsuccess_url= ' \ \' "


class ListViewWriter(BaseViewWriter):
    def __init__(self, model_name):
        super().__init__(model_name)

    def get_view_header(self):
        return f"class {self.model_name}ListView(generic.ListView):\n"

    def get_view_body(self):
        return f"\tmodel = {self.model_name}\n\tpaginate_by = 10"


class DetailViewWriter(BaseViewWriter):
    def __init__(self, model_name):
        super().__init__(model_name)

    def get_view_header(self):
        return f"class {self.model_name}DetailView(generic.DetailView):\n"

    def get_view_body(self):
        return f"\tmodel = {self.model_name}"


class ViewWriterFactory:
    @staticmethod
    def create_view(view_type, model_name):
        if view_type == 'create':
            return CreateViewWriter(model_name)
        elif view_type == 'list':
            return ListViewWriter(model_name)
        elif view_type == 'detail':
            return DetailViewWriter(model_name)
        else:
            return ListViewWriter(model_name)


class UrlWriter:
    def __init__(self, model_name, file):
        self.model_name = model_name
        self.file = file

    def write_views_urls(self, views):
        import_string = "from django.urls import path\n\n"
        
        url_string = ''
        url_string += f"    path('', {self.model_name}ListView.as_view(), name='{self.model_name.lower()}_list'),\n"
        url_string += f"    path('create/', {self.model_name}CreateView.as_view(), name='{self.model_name.lower()}_create'),\n"
        url_string += f"    path('<int:pk>/', {self.model_name}DetailView.as_view(), name='{self.model_name.lower()}_detail'),\n"
        
        with open(self.file, 'a') as f:
            f.write(import_string)
            f.write("urlpatterns = [\n")
            f.write(url_string)
            f.write("]\n")


def write_views(views,file):
    with open(file, 'a') as f:
        for view in views:
            f.write(view.get_view_string())

def main():
    model_name = 'Product'
    url_file = 'product/urls.py'

    create_view = ViewWriterFactory.create_view('create', model_name)
    list_view = ViewWriterFactory.create_view('list', model_name)
    detail_view = ViewWriterFactory.create_view('detail', model_name)

    views = [list_view, create_view, detail_view]

    writer = UrlWriter(model_name, url_file)
    writer.write_views_urls(views)
    file="product/views.py"
    write_views(views, file)
    

