from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *


def get_draft_order():
    order = Order.objects.filter(status=1).first()

    if order is None:
        return None

    return order.pk


@api_view(["GET"])
def search_visa(request):
    name = request.GET.get('query', '')

    visa = Visa.objects.filter(status=1).filter(name__icontains=name)

    serializer = VisaSerializer(visa, many=True)

    data = {
        "visas": serializer.data,
        "draft_order": get_draft_order()
    }

    return Response(data)


@api_view(['GET'])
def get_visa_by_id(request, visa_id):
    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    visa = Visa.objects.get(pk=visa_id)

    serializer = VisaSerializer(visa, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_visa(request, visa_id):
    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    visa = Visa.objects.get(pk=visa_id)
    serializer = VisaSerializer(visa, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_visa(request):
    Visa.objects.create()

    visas = Visa.objects.all()
    serializer = VisaSerializer(visas, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_visa(request, visa_id):
    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    visa = Visa.objects.get(pk=visa_id)
    visa.status = 2
    visa.save()

    visas = Visa.objects.filter(status=1)
    serializer = VisaSerializer(visas, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_visa_to_order(request, visa_id):
    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    visa = Visa.objects.get(pk=visa_id)

    order = Order.objects.filter(status=1).last()

    if order is None:
        order = Order.objects.create()

    order.visas.add(visa)
    order.save()

    serializer = VisaSerializer(order.visas, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_visa_image(request, visa_id):
    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Visa.objects.get(pk=visa_id)

    return HttpResponse(service.image, content_type="image/png")


@api_view(["PUT"])
def update_visa_image(request, visa_id):
    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    visa = Visa.objects.get(pk=visa_id)

    serializer = VisaSerializer(visa, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return HttpResponse(visa.image, content_type="image/png", status=status.HTTP_200_OK)


@api_view(["GET"])
def get_orders(request):
    orders = Order.objects.all()

    request_status = request.GET.get("status")
    if request_status:
        orders = orders.filter(status=request_status)

    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_order_by_id(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    order.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 2
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)

    if order.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = request_status
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    order.status = 5
    order.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_visa_from_order(request, order_id, visa_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    order.visas.remove(Visa.objects.get(pk=visa_id))
    order.save()

    serializer = VisaSerializer(order.visas, many=True)

    return Response(serializer.data)

