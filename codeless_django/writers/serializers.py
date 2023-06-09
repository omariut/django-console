
import os
from codeless_django.writers.base import BaseWriter,BaseBuilder

class ModelSerializerBuilder(BaseBuilder):

    def __init__(self,app_name,model_name):
            self.model_name=model_name
            self.app_name=app_name
    
    def get_object_header(self):
        return f"class {self.model_name}Serializer(serializers.ModelSerializer):\n\n\tclass Meta:\n"
    
    def get_object_body(self):
        return f"\t\tmodel = {self.app_name}_models.{self.model_name}\n\t\tfields = '__all__'"

    
class ModelSerializerWriter(BaseWriter):
    def __init__(self, app_name,models):
        self.app_name=app_name
        self.models=models
        file_name=f"{app_name}/serializers.py"

        if not os.path.exists(file_name):
            with open(file_name,'a') as f:
                f.write("from rest_framework import serializers \n \n")
        super().__init__(file_name)
    
    def get_full_string(self):
        app_name=self.app_name
        full_string = ""
        for model_name in self.models.keys():
            full_string+=ModelSerializerBuilder(app_name, model_name).get_object_string()

        return full_string