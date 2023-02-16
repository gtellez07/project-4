from pyexpat.errors import messages
import requests
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.views import View
from main_app.forms import ShowForm
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import serializers
from .models import Show, Series
from .forms import CreateUserForm, LoginUserForm
from pprint import pprint

api_key = '3d62d502968b0ef09de0fdbdfd9d6795'

@csrf_exempt
def register(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)
        return redirect('home')
    else:
        context = {'form': form}
        return render(request, 'register.html', context)

    ###### Original code that was not completing Registration form ######
    # form = CreateUserForm()
    # if form.is_valid():
    #     form.save()
    #     user = form.cleaned_data.get('username')
    #     messages.success(request, 'Account was created for ' + user)
    #     return redirect('login')
            
    # context = {'form': form}
    # return render(request, 'register.html', context)

def signout(request):
    logout(request)
    return redirect('login')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        context = {'form' : form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = LoginUserForm()
        context = {'form' : form}

        user = authenticate(username=username, password=password)
        print("user")
        print(user)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', context)
            

def home(request):
    print("home")
    return render(request, 'home.html')

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
            series = Series.series.get(show_id = show_id)
            series.watched = watched
            series.favorite = favorite
            series.save()
        else:        
            series = Series.series.create(
                show_id = show_id,
                user_id = request.user.id,
                review = 0,
                title=title,
                genre=genre,
                description=description,
                watched = watched,
                favorite = favorite
            )

        return redirect('home')

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

# class ShowList(View):
#     def get(self, request, *args, **kwargs):
#         url = f'https://api.themoviedb.org/3/tv/popular?api_key={api_key}&language=en-US&page=1'
#         response = requests.get(url)
#         data = response.json()
#         print("hello test 🎥 🎬 🍿 🎭")
#         pprint(data)
#         context = {'data': data['results']}
#         return render(request, 'shows_list.html', context)

class ShowList(View):
    def get(self, request, *args, **kwargs):
        url = f'https://api.themoviedb.org/3/tv/popular?api_key={api_key}&language=en-US&page=1'
        response = requests.get(url)
        image_base_url = 'https://image.tmdb.org/t/p/w500'
        data = response.json()
        
        # pprint(data)
        # pprint(context)
        fids = []
        new_data = []
        wids = []
        if request.user.is_authenticated:
            # get all favorite shows
            f = Series.series.filter(user_id=request.user.id, favorite=True)
            ff = f.all()
            for x in ff:
                fids.append(x.show_id)

            # get all watched shows
            w = Series.series.filter(user_id=request.user.id, watched=True)
            ww = w.all()
            for x in ww:
                wids.append(x.show_id)


        print("fids")
        print(fids)
        for item in data['results']:
            if item['id'] in wids:
                is_watched = 1
                print(item["name"])
            else:
                is_watched = 0

            if item['id'] in fids:
                is_fave = 1
                print(item["name"])
            else:
                is_fave = 0

            dd = {'title': item['name'], 'is_fave': is_fave, 'is_watched': is_watched, 'id': item['id'], 'description': item['overview'], 'vote_average': item['vote_average'], 'poster': image_base_url + item['poster_path'], 'date': item['first_air_date']}
            new_data.append(dd)


        context = {'fids': fids, 'data': new_data}
        return render(request, 'shows_list.html', context)







