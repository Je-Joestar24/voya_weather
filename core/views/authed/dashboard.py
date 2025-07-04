from django.shortcuts import render

# Create your views here.

def dashboard_view(request):

    return render(request, 'authed/dashboard/index.html', {
        'status': 'info',
        'message': 'DASHBOARD'
        })