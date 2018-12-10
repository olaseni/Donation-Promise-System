from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext

from adminplus.sites import AdminSitePlus

__all__ = ['register_admin_views']


class AdminSite(AdminSitePlus):
    index_template = 'admin/index.html'


def register_admin_views():
    """
    Registers admin customizations
    """

    @admin.site.register_view('reports/causes/amount', name='Top 5 causes by amount')
    def reports_cause_amount(request):
        """
        A view to provide reports
        """
        # Fanciness.
        return render_to_response('admin/reports/causes-amount.html',
                                  {'title': 'Top causes by amount'},
                                  RequestContext(request, {}))

    @admin.site.register_view('reports/causes/promises', name='Top 5 causes by promises')
    def reports_causes_promises(request):
        """
        A view to provide reports
        """
        # Fanciness.
        return render_to_response('admin/reports/causes-promises.html',
                                  {'title': 'Top causes by promises'},
                                  RequestContext(request, {}))