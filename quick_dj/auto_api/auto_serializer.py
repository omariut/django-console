
import os

def get_serializer_header(model_name):
    return f"class {model_name}Serializer(serializers.ModelSerializer):\n"

def get_serializer_body(model_name):
    return f"\tmodel = {model_name}\n\tfields = '__all__'"

def get_serializer_string(model_name):
    serializer_header=get_serializer_header(model_name)
    serializer_body=get_serializer_body(model_name)
    return serializer_header + serializer_body + "\n"

def write_serializer(model_name,file):
    file="product/serializers.py"
    model_name="Product"
    serializer_string=get_serializer_string(model_name)
    with open(file, 'a') as f:
        f.write(serializer_string)

class ModelSerializerWriter:
    def __init__(self, app_name,model_name):
        self.model_name = model_name
        self.file_name=f"{app_name}/serializers.py"

        if not os.path.exists(self.file_name):
            with open(self.file_name,'a') as f:
                f.write("from rest_framework import serializers \n \n")
    
    def get_header(self):
        return f"class {self.model_name}Serializer(serializers.ModelSerializer):\n"
    
    def get_body(self):
        return f"\tmodel = {self.model_name}\n\tfields = '__all__'"
    
    def get_string(self):
        serializer_header = self.get_header()
        serializer_body = self.get_body()
        return serializer_header + serializer_body + "\n"
    
    def write_serializer(self):
        serializer_string=self.get_string()
        with open(self.file_name, 'a') as f:
            f.write(serializer_string)

    
