from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def favorite_places_view(request):

    return render(request, 'authed/favorites/index.html', {
        'status': 'info',
        'message': 'RECENT VIEWED PLACES'
        })