from django.shortcuts import render

# Create your views here.

def profile_view(request):

    return render(request, 'authed/profile/index.html', {
        'status': 'info',
        'message': 'RECENT VIEWED PLACES'
        })