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
import json

api_key = '3d62d502968b0ef09de0fdbdfd9d6795'

### Registration form for new users to create an account
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

### Sign out function for users to sign out of their account and return to the login page
def signout(request):
    logout(request)
    return redirect('login')



def ajax_post_view(request):
    data_from_post = json.load(request)['post_data'] #Get data from POST request
    #Do something with the data from the POST request
    #If sending data back to the view, create the data dictionary
    data = {
        'my_data':data_to_display,
    }
    return JsonResponse(data)

    
### Login form for users to login to their account
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
            
### Home page for users to view their profile and list of shows
def home(request):
    print("home")
    return render(request, 'home.html')

### I DONT THINK I NEED THIS...???🤔🤔🤔🤔
# def show_create(request):
#     if request.method == 'POST':
#         form = ShowForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('show_list')
#     else:
#         form = ShowForm()
#     return render(request, 'show_create.html', {'form': form})

class ShowCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'show_create.html')

    def post(self, request, *args, **kwargs):
        show_id = request.POST.get('show_id')
        
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        type = request.POST.get('type')
        watched = request.POST.get('watched')
        favorite = request.POST.get('favorite')
        rating = request.POST.get('rating')
        sid = request.POST.get('sid')
        print("rating")
        print(sid)

        if sid == 0:
            # create new record
            obj = Series.series.create(
                show_id = show_id,
                user_id = request.user.id,
                review = 0,
                title=title,
                genre=genre,
                description=description,
                watched=watched,
                favorite=favorite,
            )
        elif sid == None:
            show = Series.series.filter(show_id=show_id, user_id=request.user.id)
            count = show.count()
            if count > 0:
                first = show.first()
                obj = Series.series.filter(id=first.id).update(
                    show_id = show_id,
                    user_id = request.user.id,
                    review = 0,
                    title=title,
                    genre=genre,
                    description=description,
                    watched=watched,
                    favorite=favorite,
                )
            else:
                obj = Series.series.create(
                    show_id = show_id,
                    user_id = request.user.id,
                    review = 0,
                    title=title,
                    genre=genre,
                    description=description,
                    watched=watched,
                    favorite=favorite,
                )
        else:
            # update existing record 
            obj = Series.series.filter(id=sid).update(
                show_id = show_id,
                user_id = request.user.id,
                review = 0,
                title=title,
                genre=genre,
                description=description,
                watched=watched,
                favorite=favorite,
            )

        response = redirect('/')
        return response
 
class ShowDetailView(View):
    def get(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_pk')
        media_type = kwargs.get('media_type')
        url = f'https://api.themoviedb.org/3/{media_type}/{tv_id}?api_key={api_key}&language=en-US&page=1'
        response = requests.get(url)
        image_base_url = 'https://image.tmdb.org/t/p/w500'
        data = response.json()
        print("data")
        pprint(data.get('title'))
       
        show = Series.series.filter(show_id=tv_id, user_id=request.user.id)
        count = show.count()
        
        if count > 0:
            series = show.first()
            watched = series.watched
            favorite = series.favorite
            sid = series.id
        else:
            sid = 0
            watched = False
            favorite = False
        print('favorite')
        print(favorite)
        
        # print("series")
        # print(series.favorite)
        #photo of movie, description, a box for commenting, select for rating, select for watched, select for favorite
        return render(request, 'show_details.html', {'show': data, 'watched': watched, 'favorite': favorite, 'sid': sid})

    def post(self, request, *args, **kwargs):
        tv_id = kwargs.get('tv_pk')
        show = Show.objects.get(id=tv_id)

        show.title = request.POST.get('title')
        show.genre = request.POST.get('genre')
        show.description = request.POST.get('description')
        show.review = request.POST.get('review')
        show.save()

        return redirect('show_details', tv_id=show.tv_id)

### DO I NEED THE GET...???🤔🤔🤔🤔 it is returning to the show_delete.html, and that template doesnt exist
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

class ShowList(View):
    def get(self, request, *args, **kwargs):
        url = f'https://api.themoviedb.org/3/trending/all/week?api_key={api_key}&language=en-US&page=1'
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


        # print("data")
        # pprint(data['results'])
        for item in data['results']:
            if item['id'] in wids:
                is_watched = 1
                # print(item["title"])
            else:
                is_watched = 0

            if item['id'] in fids:
                is_fave = 1
                # print(item["title"])
            else:
                is_fave = 0
                print('item')
                print(item.get('original_title'))
                print("The variable, name is of type:", type(item))


            dd = {'title': item.get('original_title'), 'is_fave': is_fave, 'is_watched': is_watched, 'id': item.get('id'), 'description': item.get('overview'), 'vote_average': item.get('vote_average'), 'poster': image_base_url + item.get('poster_path'), 'date': item.get('release_date'), 'media_type': item.get('media_type')}
            new_data.append(dd)


        context = {'fids': fids, 'data': new_data}
        return render(request, 'shows_list.html', context)







