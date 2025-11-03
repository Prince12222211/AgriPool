from django.urls import path
from . import views

app_name = 'fertilizer'

urlpatterns = [
    path('', views.land_parcel_list, name='land_parcel_list'),
    path('create/', views.create_land_parcel, name='create_land_parcel'),
    path('<int:parcel_id>/', views.land_parcel_detail, name='land_parcel_detail'),
    path('<int:parcel_id>/recommendations/', views.crop_recommendations, name='crop_recommendations'),
    path('<int:parcel_id>/plan/create/', views.create_fertilizer_plan, name='create_fertilizer_plan'),
    path('plan/<int:plan_id>/', views.fertilizer_plan_detail, name='fertilizer_plan_detail'),
]
