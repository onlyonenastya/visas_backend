from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import date
from bmstu_lab.models import *
from django.db.models import Q
import psycopg2


def GetVises(request):
    keyword = request.GET.get("country")
    vises = Vises.objects.filter(status="enabled")
    if keyword:
        keyword = keyword[0].upper() + keyword[1:]
        vises = Vises.objects.filter(status="enabled").filter(country=keyword)
    return render(
        request,
        "vises.html",
        {"data": {"vises": vises}, "search_query": keyword if keyword else ""},
    )


def GetVise(request, id):
    return render(
        request, "vise.html", {"data": {"vise": Vises.objects.filter(id=id)[0]}}
    )


def delete_vise(request, id):
    conn = psycopg2.connect(
        database="vise_center",
        user="postgres",
        password="4025",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()

    cur.execute("update vises set status='deleted' WHERE id = %s;", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("vises")
