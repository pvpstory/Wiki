from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label='title')
#<input class="search" type="text" name="q" placeholder="Search Encyclopedia">
def index(request):

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            return render(request, "encyclopedia/wiki.html", {
                "content": util.get_entry(title), "title": title
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": NewTaskForm()

    })

def wiki(request, title):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            return render(request, "encyclopedia/wiki.html", {
                "content": util.get_entry(title), "title": title
            })

    if util.get_entry(title) is None:
        return HttpResponse("error")
    return render(request, "encyclopedia/wiki.html", {
        "content": util.get_entry(title), "title": title, "form": NewTaskForm()
    })


