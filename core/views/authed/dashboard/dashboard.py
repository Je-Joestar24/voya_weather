"""
Dashboard View Module
---------------------
Handles the user dashboard, including summary statistics, recent activity, and highlights of favorite/saved places.
"""

from core.views.authed.util  import render, login_required
from .highlights_helper import get_highlights
from .summary_helper import get_summary
from .recents_helper import get_recents

@login_required
def dashboard_view(request):
    """
    Render the dashboard page for authenticated users, including summary, recents, and highlights.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the dashboard template with context data.
    """
    user = request.user
    summary = get_summary(user)
    recents = get_recents(user)
    highlights = get_highlights(user)

    return render(request, 'authed/dashboard/index.html', {
        'status': 'info',
        'message': 'DASHBOARD',
        'summary': summary,
        'recents': recents,
        'highlights': highlights,
    })