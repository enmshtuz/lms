
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_remove_course_published_date_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='is_forced_enrollment',
            field=models.BooleanField(default=False),
        ),
    ]
