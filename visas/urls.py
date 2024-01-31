from django.urls import path

from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/visas/search/', search_visa),  # GET
    path('api/visas/<int:visa_id>/', get_visa_by_id),  # GET
    path('api/visas/<int:visa_id>/update/', update_visa),  # PUT
    path('api/visas/<int:visa_id>/delete/', delete_visa),  # DELETE
    path('api/visas/create/', create_visa),  # POST
    path('api/visas/<int:visa_id>/add_to_order/', add_visa_to_order),  # POST
    path('api/visas/<int:visa_id>/image/', get_visa_image),  # GET
    path('api/visas/<int:visa_id>/update_image/', update_visa_image),  # PUT

    # Набор методов для заявок
    path('api/orders/', get_orders),  # GET
    path('api/orders/<int:order_id>/', get_order_by_id),  # GET
    path('api/orders/<int:order_id>/update/', update_order),  # PUT
    path('api/orders/<int:order_id>/update_status_user/', update_status_user),  # PUT
    path('api/orders/<int:order_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/orders/<int:order_id>/delete/', delete_order),  # DELETE
    path('api/orders/<int:order_id>/delete_visa/<int:visa_id>/', delete_visa_from_order),  # DELETE
]