from django.shortcuts import render
from django.http import JsonResponse
from answer.answer import Check
from answer.forms import CheckForm

try:
	from pydebugger.debug import debug
except:
	def debug(*args, **kwargs):
		print("data:", kwargs.get('data'))

def check(request):
	form = CheckForm()
	result = {'message':'no data'}
	data = request.POST.get('data') or request.GET.get('data')
	debug(data = data, debug = 1)
	message = ''
	if data:
		result = Check.check(data)
		if result:
			message = "True"
		else:
			message = "False"
	# return JsonResponse({'result': result})
	return render(request, 'check.html', {'data':data, 'message':message, 'form': form})