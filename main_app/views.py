import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .models import Show

class ShowCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main_app/show_create.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        review = request.POST.get('review')

        show = Show.objects.create(
            title=title,
            genre=genre,
            description=description,
            review=review,
        )

        return redirect('show_details', tv_id=show.tv_id)

class ShowUpdateView(View):
    def get(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_id')
        show = Show.objects.get(tv_id=tv_id)
        return render(request, 'main_app/show_update.html', {'show': show})

    def post(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_id')
        show = Show.objects.get(tv_id=tv_id)

        show.title = request.POST.get('title')
        show.genre = request.POST.get('genre')
        show.description = request.POST.get('description')
        show.review = request.POST.get('review')
        show.save()

        return redirect('show_details', tv_id=show.tv_id)

class ShowDeleteView(View):
    def get(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_id')
        show = Show.objects.get(tv_id=tv_id)
        return render(request, 'main_app/show_delete.html', {'show': show})

    def post(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_id')
        show = Show.objects.get(tv_id=tv_id)
        show.delete()
        return redirect('home')

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

class ShowListView(ListAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

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

    # show details of a single tv show
def show_details(request, tv_id):
    api_key = '3d62d502968b0ef09de0fdbdfd9d6795'

    # build URL to make the API request
    url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()

    # pass the data to a template to render the TV show details
    context = {'data': data}
    return render(request, 'main_app/show_details.html', context)

def show_form(request):
    form = ShowForm()
    return render(request, 'main_app/show_form.html', {'form': form})
