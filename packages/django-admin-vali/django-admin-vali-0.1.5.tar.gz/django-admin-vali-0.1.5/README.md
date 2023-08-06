# Django Admin Vali  

[![GitHub version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&type=6&v=0.1.5&x2=0)](https://pypi.org/project/django-admin-vali/)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/JchJ/Vali-Django-Admin/blob/master/LICENSE)

**Note**

This project is based in django-vali project from cnanyi  
https://github.com/cnanyi/django-vali.

## Overview  

### Administrator
  * User who has permission to access the dashboard.
  * Can view all log entries.
  * Can view all dynamics data.

#### Requirements
  * django >= 2.0
  * python >= 3.0  

### Routes
* Site:
  * **url:** ```/admin```
    * Page with administrator access.
  * **url:** ```/admin/dashboard```
    * Page with dashboard access.

  **Extra**

  This project allows you to use i18n in urls
  https://docs.djangoproject.com/en/2.0/topics/i18n/.
 
# Installation

Install using `pip`...

    pip install django-admin-vali

Add `'vali'` to your `INSTALLED_APPS` setting before `'django.contrib.admin'`.

    INSTALLED_APPS = (
        ...
        'vali',
        'django.contrib.admin',
        ...
    )  

If you use Dashboard, include `'vali'` to your `urls.py` setting.

    urlpatterns = (
        ...
        path('admin/', include(('vali.urls','vali'), namespace='dashboard')),
        ...
    )

In your settings, add `VALI_CONFIG`.

    VALI_CONFIG = {
      'theme': 'default',
      'dashboard': {
          'name': 'Dashboard',
          'url': '/admin/dashboard/',
          'subtitle': 'Dashboard view with all statistics',
          'site_name': 'Dashboard admin',
          'url_image_profile': ''
      },
      'applist': {
          "order": "registry", "group": True
      },
    }  
  
# Usage  

**Note**

You can use the model that you want.  

In your `'counters.py'` add ...

    from vali.counters import CounterBase
    from .models import Messages

    class MessagesCounter(CounterBase):
        title = 'Title goes here'

        def get_value(self, request):
            return Messages.objects.count()  

or  

    from vali.counters import ModelCounter
    from .models import Messages

    class MessagesCounter(ModelCounter):
        model = Messages  

![alt text](/vali/static/img/counter.png)  
  
In your `'charts.py'` add ...

    from vali.charts import ModelCharts
    from .models import Messages


    class ChartCounter(ModelCharts):
        model = Messages

        chart_type = 'Bar'
        name = 'barchart1'
        labels = ["2018-03-01", "2018-03-02", "2018-03-03", "2018-03-04", "2018-03-05"]
        datasets = [
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
        ]  

In your `'views.py'` add ...

    from .counters import MessagesCounter
    from .charts import ChartCounter
    from vali.views import ValiDashboardBase

    class MessagesDashboardView(ValiDashboardBase):
        template_name = 'dashboard.html'

        list_counters = [
            MessagesCounter(),
        ]   
        list_charts = [
            ChartCounter(),
        ]
  
License
--------
This project is licensed under the [MIT](LICENSE) License.