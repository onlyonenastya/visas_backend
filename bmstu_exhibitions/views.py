from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import date
from bmstu_exhibitions.models import OrdersVises
from bmstu_exhibitions.models import Users
from bmstu_exhibitions.models import Vises
from bmstu_exhibitions.models import Orders
from django.db.models import Q

services = [
    {
        "title": "Туристическая виза",
        "aspect": "Туристам",
        "id": 0,
        "src": "https://w7.pngwing.com/pngs/618/285/png-transparent-passport-canada-travel-visa-eb-5-visa-cartoon-visa-stamped-cartoon-character-logo-cartoons-thumbnail.png",
        "text": "Виза позволит Вам посещение различных уголков мира в целях отдыха, лечения, туризма. ",
        "simp": [
            "Временный въезд на территорию других государств",
            "Европа, Азия, Америка",
            "Помощь в оформлении всех необходимых документов",
            "Консультация с представителями посольств",
            "Советы по наименьшим затратам",
        ],
    },
    {
        "title": "Студанческая виза",
        "aspect": "Студентам",
        "id": 1,
        "src": "https://w7.pngwing.com/pngs/853/267/png-transparent-united-states-department-of-homeland-security-h-1b-visa-travel-visa-united-states-citizenship-and-immigration-services-student-visa-united-states-business-travel-visa-thumbnail.png",
        "text": "Получение студенческой визы — это один из самых важных этапов для студентов, желающих учиться за границей. Независимо от того, куда вы планируете уехать учиться, вы должны иметь студенческую визу, чтобы быть законным студентом в стране пребывания.",
        "simp": [
            "Помощь при прохождении интервью в посольстве",
            "Заполнение заявления",
            "Помощь в определении типа визы, необходимой для обучения",
            "Великобритания, Америка, Германия, Китай",
            "Срок оформления от 2-х до 8-ми недель",
        ],
    },
    {
        "title": "Рабочая виза",
        "aspect": "Сотрудникам компаний",
        "id": 2,
        "src": "https://w7.pngwing.com/pngs/227/811/png-transparent-freelancer-sole-proprietorship-workplace-employment-tax-copywriter-purple-violet-employment-thumbnail.png",
        "text": "Рабочая виза – это официальное разрешение, позволяющее иностранному гражданину работать на территории Российской Федерации (со всеми вытекающими отсюда правами и обязанностями), выдаваемое на определенный период времени.",
        "simp": [
            "Помощь в проверке необходимых сертификатов о знании языка и резюме",
            "Оформление разрешения на работу",
            "Предварительная запись на подачу документов",
        ],
    },
]


def viseList(request):
    return render(
        request,
        "services.html",
        {"data": {"current_date": date.today(), "vises": Vises.objects.all()}},
    )


def GetVise(request, id):
    return render(
        request,
        "service.html",
        {
            "data": {
                "current_date": date.today(),
                "vise": Vises.objects.filter(id=id)[0],
            }
        },
    )


def GetServices(request):
    return render(request, "services.html", {"services": services})


def GetService(request, id):
    for s in services:
        if s["id"] == id:
            return render(request, "service.html", {"s": s})


def GetQuery(request):
    query = request.GET.get("query", "")
    # print("__QUERY__ =", query, type(query))
    new_services = []
    for service in services:
        if query.lower() in service["title"].lower():
            new_services.append(service)

    if len(new_services) > 0:
        return render(request, "services.html", {"services": new_services})
    else:
        return render(request, "services.html", {"services": services})
