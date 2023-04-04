import json
 
def get_data_from_file(file='data.json'):
    with open(file,'r') as file:
        data=json.load(file)
    
    return data

def write_data_to_file(data,file='data.json'):
    with open(file,'w') as file:
        json.dump(data, file)

def get_new_data_for_app(app_name):
    new_data={
        app_name:{
            "models":{}
        }
       
    }
    return new_data

def get_new_data_for_model(model_name):
    new_data={
        model_name:{
            "fields":{}
        }
       
    }
    return new_data

def get_new_data_for_fields(field_name,field_type):
    new_data={
        field_name:{
            "type":field_type,
            "options":[]
        }
       
    }
    return new_data

def get_new_data_for_options(option_name,value):
    new_data={
        "name":option_name,
        "value":value
    }
    return new_data



def write_data_for_apps(app_name):
    data=get_data_from_file()
    new_data=get_new_data_for_app(app_name)
    data["apps"].update(new_data)
    write_data_to_file(data)

def write_data_for_models(app_name,model_name):
    data=get_data_from_file()
    new_data=get_new_data_for_model(model_name)
    data["apps"][app_name]["models"].update(new_data)
    write_data_to_file(data)

def write_data_for_fields(field_name,field_type,model_name,app_name):
    data=get_data_from_file()
    new_data=get_new_data_for_fields(field_name,field_type)
    data["apps"][app_name]["models"][model_name]["fields"].update(new_data)
    write_data_to_file(data)


def write_data_for_options(option_name,option_value,field_name,model_name,app_name):
    data=get_data_from_file()
    new_data=get_new_data_for_options(option_name, option_value)
    data["apps"][app_name]["models"][model_name]["fields"][field_name]["options"].append(new_data)
    write_data_to_file(data)


def delete_data(*keys):
    data = get_data_from_file()
    sub_data = data
    for key in keys[:-1]:
        sub_data = sub_data[key]
    del sub_data[keys[-1]]
    write_data_to_file(data)



def delete_app(app_name):
    delete_data("apps", app_name)

def delete_model(app_name, model_name):
    delete_data("apps", app_name, "models", model_name)

def delete_field(app_name, model_name, field_name):
    delete_data("apps", app_name, "models", model_name, "fields", field_name)
