from codeless_django.writers.base import BaseBuilder,BaseWriter,BaseURLWriter #BaseViewWriter,BaseURLWriter


class BaseAPIViewBuilder(BaseBuilder):
    def __init__(self,app_name,model_name):
            self.model_name=model_name
            self.app_name=app_name

    def get_object_body(self):
        return f"\tserializer_class = serializers.{self.model_name}Serializer\n\tqueryset = {self.app_name}_models.{self.model_name}.objects.filter().select_related().prefetch_related()\n\t#authentication_classes=()"


class ListCreateAPIViewBuilder(BaseAPIViewBuilder):

    def get_object_header(self):
        return f"class {self.model_name}ListCreateAPIView(generics.ListCreateAPIView):\n"

class RetrieveUpdateDestroyAPIViewBuilder(BaseAPIViewBuilder):

    def get_object_header(self):
        return f"class {self.model_name}RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):\n"

class APIViewWriter(BaseWriter):
    def __init__(self, app_name,models):
        self.models = models
        self.app_name=app_name
        file_name = f"{app_name}/views.py"
        super().__init__(file_name)
    
    def get_full_string(self):
        app_name=self.app_name
        full_string = ""
        for model_name in self.models.keys():
            full_string+=ListCreateAPIViewBuilder(app_name, model_name).get_object_string()
            full_string+=RetrieveUpdateDestroyAPIViewBuilder(app_name, model_name).get_object_string()
        return full_string




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