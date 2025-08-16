from django.db import migrations

def forwards(apps, schema_editor):
    if "oc_lettings_site_profile" not in schema_editor.connection.introspection.table_names():
        return

    OldProfile = apps.get_model("oc_lettings_site", "Profile")
    NewProfile = apps.get_model("profiles", "Profile")

    for old in OldProfile.objects.all().iterator():
        NewProfile.objects.update_or_create(
            id=old.id,
            defaults=dict(
                user_id=old.user_id,
                favorite_city=getattr(old, "favorite_city", ""),
            ),
        )

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
        ("oc_lettings_site", "0001_initial"),
    ]
    operations = [migrations.RunPython(forwards, backwards)]