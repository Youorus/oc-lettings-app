from django.db import migrations

def forwards(apps, schema_editor):
    tables = schema_editor.connection.introspection.table_names()
    # pas de source -> on sort proprement
    if "oc_lettings_site_profiles" not in tables or "oc_lettings_site_letting" not in tables:
        return

    OldAddress = apps.get_model("oc_lettings_site", "profiles")  # ancien "Address"
    OldLetting = apps.get_model("oc_lettings_site", "Letting")
    NewAddress = apps.get_model("lettings", "Address")
    NewLetting = apps.get_model("lettings", "Letting")

    # 1) addresses (upsert par PK)
    for old in OldAddress.objects.all().iterator():
        NewAddress.objects.update_or_create(
            id=old.id,
            defaults=dict(
                number=old.number,
                street=old.street,
                city=old.city,
                state=old.state,
                zip_code=old.zip_code,
                country_iso_code=old.country_iso_code,
            ),
        )

    # 2) lettings (upsert par PK)
    for old in OldLetting.objects.all().iterator():
        NewLetting.objects.update_or_create(
            id=old.id,
            defaults=dict(
                title=old.title,
                address_id=old.profiles_id,  # l’ancienne O2O pointait vers "profiles"
            ),
        )

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ("lettings", "0001_initial"),
        ("oc_lettings_site", "0001_initial"),
    ]
    operations = [migrations.RunPython(forwards, backwards)]