from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'api'

urlpatterns = [
    path('realestate', views.get_all, name='get_all'),
    path('most_common', views.get_most_common, name='get_most_common'),
    path('count_props_by_size', views.get_props_by_size, name='get_props_by_size'),
    path('count_props_by_year', views.get_props_by_year, name='get_props_by_year'),
    path('num_of_properties', views.get_number_of_properties,
         name='get_number_of_properties'),
    path('num_of_sell_by_city', views.get_number_of_properties_by_city,
         name='get_number_of_properties_by_city'),
    path('registration_count', views.get_registration,
         name='get_registration'),
    path('sell_rent_ratio', views.get_sell_rent_ratio, name='get_sell_rent_ratio'),
    path('count_props_by_price_category', views.get_props_by_price_category, name='get_props_by_price_category'),
    path('num_of_properties_with_parking', views.get_number_of_properties_with_parking, name='get_number_of_properties_with_parking'),
    path('top30', views.get_top_30, name='get_top_30'),
    path('top100', views.get_top_100, name='get_top_100'),
    path('2020', views.get_2020, name='get_2020'),
    path('top30_rooms_area', views.get_top_30_rooms_area, name='get_top_30_rooms_area'),
    path('linear_regression', views.linear_regression, name='linear_regression'),
    path('knn', views.knn_prediction, name='knn'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
