from django.apps import apps
from django.contrib.auth.models import Group
from django.views.generic import TemplateView

from django.conf import settings
from django.apps import apps

class ValiDashboardView(TemplateView):
    template_name = 'dashboard.html'
    # default count users data
    users = (apps.get_model(settings.AUTH_USER_MODEL)).objects.count()
    # default count groups data
    groups = Group.objects.count()
    # default count apps data
    apps_len = len(apps.get_models())

    # default charts data
    charts = [
        {
            # Support Chart types: Bar, Line, Radar
            "chart_type1": ["Bar", "Line", "Radar"],
            "name": "barchart1",
            "title": "Barchart",
            "type": "Bar",
            "labels": ["2018-03-01", "2018-03-02", "2018-03-03", "2018-03-04", "2018-03-05"],
            "datasets": [
                {
                    "label": "dataset 1",
                    "fillColor": "rgba(220,220,220,0.2)",
                    "strokeColor": "rgba(220,220,220,1)",
                    "pointColor": "rgba(220,220,220,1)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": [65, 59, 80, 81, 80]
                },
                {
                    "label": "dataset 2",
                    "fillColor": "rgba(151,187,205,0.2)",
                    "strokeColor": "rgba(151,187,205,1)",
                    "pointColor": "rgba(151,187,205,1)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(151,187,205,1)",
                    "data": [28, 48, 40, 19, 69]
                }
            ],
        },
        {
            # Support Chart types: PolarArea, Pie, Doughnut
            "chart_type2": ["PolarArea", "Pie", "Doughnut"],
            "name": "piechart1",
            "title": "Piechart",
            "type": "Pie",
            "pdatasets": [
                {
                    "value": 300,
                    "color": "#F7464A",
                    "highlight": "#FF5A5E",
                    "label": "Red"
                },
                {
                    "value": 50,
                    "color": "#46BFBD",
                    "highlight": "#5AD3D1",
                    "label": "Green"
                },
                {
                    "value": 100,
                    "color": "#FDB45C",
                    "highlight": "#FFC870",
                    "label": "Yellow"
                },
            ]
        }
    ]

    # default icons data
    top_icons = [
        {"title": "Users", "value": users, "style": "primary", "icon": "fa-user-circle"},
        {"title": "Groups", "value": groups, "style": "warning", "icon": "fa-users"},
        {"title": "Apps", "value": apps_len, "style": "info", "icon": "fa-briefcase"},
        {"title": "Charts", "value": len(charts), "style": "danger", "icon": "fa-line-chart"},
    ]

    def get_context_data(self, **kwargs):
        context = super(ValiDashboardView, self).get_context_data(**kwargs)
        # load sample data
        context['icons'] = self.top_icons
        context['charts'] = self.charts
        context['users'] = self.users
        return context
