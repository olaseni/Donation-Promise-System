from collections import OrderedDict

from django.contrib import admin
from django.shortcuts import render

from adminplus.sites import AdminSitePlus

from .reports import top_causes_by_amount, top_causes_by_promises

__all__ = ['register_admin_views']


class AdminSite(AdminSitePlus):
    index_template = 'dps_main/admin/index.html'


def register_admin_views():
    """
    Registers admin customizations
    """

    def query_to_dict(q, k, v):
        """
        Consume a queryset into a dict
        """
        o = OrderedDict()
        for item in q:
            o['%s/%s' % (getattr(item, 'id'), getattr(item, k))] = getattr(item, v)
        return o

    @admin.site.register_view('reports/causes/amount', name='Top 5 causes by amount')
    def reports_cause_amount(request):
        """
        A view to provide reports
        """
        return render(request, 'dps_main/admin/reports/causes-amount.html',
                      {'title': 'Top causes by amount',
                       'report': query_to_dict(top_causes_by_amount(), 'title', 'sum')})

    @admin.site.register_view('reports/causes/promises', name='Top 5 causes by promises')
    def reports_causes_promises(request):
        """
        A view to provide reports
        """
        return render(request, 'dps_main/admin/reports/causes-promises.html',
                      {'title': 'Top causes by promises',
                       'report': query_to_dict(top_causes_by_promises(), 'title', 'count')})
