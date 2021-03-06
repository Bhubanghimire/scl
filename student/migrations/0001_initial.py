# Generated by Django 3.2.4 on 2021-06-15 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
        ('parent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ManyToManyField(blank=True, related_name='parent', to='parent.Parent')),
                ('student', models.ManyToManyField(blank=True, related_name='student', to='administration.Admission')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_now', models.DateField(auto_now=True)),
                ('status', models.CharField(choices=[('P', 'P'), ('A', 'A')], default='', max_length=5)),
                ('class_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.classroom')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance', to='student.student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.subject')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacherforattendance', to='administration.staff')),
            ],
        ),
    ]
