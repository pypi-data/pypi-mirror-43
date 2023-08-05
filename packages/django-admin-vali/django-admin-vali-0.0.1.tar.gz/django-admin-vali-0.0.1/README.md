# Projeto: Bootstrap Vali Django Admin

## Glosário de termos

### Atores

**Administrador:** Usuário que possui permissão para acessar o dashboard.

#### Requisitos
* Django:
  * **versão:**```2.0+```

### Rotas
* Site:
  * **url:**```/<lang>/admin```
    Página com acesso ao administrador.
  * **url:**```/<lang>/admin/dashboard```
    Página com acesso ao dashboard.

### Funcionalidades
* Usuário:
  * **url:**```/<lang>/admin```
    * Pode visualizar o log do sistema.
  * **url:**```/<lang>/admin/dashboard```
    * Pode visualizar dados dinâmicos do sistema.

#### Início
```bash
    apt-get install python-pip
    pip install virtualenv <envname>
    source envname/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
```

## Changelog
*02/03/2019* - Início  
*05/03/2019* - Adicionando funcionalidade de impressão de múltiplos e-mails.  
*05/03/2019* - Adicionando funcionalidade de impressão individual de e-mail.  
*06/03/2019* - Adicionando funcionalidade de exportar os contatos selecionados em um arquivo csv.  