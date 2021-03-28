from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    wiki_page = util.get_entry(title)

    if (not wiki_page):
        return render(request, "encyclopedia/fail.html", {
          "message": "Not Found",
          "status": 404
        })

    markdowner = Markdown()

    html_wiki_page = markdowner.convert(wiki_page)

    return render(request, "encyclopedia/title.html", {
        "title": title,
        "html_page": html_wiki_page
    })


def search(request):
    search_key = request.POST.get("q", "")
    
    entries = util.list_entries()
    exists = search_key in entries
    
    if exists:
        return title(request, search_key)

    filtered_entries = [entry for entry in entries if not entry.find(search_key) == -1]

    return render(request, "encyclopedia/index.html", {
        "entries": filtered_entries
    })

