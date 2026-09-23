from django.db import migrations, models
from django.core.validators import MinValueValidator


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaapp', '0002_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(
                decimal_places=0,
                max_digits=10,
                validators=[MinValueValidator(0)],
            ),
        ),
    ]