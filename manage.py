#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import debugpy

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wemake.settings')
    
    if(os.environ['DEBUG'])=="TRUE":
        print("Waiting for debugger to attach.....")
        try:
            
            debugpy.listen(("0.0.0.0", 3002))
            debugpy.wait_for_client()
            print('Attached!')
        except Exception as e:
            pass

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
    main()
