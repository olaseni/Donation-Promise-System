from random import randint

from django import template
from collections import OrderedDict

from dps_main.utilities.fusioncharts import FusionCharts

from dps_main.utilities.actions import ActionHelper

register = template.Library()


@register.simple_tag(takes_context=True)
def action_helper_ping(context):
    """
    Pings the action helper
    """
    return ActionHelper(context.get('user')).ping()


@register.inclusion_tag(takes_context=True, filename='dps_main/tags/fusion_bar_chart.html')
def fusion_bar_chart_cause(context, report, caption='Title', x_axis='X Axis', y_axis='Y Axis', number_prefix='',
                           number_suffix=''):
    # Chart data is passed here in key-value pairs.
    data_source = OrderedDict()

    # Dict contains key-value pairs of data for chart attribute
    config = {"caption": caption,
              "xAxisName": x_axis,
              "yAxisName": y_axis,
              "numberPrefix": number_prefix,
              "numberSuffix": number_suffix,
              "theme": "fusion"}

    # report should be an ordereddict containing key-value pairs of data
    report = report or OrderedDict()

    data_source["chart"] = config
    data_source["data"] = []

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array
    # is a JSON object# having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
    for key, value in report.items():
        data = {"label": key, "value": value}
        data_source["data"].append(data)

    html_id = F'fusion-{randint(11111111, 999999999)}-chart'
    html_div_container = F'{html_id}-container'

    # Create an object for the chart using the FusionCharts constructor
    chart = FusionCharts("bar3d", html_id, "80%", "500", html_div_container, "json", data_source)

    return {'output': chart.render(),
            'html_id': html_id,
            'html_container': html_div_container}
