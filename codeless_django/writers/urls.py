from  codeless_django.writers.base import BaseWriter



class URLWriter(BaseWriter):
    def __init__(self, app_name,models):
        self.models = models
        self.app_name=app_name
        file_name = f"{app_name}/urls.py"
        super().__init__(file_name)
    
    def get_full_string(self):
        initial_string = "urlpatterns += [ \n"
        url_path_strings = ""

        for model_name in self.models.keys():
            url_string = ''
            url_string += f"    path('{model_name.lower()}/list/', views.{model_name}ListView.as_view(), name='{model_name.lower()}_list'),\n"
            url_string += f"    path('{model_name.lower()}/create/', views.{model_name}CreateView.as_view(), name='{model_name.lower()}_create'),\n"
            url_string += f"    path('{model_name.lower()}/<int:pk>/', views.{model_name}DetailView.as_view(), name='{model_name.lower()}_detail'),\n"
            url_path_strings+=url_string
        
        full_string = initial_string + url_path_strings + "\n ] \n\n"
        return full_string


class APIUrlWriter(BaseWriter):
    def __init__(self, app_name,models):
        self.models = models
        self.app_name=app_name
        file_name = f"{app_name}/urls.py"
        super().__init__(file_name)
    
    def get_full_string(self):
        initial_string = "urlpatterns += [ \n"
        url_path_strings = ""

        for model_name in self.models.keys():
            url_string = ''
            url_string += f"    path('{model_name.lower()}s/', views.{model_name}ListCreateAPIView.as_view(), name='{model_name.lower()}_list_create'),\n"
            url_string += f"    path('{model_name.lower()}s/<int:pk>', views.{model_name}RetrieveUpdateDestroyAPIView.as_view(), name='{model_name.lower()}_retrieve_update_destroy'),\n"
            url_path_strings+=url_string
        
        full_string = initial_string + url_path_strings + "\n ] \n\n"
        return full_string


