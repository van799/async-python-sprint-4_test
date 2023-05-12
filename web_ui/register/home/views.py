from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from home.forms import DataForm


import requests
import json

class Url:
    origin_url = ''
    short_url = ''
    details_url = ''


@login_required(login_url="/auth/login/")
def index(request):
    url = f"http://127.0.0.1:8001/{request.user}"
    res = requests.get(url)
    add_url_form = DataForm(
        request.POST or None,
        files=request.FILES or None,
    )
    print_json = json.loads(res.content)

    if res.status_code == 200:
        context = {
            "add_url_form": add_url_form,
            "has_error": True,
            "url_list": print_json,
        }
    else:
        context = {
            "add_url_form": add_url_form,
        }

    # add_url_form = DataForm(
    #     request.POST or None,
    #     files=request.FILES or None,
    # )
    # if add_url_form.is_valid():
    #     instance = add_url_form.save(commit=False)
    #     instance.author = request.user
    #     instance.save()
    #     return redirect('homes:index')
    #
    # urls_list = Urls.objects.all().order_by('-pub_date')

    return render(request, "homes/index.html", context)
