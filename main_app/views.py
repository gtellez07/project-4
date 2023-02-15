import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from main_app.forms import ShowForm
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import serializers
from .models import Show, Series

def home(request):
    return HttpResponse('Home Page')

def show_create(request):
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_list')
    else:
        form = ShowForm()
    return render(request, 'show_create.html', {'form': form})

class ShowCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'show_create.html')

    def post(self, request, *args, **kwargs):
        show_id = request.POST.get('show_id')
        exists = 0
        
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        type = request.POST.get('type')
        watched = 0
        favorite = 0

        if type == "ab":
            watched = 0
        elif type == "rb":
            watched = 1
        elif type == "af":
            favorite = 1
        elif type == "rf":
            favorite = 0
        else:
            watched = 0
            favorite = 0

        if exists:
            series = Series.objects.get(show_id = show_id)
            series.watched = watched
            series.favorite = favorite
            series.save()
        else:        
            series = Series.objects.create(
                show_id = show_id,
                user_id = 1,
                review = 0,
                title=title,
                genre=genre,
                description=description,
                watched = watched,
                favorite = favorite
            )

        return redirect('show_details', tv_id=show_id)

class ShowUpdateView(View):
    def get(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_pk')
        show = Show.objects.get(id=tv_id)
        return render(request, 'show_update.html', {'show': show})

    def post(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_pk')
        show = Show.objects.get(id=tv_id)

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

# class ShowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Show
#         fields = '__all__'

# class ShowListView(ListAPIView):
#     queryset = Show.objects.all()
#     serializer_class = ShowSerializer

class ShowList(View):
    def get(self, request, *args, **kwargs):
        url = 'https://api.themoviedb.org/3/tv/popular?api_key=3d62d502968b0ef09de0fdbdfd9d6795&language=en-US&page=1'
        response = requests.get(url)
        data = response.json()
        print("hello test")
        print(data['results'])
        context = {'data': data['results']}
        return render(request, 'shows_list.html', context)

    # def show_details(request, tv_id):
    #     api_key = '3d62d502968b0ef09de0fdbdfd9d6795'
    #     url = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}d&language=en-US'

    #     response = requests.get(url.format(tv_id=tv_id, api_key=api_key))
    #     data = response.json()

    #     context = {'data': data}
    #     return render(request, 'show_details.html', context)

    # def show_form(request):
    #     form = ShowForm()
    #     return render(request, 'show_form.html', {'form': form})
