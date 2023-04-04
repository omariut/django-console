
GENERIC_VIEW_STRING = {
    "create":"CreateView",
    "update":"UpdateView",
    "delete":"DeleteView",
    "list":"ListView",
    "detail":"DetailView"
}


def get_generic_view_string(crud_type):
    return GENERIC_VIEW_STRING.get(crud_type, "ListView")





def get_class_view_string(model,crud_type):
    generic_view_string=get_generic_view_string(crud_type)
    view_header = f"class {self.model_name}({generic_view_string}):\n"
    view_body = "\n".join([f"\t{field}" for field in self.fields])



def write_view_files(model,file):
    with open(file, "a") as f:
        f.write(model_body)
        f.write('\n\n')