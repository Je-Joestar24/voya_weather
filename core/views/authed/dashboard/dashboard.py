"""
Dashboard View Module
---------------------
Handles the user dashboard, including summary statistics, recent activity, and highlights of favorite/saved places.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .highlights_helper import get_highlights
from .summary_helper import get_summary
from .recents_helper import get_recents

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'authed/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'status': 'info',
            'message': 'DASHBOARD',
            'summary': get_summary(user),
            'recents': get_recents(user),
            'highlights': get_highlights(user),
        })
        return context