from  codeless_django.writers.base import BaseWriter, BaseViewWriter,BaseURLWriter,BaseBuilder


class BaseViewBuilder(BaseBuilder):
    def __init__(self,app_name,model_name):
        self.model_name=model_name
        self.app_name=app_name


class CreateViewBuilder(BaseViewBuilder):

    def get_object_header(self):
        return f"class {self.model_name}CreateView(generic.CreateView):\n"

    def get_object_body(self):
        return f"\tmodel = {self.app_name}_models.{self.model_name}\n\tfields = '__all__'\n\tsuccess_url= ' \ \' "


class ListViewBuilder(BaseViewBuilder):

    def get_object_header(self):
        return f"class {self.model_name}ListView(generic.ListView):\n"

    def get_object_body(self):
        return f"\tmodel =  {self.app_name}_models.{self.model_name}\n\tpaginate_by = 10 \n"


class DetailViewBuilder(BaseViewBuilder):

    def get_object_header(self):
        return f"class {self.model_name}DetailView(generic.DetailView):\n"

    def get_object_body(self):
        return f"\tmodel =  {self.app_name}_models.{self.model_name} \n"


class UpdateViewBuilder(BaseViewBuilder):

    def get_object_header(self):
        return f"class {self.model_name}UpdateView(generic.UpdateView):\n"

    def get_object_body(self):
        return f"\tmodel =  {self.app_name}_models.{self.model_name} \n"
    

class ViewWriter(BaseWriter):
    def __init__(self, app_name,models):
        self.models = models
        self.app_name=app_name
        file_name = f"{app_name}/views.py"
        super().__init__(file_name)
    
    def get_full_string(self):
        app_name=self.app_name
        full_string = ""
        for model_name in self.models.keys():
            full_string+=ListViewBuilder(app_name, model_name).get_object_string()
            full_string+=DetailViewBuilder(app_name, model_name).get_object_string()
            full_string+=UpdateViewBuilder(app_name, model_name).get_object_string()
            full_string+=CreateViewBuilder(app_name, model_name).get_object_string()

        return full_string




