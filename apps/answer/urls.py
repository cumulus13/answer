from django.urls import path
from answer.views import check

urlpatterns = [
	path('check/', check),
]