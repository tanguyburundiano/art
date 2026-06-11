from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legaltexts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Part',
            new_name='Sector',
        ),
        migrations.RenameModel(
            old_name='Section',
            new_name='Part',
        ),
        migrations.RenameField(
            model_name='part',
            old_name='part',
            new_name='sector',
        ),
        migrations.RenameField(
            model_name='legalarticle',
            old_name='section',
            new_name='part',
        ),
        migrations.AlterField(
            model_name='part',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='legaltexts.sector'),
        ),
        migrations.AlterField(
            model_name='legalarticle',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='legaltexts.part'),
        ),
    ]
