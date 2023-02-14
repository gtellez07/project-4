import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View

class ShowList(View):
    def get(self, request, *args, **kwargs):
        url = 'https://api.themoviedb.org/3/tv/popular?api_key=3d62d502968b0ef09de0fdbdfd9d6795&language=en-US&page=1'
        response = requests.get(url)
        data = response.json()
        return JsonResponse(data, safe=False)

def home(request):
    return HttpResponse('<h1>Hello World!</h1>')

def show_details(request, tv_id):
    url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}d&language=en-US'
    api_key = '3d62d502968b0ef09de0fdbdfd9d6795'

    response = requests.get(url.format(tv_id=tv_id, api_key=api_key))
    data = response.json()

    context = {'data': data}
    return render(request, 'main_app/show_details.html', context)
