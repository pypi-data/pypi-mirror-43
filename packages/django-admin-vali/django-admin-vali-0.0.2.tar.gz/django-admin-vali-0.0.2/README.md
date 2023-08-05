# Projeto: Django Admin Vali

## Glosário de termos

### Atores

**Administrador:** Usuário que possui permissão para acessar o dashboard.

#### Requisitos
* Django:
  * **versão:**```2.0+```

### Rotas
* Site:
  * **url:**```/admin```
    Página com acesso ao administrador.
  * **url:**```/admin/dashboard```
    Página com acesso ao dashboard.

### Funcionalidades
* Usuário:
  * **url:**```/admin```
    * Pode visualizar o log do sistema.
  * **url:**```/admin/dashboard```
    * Pode visualizar dados dinâmicos do sistema.
 
# Installation

Install using `pip`...

    pip install django-admin-vali

Add `'vali'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'vali',
    )  

If you use Dashboard, include `'vali'` to your `urls.py` setting.

    urlpatterns = (
        ...
        path('admin/', include(('vali.urls','vali'), namespace='dashboard')),
        ...
    )
