from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def search_places_view(request):

    return render(request, 'authed/searchplaces/index.html', {
        'status': 'info',
        'message': 'SEARCH PLACES'
        })