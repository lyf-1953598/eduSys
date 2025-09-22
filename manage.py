'''
Author: shaojinxin
Date: 2022-09-14 11:01:49
LastEditTime: 2022-09-15 10:32:36
Description: 

Copyright (c) 2022 by shaojinxin/citorytech, All Rights Reserved. 
'''
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import webbrowser

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    from django.core.management.commands.runserver import Command as Runserver
    main()
