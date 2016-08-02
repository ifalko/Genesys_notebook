from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .forms import RecordForm
from .models import RecordNotebook
from datetime import datetime

from django.db.models import Q

# Create your views here.

#*******************************************************************************
def add_record(request):
    if not request.user.is_authenticated():
        return redirect("loginsys:login")

    form = RecordForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            instance        = form.save(commit=False)
            date_birthday   = instance.birthday
            if date_birthday is not None: #Check: The user was not born yet
                birthday    = datetime(date_birthday.year, date_birthday.month, date_birthday.day)
                if birthday > datetime.today():
                    context = {
                        "error"     : "Error: The user was not born yet",
                        "title"     : "Create",
                        "input1"    : "New contact",
                        "input2"    : "Create a new contact",
                        "form"      : form,
                    }
                    return render(request, "record_form.html", context)
            
            instance.owner  = request.user
            instance.save()
            return redirect("content:list_record")

    context = {
        "title"     : "Create",
        "input1"    : "New contact",
        "input2"    : "Create a new contact",
        "form"      : form,
    }
    return render(request, "record_form.html", context)

#*******************************************************************************

def list_record(request):
    if not request.user.is_authenticated():
        return redirect("loginsys:login")

    queryset_list = queryset_list = RecordNotebook.objects.filter(owner=request.user)
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                                            Q(full_name__icontains=query)|
                                            Q(phone_number__icontains=query)|
                                            Q(birthday__icontains=query)
                                            ).distinct()
    
    today = datetime.now().date()
    queryset_birthday = RecordNotebook.objects.filter(owner=request.user, birthday__day=today.day, birthday__month=today.month)
    context = {
        "title"             : "Contacts",
        "object_list"       : queryset_list,
        "queryset_birthday" : queryset_birthday,
    }
    return render(request, "list_record.html", context)

#*******************************************************************************

def update_record(request, id=None):
    if not request.user.is_authenticated():
        return redirect("loginsys:login")#redirect to login

    instance    = get_object_or_404(RecordNotebook, id=id)
    form        = RecordForm(request.POST or None, instance=instance)

    if instance.owner == request.user:
        if form.is_valid():
            instance        = form.save(commit=False)
            date_birthday   = instance.birthday
            if date_birthday is not None:
                birthday    = datetime(date_birthday.year, date_birthday.month, date_birthday.day)
                if birthday > datetime.today():
                    context = {
                        "error"     : "Error: The user was not born yet",
                        "title"     : "Edit",
                        "input1"    : "Edit",
                        "input2"    : "Update contact",
                        "form"      : form,
                    }
                    return render(request, "record_form.html", context)

            instance.save()    
            return redirect("content:list_record")
        context = {
            "title"     : "Update",
            "input1"    : "Update the contact",
            "input2"    : "Edit contact",
            "form"      : form,
        }
        return render(request, "record_form.html", context)
    else:
        return Http404

#*******************************************************************************

def delete_record(request, id=None):
    if not request.user.is_authenticated():
        return redirect("loginsys:login")#redirect to login

    instance    = get_object_or_404(RecordNotebook, id=id)
    if instance.owner == request.user:
        instance.delete()
        return redirect("content:list_record")
    else:
        return Http404

#*******************************************************************************