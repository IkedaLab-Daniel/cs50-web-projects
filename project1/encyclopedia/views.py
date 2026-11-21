from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


def index(request):
    query = request.GET.get("q")
    entries = util.list_entries()

    if query:
        entry = util.get_entry(query)

        if entry:
            return HttpResponseRedirect(f"wiki/{query}")

        else:
            match = []
            for e in entries:
                if query.lower() in e.lower():
                    match.append(e)

            return render(request, "encyclopedia/index.html", {
                        "entries": match,
                        "query": query
                    })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

def title(request, title):
    return render(request, "encyclopedia/wiki-entry.html", {
        "entry": util.get_entry(title),
        "title": title
    })

