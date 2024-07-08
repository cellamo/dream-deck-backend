from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai

from django.conf import settings

from .serializers import DreamSerializer, EmotionSerializer, ThemeSerializer
from .models import Dream, Emotion, Theme, DreamEmotion, DreamTheme
from .auth_views import SignUpView, LoginView  # noqa: F401


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class DreamViewSet(viewsets.ModelViewSet):
    queryset = Dream.objects.all()
    serializer_class = DreamSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Dream.objects.all()
        return Dream.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff or instance.user == self.request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this dream."},
                            status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=["get"])
    def my_dreams(self, request):
        dreams = Dream.objects.filter(user=self.request.user)
        serializer = self.get_serializer(dreams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def all_dreams(self, request):
        if not request.user.is_premium:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )
        dreams = Dream.objects.all()
        serializer = self.get_serializer(dreams, many=True)
        return Response(serializer.data)

class EmotionViewSet(viewsets.ModelViewSet):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Emotion.objects.all()

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Theme.objects.all()
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_themes(request):
    content = request.data.get('content')
    if not content:
        return Response({"error": "No content provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Configure the Gemini model
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate theme suggestions with a specific format
    prompt = f"""Based on the following dream content, suggest 3 relevant themes.
    Please format your response as a numbered list, with each theme on a new line.
    Each theme should be a single word.
    Do not include any additional text or explanations.

    Dream content:
    {content}

    Response format example:
    1. Adventure
    2. Mystery
    3. Nature

    Your theme suggestions:"""

    try:
        response = model.generate_content(prompt)

        # Process the response
        themes = [theme.strip().split('. ', 1)[-1] for theme in response.text.split('\n') if theme.strip() and theme[0].isdigit()]

        return Response({"suggested_themes": themes})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_emotions(request):
    content = request.data.get('content')
    if not content:
        return Response({"error": "No content provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Configure the Gemini model
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate emotion suggestions with a specific format
    prompt = f"""Based on the following dream content, suggest 3 relevant emotions that the dreamer might have experienced.
    Please format your response as a numbered list, with each emotion on a new line.
    Do not include any additional text or explanations.

    Dream content:
    {content}

    Response format example:
    1. Joy
    2. Anxiety
    3. Curiosity
    
    Your emotion suggestions:"""

    try:
        response = model.generate_content(prompt)
        print(response.text)

        # Process the response
        emotions = []
        for line in response.text.split('\n'):
            if line.strip() and line[0].isdigit():
                parts = line.split('.', 1)[-1].strip().split('(', 1)
                if len(parts) >= 1:
                    emotion = parts[0].strip()
                    emotions.append({"name": emotion})

        return Response({"suggested_emotions": emotions})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_title(request):
    content = request.data.get('content')
    if not content:
        return Response({"error": "No content provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Configure the Gemini model
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate title suggestion with a specific format
    prompt = f"""Based on the following dream content, suggest a creative and engaging title for the dream.
    The title should be concise (no more than 10 words) and capture the essence or most striking element of the dream.
    Please provide only the title, without any additional text or explanations.

    Dream content:
    {content}

    Your title suggestion:"""

    try:
        response = model.generate_content(prompt)

        # Process the response
        suggested_title = response.text.strip()

        # Ensure the title is not too long
        if len(suggested_title.split()) > 10:
            suggested_title = ' '.join(suggested_title.split()[:10]) + '...'

        return Response({"suggested_title": suggested_title})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)