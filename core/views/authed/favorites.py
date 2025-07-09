from django.shortcuts import render

# Create your views here.

def favorite_places_view(request):

    return render(request, 'authed/favorites/index.html', {
        'status': 'info',
        'message': 'RECENT VIEWED PLACES'
        })