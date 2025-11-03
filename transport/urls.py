from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.transport_list, name='transport_list'),
    path('my-requests/', views.my_transport_requests, name='my_transport_requests'),
    path('my-offers/', views.my_transport_offers, name='my_transport_offers'),
    path('create/', views.create_transport_request, name='create_transport_request'),
    path('create-offer/', views.create_transport_offer, name='create_transport_offer'),
    path('request/<int:request_id>/', views.transport_detail, name='transport_detail'),
    path('request/<int:request_id>/match/', views.create_transport_match, name='create_match'),
    path('match/<int:match_id>/accept/', views.accept_transport_match, name='accept_match'),
    path('match/<int:match_id>/complete/', views.complete_transport, name='complete_transport'),
]
