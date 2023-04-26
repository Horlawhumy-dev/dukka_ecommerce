# Generated by Django 4.2 on 2023-04-26 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("payment", "0003_alter_transaction_user_involved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="user_involved",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_transaction",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
