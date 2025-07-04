from django.shortcuts import render

# Create your views here.

def saved_places_view(request):

    return render(request, 'authed/savedplaces/index.html', {
        'status': 'info',
        'message': 'SAVED PLACES'
        })