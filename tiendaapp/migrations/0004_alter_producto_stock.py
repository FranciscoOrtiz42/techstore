from django.core.validators import MaxValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaapp', '0003_alter_producto_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.PositiveIntegerField(
                default=0,
                validators=[MaxValueValidator(9999)],
            ),
        ),
    ]