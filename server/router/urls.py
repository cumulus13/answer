from django.urls import path, include
from router import views as router

urlpatterns = [
	path('', router.index),
	path('data/', router.get_data)
]