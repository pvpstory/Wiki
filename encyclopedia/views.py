from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def wiki(request, title):
    if util.get_entry(title) is None:
        return HttpResponse("error")
    return render(request, "encyclopedia/wiki.html", {
        "content": util.get_entry(title), "title": title
    })

