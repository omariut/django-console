from codeless_django.writers.base import BaseWriter,BaseBuilder

class ModelBuilder(BaseBuilder):

    def __init__(self,model_name, fields,meta_options):
        self.model_name=model_name
        self.fields=fields
        self.meta_options=meta_options

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

    def get_object_string(self):
        return self.get_object_header() + self.get_object_body() + '\n'
class ModelWriter(BaseWriter):

    def __init__(self, app_name,models):
        self.models = models
        file_name = f"{app_name}/models.py"
        super().__init__(file_name)
    
    def get_full_string(self):
        full_string = ""
        for model_name,value in self.models.items():
            fields=value["fields"]
            meta_options=value["meta_options"]
            builder = ModelBuilder(model_name,fields, meta_options)
            full_string+= builder.get_object_string()
        return full_string