from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms

from . import util
import random

class NewTaskForm(forms.Form):
    title = forms.CharField(label='title')

class New_page(forms.Form):
    title = forms.CharField(label='title')
    content = forms.CharField(widget=forms.Textarea)
class EditPage(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


def index(request):

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title) is None:
                list = []
                for entry in util.list_entries():
                    if title in entry:
                        list.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "title": title, "entries": util.list_entries(),"form":NewTaskForm(),
                    "titles": list
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
                if util.get_entry(title) is None:
                    list = []
                    for entry in util.list_entries():
                        if title in entry:
                            list.append(entry)
                    return render(request, "encyclopedia/search.html", {
                        "title": title, "entries": util.list_entries(), "form": NewTaskForm(),
                        "titles": list
                    })
            return render(request, "encyclopedia/wiki.html", {
                "content": util.get_entry(title), "title": title,"form":NewTaskForm()
            })

    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "Error": "The entry not found","form":NewTaskForm()
        })
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
                return render(request, "encyclopedia/error.html", {
                    "Error": "The entry already exists","form":NewTaskForm()
                })
    return render(request, "encyclopedia/new_page.html", {
        "form2": New_page(), "form":NewTaskForm()

    })
def edit(request,title):
    if request.method == "POST":
        form2 = EditPage(request.POST)
        if form2.is_valid():
            content = form2.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('wiki', title)


    data = {'content': util.get_entry(title)}
    form2 = EditPage(initial=data)
    return render(request,"encyclopedia/edit.html",{
        "title": title, "form2": form2, "form":NewTaskForm()
    })
def random_entry(request):
    entries = util.list_entries()
    number = random.randint(0, len(entries) - 1)
    title = entries[number]

    return wiki(request,title)
