from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label='title')

class New_page(forms.Form):
    title = forms.CharField(label='title')
    content = forms.CharField(widget=forms.Textarea)

#<input class="search" type="text" name="q" placeholder="Search Encyclopedia">
def index(request):

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title) is None:
                return render(request, "encyclopedia/search.html", {
                    "title": title, "entries": util.list_entries()
                })
            return render(request, "encyclopedia/wiki.html", {
                "content": util.get_entry(title), "title": title,"form":NewTaskForm()
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": NewTaskForm()

    })

def wiki(request, title):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title) is None:
                return HttpResponse("error")
            return render(request, "encyclopedia/wiki.html", {
                "content": util.get_entry(title), "title": title,"form":NewTaskForm()
            })

    if util.get_entry(title) is None:
        return HttpResponse("error")
    return render(request, "encyclopedia/wiki.html", {
        "content": util.get_entry(title), "title": title, "form": NewTaskForm()
    })
def new_entry(request):
    if request.method == "POST":
        form = New_page(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return render(request, "encyclopedia/wiki.html", {
                    "content": util.get_entry(title), "title": title, "form": NewTaskForm()
                })
            else:
                return HttpResponse("error")
    return render(request, "encyclopedia/new_page.html", {
        "form2": New_page(), "form":NewTaskForm()

    })
def edit(request,title):
    if request.method == "POST":
        form = New_page(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/wiki.html", {
                    "content": util.get_entry(title), "title": title, "form": NewTaskForm()
                })
    data = {'ontent': util.get_entry(title)}
    form2 = New_page(initial=data)
    return render(request,"encyclopedia/edit.html",{
        "title": title, "form2": form2, "form":NewTaskForm()
    })


