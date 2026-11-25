from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
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

## -- Create new entry
class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def addEntry(request):
    entries = util.list_entries()

    if request.method == "POST":
        form = NewEntry(
            request.POST
        )

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            for e in entries:
                if title.lower() in e.lower():
                    return render(request, "encyclopedia/add.html", {
                        "form": form,
                        "error": f'Title "{title}" already exists.',
                        "title_error": True
                    })
                
            util.save_entry(title, content)

            # return HttpResponseRedirect(reverse(f"encyclopedia:title"))
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia:add.html", {
                "form": form
            })

    return render(
        request, "encyclopedia/add.html", {
            "form": NewEntry()
        }
    )