from django.conf import settings

class DocumentationWriter:
    def __init__(self):
        self.file_name=settings_file=settings.ROOT_URLCONF.split(".")[0] + "/urls.py"

    def write_documentation_url(self):
        pass