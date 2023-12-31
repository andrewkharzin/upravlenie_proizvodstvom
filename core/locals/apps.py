# Application definition

DJANGO_APPS = [
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
   'apps.accounts',
   'apps.sklad',
   'apps.sklad.materials',
   'apps.sklad.inventory',
   'apps.sklad.order',
   'apps.employees',
   'apps.infobase',
]
    
THIRDPARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'mptt',
    'django_mptt_admin',
    'import_export',
    'schedule',
    'djangobower',
    'star_ratings',
    'phonenumber_field',

]
    
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRDPARTY_APPS

