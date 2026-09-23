from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaapp', '0004_alter_producto_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(
                decimal_places=0,
                max_digits=10,
                validators=[MinValueValidator(1000)],
            ),
        ),
    ]