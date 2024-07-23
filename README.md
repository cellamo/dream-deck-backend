# Dream Deck

Dream Deck is a Django-based backend API for a dream journaling and analysis application. It allows users to record their dreams, analyze them, and gain insights into their subconscious mind.

## Features

- User authentication and registration
- CRUD operations for dreams
- Emotion and theme tagging for dreams
- AI-powered dream analysis and insights
- Suggestion system for dream titles, themes, and emotions
- Cultural interpretations of dreams
- Lucid dreaming progress tracking
- Dream challenges and daily tasks
- Collaborative dreaming

## API Endpoints

- `/api/v1/dreams/`: Dream management
- `/api/v1/emotions/`: Emotion management
- `/api/v1/themes/`: Theme management
- `/api/v1/suggest-themes/`: AI-powered theme suggestions
- `/api/v1/suggest-emotions/`: AI-powered emotion suggestions
- `/api/v1/suggest-title/`: AI-powered title suggestions
- `/api/v1/generate-dream-insight/`: AI-powered dream analysis
- `/api/v1/dreams/<int:dream_id>/check-insight/`: Check for existing dream insights

## Authentication

The API uses JSON Web Tokens (JWT) for authentication. To obtain a token, use the following endpoints:

- `/api/v1/token/`: Obtain JWT token
- `/api/v1/token/refresh/`: Refresh JWT token
- `/api/v1/token/verify/`: Verify JWT token

## Models

- User: Custom user model with additional fields
- Dream: Main model for storing dream entries
- Emotion: Represents different emotions
- Theme: Represents different themes
- DreamInsight: Stores AI-generated insights for dreams
- (Other models for challenges, lucid dreaming progress, etc.)

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (including Gemini API key)
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

### Database configuration
DATABASE_URL=your_database_url_here
DIRECT_URL=your_direct_database_url_here

### API Keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here


> **Note:** Replace the placeholder values with your actual configuration. Never commit the `.env` file with real values to version control.

## Technologies Used

- Django
- Django Rest Framework
- Google's Generative AI (Gemini)
- PostgreSQL (recommended for production)

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE).