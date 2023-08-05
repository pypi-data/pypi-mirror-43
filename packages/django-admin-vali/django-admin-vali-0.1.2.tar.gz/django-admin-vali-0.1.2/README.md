# Django Admin Vali  

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
  https://github.com/cnanyi/django-vali.
 
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

In your `'counters.py'` add ...

    from vali.counters import CounterBase
    from .models import MyModel

    class MyModelCounter(CounterBase):
        title = 'Title goes here'

        def get_value(self, request):
            return MyModel.objects.count()  

In your `'views.py'` add ...

    from .counters import MyModelCounter
    from vali.views import ValiDashboardBase

    class MyModelDashboardView(ValiDashboardBase):
        template_name = 'dashboard.html'

        list_counters = [
            MyModelCounter(),
        ]   

License
--------
This project is licensed under the [MIT](LICENSE) License.