from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import BadRequest
from quick_dj.process_manager import process_project
from django.http import HttpResponse
from quick_dj.data_manager import DataManager

data_manager=DataManager()
# Create your views here.
@csrf_exempt
def home(request):
    data=data_manager._load_data()
    for option,value in request.POST.items():
        if value:
            print(value)
        
    return render(request, 'quick_dj/home.html',context=data )

@csrf_exempt
def add_app(request):
    if request.method=="POST":
        app_name = request.POST.get("app_name")
        if app_name:
            data_manager.create_app(app_name.lower())
        return redirect('home')
    else:
        return render(request, 'quick_dj/forms/app_form.html')


@csrf_exempt
def add_model(request,app_name):
    model_name = request.POST.get("model_name")
    data_manager.create_model(app_name, model_name)
    return redirect('home')


@csrf_exempt
def add_field(request,model_name,app_name):
    if request.method=="POST":
        request.POST._mutable=True
        field_name =request.POST.pop('field_name')[0]
        field_type = request.POST.pop('field_class')[0]
        data_manager.create_field(app_name, model_name, field_name, field_type)

        for option_name,option_value in request.POST.items():
            if option_value:
                data_manager.create_option(app_name, model_name, field_name, option_name, option_value)
        return redirect('home')
    else:
        context={}
        context["field_class"]=request.GET.get('field_class',"")
        context["model_name"]=model_name
        context["app_name"]=app_name
        return render(request, 'quick_dj/forms/field_form.html',context=context)




def get_field_options(request):
    field_class=request.GET.get('field_class',"")   
    return render(request, 'quick_dj/forms/field_option.html',context={"field_class":field_class}) 


def delete_app(request,app_name):
    data_manager.delete_app(app_name)
    return redirect('home')

def delete_model(request,app_name,model_name):
    data_manager.delete_model(app_name, model_name)
    return redirect('home')

def delete_field(request,app_name,model_name, field_name):
    data_manager.delete_field(app_name, model_name, field_name)
    return redirect('home')

def create_apps(request):
    data=data_manager._load_data()
    process_project(data["apps"])
    return HttpResponse("Success")