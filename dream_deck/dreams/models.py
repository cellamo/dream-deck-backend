from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='dream_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='dream_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dreams')
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_lucid = models.BooleanField(default=False)
    audio_recording = models.FileField(upload_to='dream_recordings/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s dream: {self.title}"

class Emotion(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DreamEmotion(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='emotions')
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    intensity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = ('dream', 'emotion')

class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DreamTheme(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='themes')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('dream', 'theme')

class ArtworkGeneration(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='artworks')
    image = models.ImageField(upload_to='dream_artworks/')
    created_at = models.DateTimeField(auto_now_add=True)

class SoundtrackGeneration(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='soundtracks')
    audio_file = models.FileField(upload_to='dream_soundtracks/')
    created_at = models.DateTimeField(auto_now_add=True)

class DreamChallenge(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.ForeignKey(DreamChallenge, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'challenge')

class LucidDreamingProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lucid_progress')
    techniques_practiced = models.TextField()
    success_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

class CulturalInterpretation(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='cultural_interpretations')
    culture = models.CharField(max_length=100)
    interpretation = models.TextField()

class DailyTask(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name='daily_tasks')
    task_description = models.TextField()
    completed = models.BooleanField(default=False)

class DreamMeditation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meditations')
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='dream_meditations/')
    created_at = models.DateTimeField(auto_now_add=True)

class DreamPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompts')
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s prompt: {self.prompt_text[:50]}..."

class CollaborativeDream(models.Model):
    prompt = models.ForeignKey(DreamPrompt, on_delete=models.CASCADE, related_name='collaborative_dreams')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collaborative dream by {self.user.username} for prompt: {self.prompt.prompt_text[:50]}..."

class DreamInsight(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE, related_name='insight')
    summary = models.TextField()
    analysis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Insight for {self.dream.title}"
