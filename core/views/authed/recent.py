from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def recents_view(request):

    return render(request, 'authed/recentplaces/index.html', {
        'status': 'info',
        'message': 'RECENT VIEWED PLACES'
        })