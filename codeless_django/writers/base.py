from abc import ABC, abstractmethod

class BaseBuilder(ABC):

    @abstractmethod
    def get_object_header(self):
        pass

    @abstractmethod
    def get_object_body(self):
        pass

    def get_object_string(self):
        return self.get_object_header() + self.get_object_body() + '\n'
    


class BaseWriter(ABC):
    
    def __init__(self,file_name):
        self.file_name=file_name
    

    
    
    def get_full_string(self):
        pass
    
    def write_object(self):
        with open(self.file_name,'a') as f:
            f.write(self.get_full_string())


class BaseViewWriter(BaseWriter):

    def __init__(self,app_name, model_name):
        file_name=f"{app_name}/views.py"
        return super().__init__(app_name, model_name,file_name)




class BaseURLWriter(BaseWriter):
    def __init__(self,app_name, model_name,):
        file_name=f"{app_name}/urls.py"
        return super().__init__(app_name, model_name,file_name)


    def get_object_header(self):
        pass


    def get_object_body(self):
        pass
    
    @abstractmethod
    def get_url_string(self):
        pass

    def get_object_string(self):
        url_string=self.get_url_string()
        return "urlpatterns = [\n" + url_string + "]\n"