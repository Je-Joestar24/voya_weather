from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def saved_places_view(request):

    return render(request, 'authed/savedplaces/index.html', {
        'status': 'info',
        'message': 'SAVED PLACES'
        })