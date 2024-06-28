# Generated by Django 5.0.4 on 2024-06-28 03:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct_requests', '0001_initial'),
        ('register', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drctinternalnote',
            name='fk_campus',
        ),
        migrations.RemoveField(
            model_name='drctinternalnote',
            name='fk_reporter',
        ),
        migrations.RemoveField(
            model_name='drctregulament',
            name='fk_drct_internal_note',
        ),
        migrations.RemoveField(
            model_name='drctstudentinternalnote',
            name='fk_drct_internal_note',
        ),
        migrations.RemoveField(
            model_name='drctstudentinternalnote',
            name='fk_student',
        ),
        migrations.CreateModel(
            name='CTCIInternalNote',
            fields=[
                ('pk_ct_ci_internal_note', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=128)),
                ('ct_ci_single_attach', models.CharField(max_length=30)),
                ('ct_ci_deadline', models.DateField()),
                ('ct_ci_student_deadline', models.DateField()),
                ('ct_ci_cal_statement', models.IntegerField(null=True)),
                ('ct_ci_cmdt_statement', models.IntegerField(null=True)),
                ('ct_ci_cmdt_answer', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField()),
                ('status', models.IntegerField()),
                ('fk_campus', models.ForeignKey(db_column='fk_campus', on_delete=django.db.models.deletion.DO_NOTHING, to='register.campus')),
                ('fk_reporter', models.ForeignKey(db_column='fk_reporter', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_ct_ci_internal_note',
            },
        ),
        migrations.CreateModel(
            name='CTCIComment',
            fields=[
                ('pk_ct_ci_comment', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('fk_user', models.ForeignKey(db_column='fk_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('fk_ct_ci_internal_note', models.ForeignKey(db_column='fk_ct_ci_internal_note', on_delete=django.db.models.deletion.CASCADE, to='ct_requests.ctciinternalnote')),
            ],
            options={
                'db_table': 'tb_ct_ci_comment',
            },
        ),
        migrations.CreateModel(
            name='CTCIRegulament',
            fields=[
                ('pk_ct_ci_regulament', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('regulament', models.CharField(max_length=30)),
                ('fk_ct_ci_internal_note', models.ForeignKey(db_column='fk_ct_ci_internal_note', on_delete=django.db.models.deletion.CASCADE, to='ct_requests.ctciinternalnote')),
            ],
            options={
                'db_table': 'tb_ct_ci_regulament',
            },
        ),
        migrations.CreateModel(
            name='CTCIStudentInternalNote',
            fields=[
                ('pk_ct_ci_student_internal_note', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('fk_ct_ci_internal_note', models.ForeignKey(db_column='fk_ct_ci_internal_note', on_delete=django.db.models.deletion.CASCADE, to='ct_requests.ctciinternalnote')),
                ('fk_student', models.ForeignKey(db_column='fk_student', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_ct_ci_student_internal_note',
            },
        ),
        migrations.DeleteModel(
            name='DRCTComment',
        ),
        migrations.DeleteModel(
            name='DRCTRegulament',
        ),
        migrations.DeleteModel(
            name='DRCTInternalNote',
        ),
        migrations.DeleteModel(
            name='DRCTStudentInternalNote',
        ),
    ]
