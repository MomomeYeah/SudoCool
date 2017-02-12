#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get('DEPLOY_ENVIRONMENT') == 'heroku':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
