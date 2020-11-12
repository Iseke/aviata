from api import views

from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('find/', cache_page(1, cache=None, key_prefix='mysite')(views.FindFlightView.as_view())),
    path('check/', cache_page(1, cache=None, key_prefix='mysite')(views.CheckFlightView.as_view())),
    path('booking/', cache_page(1, cache=None, key_prefix='mysite')(views.ClearView.as_view()))
]