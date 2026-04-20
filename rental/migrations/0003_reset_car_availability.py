from django.db import migrations


def reset_car_availability(apps, schema_editor):
    Car = apps.get_model("rental", "Car")
    Car.objects.all().update(available=True)


class Migration(migrations.Migration):

    dependencies = [
        ("rental", "0002_user_role_alter_user_is_customer"),
    ]

    operations = [
        migrations.RunPython(reset_car_availability, migrations.RunPython.noop),
    ]