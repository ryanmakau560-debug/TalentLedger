from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_postman(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Success! Django is talking to Postman."})

from django.shortcuts import render

def home(request):

    return render(request, 'pages/home.html')