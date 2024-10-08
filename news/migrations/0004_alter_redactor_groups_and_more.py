# Generated by Django 5.1.1 on 2024-09-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("news", "0003_alter_redactor_groups_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="redactor",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to.",
                related_name="redactor_set",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AlterField(
            model_name="redactor",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="redactor_user_set",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
