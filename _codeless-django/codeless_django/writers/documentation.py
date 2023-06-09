from django.conf import settings
import os

import codeless_django
root_path =  os.path.abspath(codeless_django.__file__).strip('__init__.py')
file_path=os.path.join(root_path, 'additional_files','root_urls.py')



class DocumentationWriter:


    def __init__(self):
        self.file_name=settings_file=settings.ROOT_URLCONF.split(".")[0] + "/urls.py"

    def write_documentation_url(self):
        os.system(f"cp {file_path} {self.file_name}")