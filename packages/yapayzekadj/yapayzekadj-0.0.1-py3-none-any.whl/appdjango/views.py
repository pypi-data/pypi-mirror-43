from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from .models import Tahmin
from django.template import loader


def index(request):
    # docs_new2 = ["kitaplar", ]
    entires = Tahmin.objects.all()
    # tahminler2 = [""]
    metinler = [""]
    # beklenenm = [""]
    toplam = []
    # for i in entires:
    #     metinler.append(i.metin)
    #     tahminler2.append(i.tahmin)
    #     beklenenm.append(i.beklenen)
    for i in entires:
        toplam.append(i)

    print(type(metinler))
    return render(request, "index.html", {"beklenen": toplam})
