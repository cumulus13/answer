from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import ast

from pydebugger.debug import debug

def index(request):
	debug(request = request)
	debug(request_items = dir(request))
	debug(request_headers = request.headers)
	debug(request_META = request.META.items())
	return HttpResponse("THIS IS ROUTER !")

def get_data(request):
	data = {}
	with open('/projects/answer/data.txt', 'r') as df:
		data = ast.literal_eval(df.read())
	return JsonResponse({"data": data,})