from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os
from dotenv import load_dotenv

from django.conf import settings

from .serializers import DreamSerializer, EmotionSerializer, ThemeSerializer
from .models import Dream, DreamInsight, Emotion, Theme, DreamEmotion, DreamTheme
from .auth_views import SignUpView, LoginView  # noqa: F401

import logging

gemini_logger = logging.getLogger("gemini_usage")


def log_gemini_usage(function_name, prompt_tokens, response_tokens):
    gemini_logger.info(
        f"{function_name}, Prompt tokens: {prompt_tokens}, Response tokens: {response_tokens}"
    )

load_dotenv()

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
            return Response(
                {"detail": "You do not have permission to delete this dream."},
                status=status.HTTP_403_FORBIDDEN,
            )

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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_themes(request):
    content = request.data.get("content")
    if not content:
        return Response(
            {"error": "No content provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")

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

        # Estimate token counts
        prompt_tokens = len(prompt) // 4
        response_tokens = len(response.text) // 4

        log_gemini_usage("suggest_themes", prompt_tokens, response_tokens)

        # Process the response
        themes = [
            theme.strip().split(". ", 1)[-1]
            for theme in response.text.split("\n")
            if theme.strip() and theme[0].isdigit()
        ]

        return Response({"suggested_themes": themes})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_emotions(request):
    content = request.data.get("content")
    if not content:
        return Response(
            {"error": "No content provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Configure the Gemini model
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")

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

        # Estimate token counts
        prompt_tokens = len(prompt) // 4
        response_tokens = len(response.text) // 4

        log_gemini_usage("suggest_emotion", prompt_tokens, response_tokens)

        # Process the response
        emotions = []
        for line in response.text.split("\n"):
            if line.strip() and line[0].isdigit():
                parts = line.split(".", 1)[-1].strip().split("(", 1)
                if len(parts) >= 1:
                    emotion = parts[0].strip()
                    emotions.append({"name": emotion})

        return Response({"suggested_emotions": emotions})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_title(request):
    content = request.data.get("content")
    if not content:
        return Response(
            {"error": "No content provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Configure the Gemini model
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate title suggestion with a specific format
    prompt = f"""Based on the following dream content, suggest a creative and engaging title for the dream.
    The title should be concise (no more than 10 words) and capture the essence or most striking element of the dream.
    Please provide only the title, without any additional text or explanations.

    Dream content:
    {content}
    
    ALWAYS USE USER'S LANGUAGE!!!

    Your title suggestion:"""

    try:
        response = model.generate_content(prompt)

        # Estimate token counts
        prompt_tokens = len(prompt) // 4
        response_tokens = len(response.text) // 4

        log_gemini_usage("suggest_title", prompt_tokens, response_tokens)

        # Process the response
        suggested_title = response.text.strip()

        # Ensure the title is not too long
        if len(suggested_title.split()) > 10:
            suggested_title = " ".join(suggested_title.split()[:10]) + "..."

        return Response({"suggested_title": suggested_title})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_dream_insight(request):
    dream_id = request.data.get("dream_id")
    if not dream_id:
        return Response(
            {"error": "No dream ID provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    dream = get_object_or_404(Dream, id=dream_id, user=request.user)
    content = dream.content

    # Load the dream interpretation knowledge base
    knowledge_base_path = os.path.join(
        settings.BASE_DIR, "dreams", "dream_interpretation_knowledge.txt"
    )
    with open(knowledge_base_path, "r") as file:
        knowledge_base = file.read()

    # Configure the Gemini model
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel(
        "gemini-1.5-pro"
    )  # Using a more capable model for this task

    # Generate dream insight with cultural interpretations
    prompt = f"""Using the following dream interpretation knowledge base as a guideline, provide insights and cultural interpretations for the given dream content. Include perspectives from at least three different cultures.

    Knowledge Base:
    {knowledge_base}

    Dream content:
    {content}

    Please structure your response as follows:
    1. General Insight: Provide a brief general interpretation of the dream.
    2. Cultural Interpretations:
       - Culture 1: [Name of Culture]
         [Interpretation from this cultural perspective]
       - Culture 2: [Name of Culture]
         [Interpretation from this cultural perspective]
       - Culture 3: [Name of Culture]
         [Interpretation from this cultural perspective]
    3. Key Symbols: List and briefly explain 3-5 key symbols from the dream.
    4. Emotional Analysis: Suggest the emotional state of the dreamer and its potential significance.
    5. Actionable Advice: Provide 1-2 suggestions for the dreamer based on this interpretation."""

    prompt2 = """You are an AI dream analyst for the Dream Deck app. Your task is to analyze user-submitted dream content and provide insightful, creative, and original interpretations based on a provided dream interpretation knowledge base. Your messages will be sent directly to user except the <scratchpad> and <dream_summary>. So talk directly to them. Always write in the Dream Content language.

Next, you will receive the user's dream content:

<dream_content>
{content}
</dream_content>

Analyze the dream content using the provided knowledge base. Be creative and original in your interpretations, going beyond simple symbol matching. Consider the overall narrative, emotions, and themes present in the dream.

Before providing your final analysis, use a <scratchpad> to think through your interpretation process. Consider different aspects of the dream and how they might relate to the dreamer's subconscious mind, daily life, or emotional state.

Your final analysis should be divided into the following sections, each wrapped in appropriate XML tags:

1. <dream_summary>: Provide a brief summary of the key elements and narrative of the dream.

2. <emotional_landscape>: Analyze the emotions present in the dream and what they might represent.

3. <symbolic_analysis>: Interpret key symbols or objects in the dream, relating them to possible meanings in the dreamer's life.

4. <narrative_interpretation>: Examine the overall story or sequence of events in the dream and what it might signify.

5. <personal_growth_insights>: Offer suggestions on how the dreamer might use insights from the dream for personal development or problem-solving in their waking life.

6. <cultural_perspective>: Provide an interpretation from a specific cultural viewpoint, if applicable.

7. <recurring_themes>: Identify any common dream themes present and their potential significance.

8. <lucid_dreaming_potential>: Suggest techniques the dreamer could use to achieve lucidity if they were to have a similar dream in the future.

9. <artistic_inspiration>: Describe a potential piece of artwork or music that could be generated based on the dream's content and mood.

10. <daily_affirmation>: Create a short, inspiring affirmation related to the dream's main theme or message.

Remember to be creative and original in your interpretations, providing unique insights that go beyond conventional dream analysis. Your goal is to offer the user a rich, multifaceted understanding of their dream that they can reflect on and potentially apply to their waking life."""
    try:
        response = model.generate_content(prompt2)

        # Estimate token counts
        prompt_tokens = len(prompt2) // 4
        response_tokens = len(response.text) // 4

        log_gemini_usage("generate_insight", prompt_tokens, response_tokens)

        # Process the response
        insight = response.text.strip()

        # Save the insight to the database
        dream_insight, created = DreamInsight.objects.update_or_create(
            dream=dream,
            defaults={
                "summary": insight[
                    :1000
                ],  # Assuming summary is the first 1000 characters
                "analysis": insight,
            },
        )

        return Response({"dream_insight": insight, "saved_to_database": True})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_dream_insight(request, dream_id):
    try:
        dream = Dream.objects.get(id=dream_id, user=request.user)
        insight = DreamInsight.objects.filter(dream=dream).first()

        if insight:
            return Response({"has_insight": True, "content": insight.analysis})
        else:
            return Response({"has_insight": False})
    except Dream.DoesNotExist:
        return Response({"error": "Dream not found"}, status=404)
