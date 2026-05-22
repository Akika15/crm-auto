from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('crm_app', '0005_alter_client_email_alter_client_phone'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE crm_app_client DROP CONSTRAINT crm_app_client_phone_key;",
            reverse_sql="ALTER TABLE crm_app_client ADD CONSTRAINT crm_app_client_phone_key UNIQUE (phone);"
        ),
        migrations.RunSQL(
            "ALTER TABLE crm_app_client DROP CONSTRAINT crm_app_client_email_key;",
            reverse_sql="ALTER TABLE crm_app_client ADD CONSTRAINT crm_app_client_email_key UNIQUE (email);"
        ),
    ]