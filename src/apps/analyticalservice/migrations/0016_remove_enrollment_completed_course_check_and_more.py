# Generated by Django 5.0.3 on 2024-05-14 17:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticalservice', '0015_rename_completed_date_progress_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='enrollment',
            name='completed_course_check',
        ),
        migrations.AddConstraint(
            model_name='enrollment',
            constraint=models.CheckConstraint(check=models.Q(('completed_course', False), ('completion_date__isnull', True)), name='completion_date_null_if_not_completed'),
        ),
        migrations.AddConstraint(
            model_name='enrollment',
            constraint=models.CheckConstraint(check=models.Q(('completed_course', True), ('completion_date__isnull', False)), name='completion_date_not_null_if_completed'),
        ),
    ]
