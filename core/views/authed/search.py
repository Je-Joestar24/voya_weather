from django.shortcuts import render

# Create your views here.

def search_places_view(request):

    return render(request, 'authed/searchplaces/index.html', {
        'status': 'info',
        'message': 'SEARCH PLACES'
        })