import os
import django
from django.core.management import call_command

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyshop.settings")
    django.setup()
    with open("data.json", "w", encoding="utf-8") as f:
        call_command(
            "dumpdata",
            "--natural-primary",
            "--natural-foreign",
            "--exclude", "auth.permission",
            "--exclude", "contenttypes",
            stdout=f,
            indent=2
        )

