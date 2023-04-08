class PrepareFiles:

    def __init__(self,app_name,write_api_views=False):
        self.app_name=app_name
        self.write_api_views=write_api_views
        self.write_import_line_to_view_file()
        self.write_import_line_to_url_file()
        self.write_import_line_to_serializers_file()

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

    def write_import_line_to_serializers_file(self):
        file_name=f"{self.app_name}/serializers.py"
        if self.write_api_views:
            import_line="from rest_framework import serializers  \n"
            import_line+=f"from {self.app_name} import models as {self.app_name}_models \n"
        self.write_import_line(file_name,import_line)

    def write_import_line_to_url_file(self):
        file_name=f"{self.app_name}/urls.py"
        import_line="from django.urls import path" + "\n" + f"from {self.app_name} import views"
        self.write_import_line(file_name,import_line)