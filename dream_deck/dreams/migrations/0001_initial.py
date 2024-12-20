# Generated by Django 5.0.6 on 2024-07-01 21:52

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('is_lucid', models.BooleanField(default=False)),
                ('audio_recording', models.FileField(blank=True, null=True, upload_to='dream_recordings/')),
            ],
        ),
        migrations.CreateModel(
            name='DreamChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_tasks', to='dreams.dream')),
            ],
        ),
        migrations.CreateModel(
            name='CulturalInterpretation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('culture', models.CharField(max_length=100)),
                ('interpretation', models.TextField()),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cultural_interpretations', to='dreams.dream')),
            ],
        ),
        migrations.CreateModel(
            name='ArtworkGeneration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='dream_artworks/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks', to='dreams.dream')),
            ],
        ),
        migrations.CreateModel(
            name='SoundtrackGeneration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='dream_soundtracks/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soundtracks', to='dreams.dream')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('bio', models.TextField(blank=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('is_premium', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='dream_users', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='dream_users', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LucidDreamingProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('techniques_practiced', models.TextField()),
                ('success_rate', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lucid_progress', to='dreams.user')),
            ],
        ),
        migrations.CreateModel(
            name='DreamPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prompts', to='dreams.user')),
            ],
        ),
        migrations.CreateModel(
            name='DreamMeditation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('audio_file', models.FileField(upload_to='dream_meditations/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meditations', to='dreams.user')),
            ],
        ),
        migrations.AddField(
            model_name='dream',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dreams', to='dreams.user'),
        ),
        migrations.CreateModel(
            name='CollaborativeDream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dream_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborative_dreams', to='dreams.dreamprompt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dreams.user')),
            ],
        ),
        migrations.CreateModel(
            name='DreamEmotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intensity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emotions', to='dreams.dream')),
                ('emotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dreams.emotion')),
            ],
            options={
                'unique_together': {('dream', 'emotion')},
            },
        ),
        migrations.CreateModel(
            name='DreamTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='dreams.dream')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dreams.theme')),
            ],
            options={
                'unique_together': {('dream', 'theme')},
            },
        ),
        migrations.CreateModel(
            name='UserChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dreams.dreamchallenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='dreams.user')),
            ],
            options={
                'unique_together': {('user', 'challenge')},
            },
        ),
    ]
