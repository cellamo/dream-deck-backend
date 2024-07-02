from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Dream, Emotion, DreamEmotion, Theme, DreamTheme, 
    ArtworkGeneration, SoundtrackGeneration, DreamChallenge, 
    UserChallenge, LucidDreamingProgress, CulturalInterpretation, 
    DailyTask, DreamMeditation, DreamPrompt, CollaborativeDream
)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_premium', 'date_of_birth', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('bio', 'date_of_birth', 'is_premium')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('bio', 'date_of_birth', 'is_premium')}),
    )

class DreamEmotionInline(admin.TabularInline):
    model = DreamEmotion
    extra = 1

class DreamThemeInline(admin.TabularInline):
    model = DreamTheme
    extra = 1

class DreamAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'date', 'is_lucid']
    list_filter = ['is_lucid', 'date']
    search_fields = ['title', 'content', 'user__username']
    inlines = [DreamEmotionInline, DreamThemeInline]

class DreamChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']

class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'completed']
    list_filter = ['completed']

class LucidDreamingProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'success_rate']

class CulturalInterpretationAdmin(admin.ModelAdmin):
    list_display = ['dream', 'culture']

class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ['dream', 'task_description', 'completed']
    list_filter = ['completed']

class DreamMeditationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']

class DreamPromptAdmin(admin.ModelAdmin):
    list_display = ['user', 'prompt_text', 'created_at']

class CollaborativeDreamAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'user', 'created_at']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Dream, DreamAdmin)
admin.site.register(Emotion)
admin.site.register(Theme)
admin.site.register(ArtworkGeneration)
admin.site.register(SoundtrackGeneration)
admin.site.register(DreamChallenge, DreamChallengeAdmin)
admin.site.register(UserChallenge, UserChallengeAdmin)
admin.site.register(LucidDreamingProgress, LucidDreamingProgressAdmin)
admin.site.register(CulturalInterpretation, CulturalInterpretationAdmin)
admin.site.register(DailyTask, DailyTaskAdmin)
admin.site.register(DreamMeditation, DreamMeditationAdmin)
admin.site.register(DreamPrompt, DreamPromptAdmin)
admin.site.register(CollaborativeDream, CollaborativeDreamAdmin)
