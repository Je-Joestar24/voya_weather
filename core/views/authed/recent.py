from django.shortcuts import render

# Create your views here.

def recents_view(request):

    return render(request, 'authed/recentplaces/index.html', {
        'status': 'info',
        'message': 'RECENT VIEWED PLACES'
        })