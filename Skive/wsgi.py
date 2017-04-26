import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

# sets the settings environment variable to use the production settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Skive.settings.production")

# web server gateway interface (wsgi)
application = get_wsgi_application()

# whitenoise allows the web app to serve its own staticfiles
application = DjangoWhiteNoise(application)
