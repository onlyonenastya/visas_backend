from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponseBadRequest,HttpResponseServerError
from .permissions import IsAuthenticated, IsModerator
from .serializers import *
from minio import Minio
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view,parser_classes
import requests
import redis
import uuid

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def get_draft_order(request):
    try:
        access_token = request.COOKIES["access_token"]
        username = session_storage.get(access_token).decode('utf-8')
        user_id = CustomUser.objects.filter(email=username).values_list('id', flat=True).first()

        print(user_id)
        order = Order.objects.filter(status=1,user_id=user_id).first()
        if order is None:
            return None
        return order.pk
    except:
        return None

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def postImageToVisa(request, visa_id):
    if 'file' in request.FILES:
        file = request.FILES['file']
        subscription = Visa.objects.get(pk=visa_id, status=1)
        
        client = Minio(endpoint="localhost:9000",
                       access_key='admin',
                       secret_key='password',
                       secure=False)

        bucket_name = 'images'
        file_name = file.name
        file_path = "http://localhost:9000/images/" + file_name
        
        try:
            client.put_object(bucket_name, file_name, file, length=file.size, content_type=file.content_type)
            print("Файл успешно загружен в Minio.")
            
            serializer = VisaSerializer(instance=subscription, data={'image': file_path}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse('Image uploaded successfully.')
            else:
                return HttpResponseBadRequest('Invalid data.')
        except Exception as e:
            print("Ошибка при загрузке файла в Minio:", str(e))
            return HttpResponseServerError('An error occurred during file upload.')

    return HttpResponseBadRequest('Invalid request.')


@api_view(["GET"])
@permission_classes([AllowAny])
def search_visa(request):
    # access_token = request.COOKIES["access_token"]
    # payload = get_jwt_payload(access_token)
    # user_id = payload["user_id"]
    # print(user_id)

    name = request.GET.get('query', '')
    status = request.GET.get('status', '')
    if status in ['3']:
       visa = Visa.objects.all()
    else:
       visa = Visa.objects.filter(status=1).filter(name__icontains=name)

    serializer = VisaSerializer(visa, many=True)

    data = {
        "visas": serializer.data,
        "draft_order": get_draft_order(request)
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
    print(request.data)
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
    serializer = VisaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    access_token = request.COOKIES["access_token"]
    username = session_storage.get(access_token).decode('utf-8')
    user_id = CustomUser.objects.filter(email=username).values_list('id', flat=True).first()

    if not Visa.objects.filter(pk=visa_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    visa = Visa.objects.get(pk=visa_id)

    order = Order.objects.filter(status=1,user_id=user_id).last()

    if order is None:
        order = Order.objects.create(user_id=user_id)

    order.visas.add(visa)
    order.save()

    visa_serializer = VisaSerializer(order.visas, many=True)
    order_serializer = OrderSerializer(order)
    data = {
        "visa": visa_serializer.data,
        "order": order_serializer.data
    }
    return Response(data)


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

# !!!!!!!!!!!!!!!!!!!!!!!!!!
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_orders(request):
    access_token = request.COOKIES["access_token"]
    username = session_storage.get(access_token).decode('utf-8')
    user_id = CustomUser.objects.filter(email=username).values_list('id', flat=True).first()
    # payload = get_jwt_payload(access_token)
    # user_id = payload["user_id"]
    category = request.GET.get('category',"")
    start_day = request.GET.get('start_day',"")
    end_day = request.GET.get('end_day',"")
    if not start_day:
        start_day="1900-01-01"
    if not end_day:
        end_day="2200-01-01"
    print(start_day,end_day)
    if user_id is not None:
        user = CustomUser.objects.get(id=user_id)
        if user.is_moderator:   
            orders = Order.objects.exclude(status=5).exclude(status=1)
            if category and category != '0':
                orders = orders.filter(status=category)
            if start_day and end_day:
                orders = orders.filter(date_created__range=(start_day, end_day))
        else:
            orders = Order.objects.filter(user_id=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    else:
        return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)


    # orders = Order.objects.all()

    # request_status = request.GET.get("status")
    # if request_status:
    #     orders = orders.filter(status=request_status)

    # serializer = OrderSerializer(orders, many=True)

    # return Response(serializer.data)


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
def update_delivery_date(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    order.save()

    return Response(serializer.data)

def calculate_delivery_date(order_id):
    data = {
        "order_id": order_id,
        # "access_token": settings.REMOTE_WEB_SERVICE_AUTH_TOKEN,
    }

    requests.post("http://localhost:8080/calc_delivery_date/", json=data, timeout=3)

@api_view(["PUT"])
def update_status_user(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    request_status = request.data["status"]
    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if int(request.data["status"]) in [2]:
        calculate_delivery_date(order.pk)
        order.date_of_formation=date.today()

    order.status = request.data["status"]
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)

    if order.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if int(request.data["status"]) in [3]:
        order.date_complete=date.today()
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
@permission_classes([AllowAny])
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


from drf_yasg.utils import swagger_auto_schema

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!11
@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    username = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=username, password=password)

    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = str(uuid.uuid4())

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token,
    }
    session_storage.set(access_token, username)

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token)

    return response

@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = str(uuid.uuid4())

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    session_storage.set(access_token, user.email)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token)

    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def check(request):
    # access_token = get_access_token(request)
    try:
        access_token = request.COOKIES["access_token"]
        username = session_storage.get(access_token).decode('utf-8')
        user_id = CustomUser.objects.filter(email=username).values_list('id', flat=True).first()
        print('aaaaaaaaaaaaaaaaaa',user_id)
    except:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)
    if access_token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if not session_storage.exists(access_token):
        message = {"message": "Token is not valid"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    user_data = session_storage.get(access_token)

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def logout(request):
    access_token = request.COOKIES["access_token"]
    if access_token is None:
        message = {"message": "Token is not found in cookie"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)
    session_storage.delete(access_token)
    response = Response({'message': 'Logged out successfully'})
    response.delete_cookie('access_token')

    return response
