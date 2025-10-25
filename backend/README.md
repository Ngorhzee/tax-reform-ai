# Nigerian Tax Reform AI Chatbot API (2026)

An AI-powered chatbot API built with FastAPI, LangChain, and Google Gemini to help Nigerian taxpayers understand the 2026 tax reforms and calculate their tax obligations.

## Features

- AI-powered conversational interface using Google Gemini
- Specialized in Nigerian tax law for 2026
- Automatic tax bracket identification based on income
- Step-by-step tax calculation with Nigerian tax brackets
- Information on tax reliefs and allowances
- Session-based conversation history using ConversationBufferMemory
- RESTful API with FastAPI
- Easy integration with frontend applications

## Prerequisites

### Option 1: Local Development
- Python 3.8 or higher
- Google Gemini API key (free tier available)

### Option 2: Docker (Recommended for Production)
- Docker and Docker Compose
- Google Gemini API key (free tier available)

## Getting Your Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file from the example:
```bash
cp .env.example .env
```

6. Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## Docker Deployment

### Using Docker Compose (Recommended)

1. Make sure you have Docker and Docker Compose installed

2. Create a `.env` file with your configuration:
```bash
cp .env.example .env
```

3. Edit `.env` and add your Google API key

4. Build and run the container:
```bash
docker-compose up -d
```

5. Check the logs:
```bash
docker-compose logs -f backend
```

6. Stop the container:
```bash
docker-compose down
```

### Using Docker CLI

1. Build the image:
```bash
docker build -t tax-chatbot-backend .
```

2. Run the container:
```bash
docker run -d \
  --name tax-chatbot \
  -p 8000:8000 \
  --env-file .env \
  tax-chatbot-backend
```

3. Check logs:
```bash
docker logs -f tax-chatbot
```

4. Stop and remove:
```bash
docker stop tax-chatbot
docker rm tax-chatbot
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```http
GET /api/v1/health
```

### Chat with Bot
```http
POST /api/v1/chat
Content-Type: application/json

{
  "message": "I need help with my Nigerian taxes for 2026",
  "session_id": "optional-session-id"
}
```

**Note:**
- Only `message` is required
- `session_id` is optional - omit it to start a new conversation
- The API automatically manages conversation history using ConversationBufferMemory
- Include the `session_id` from the response in subsequent requests to continue the conversation
- The chatbot is specialized in Nigerian tax law for the 2026 tax year

Response:
```json
{
  "response": "Hello! I'd be happy to help you understand your Nigerian tax obligations for 2026...",
  "session_id": "abc-123-def",
  "timestamp": "2025-10-25T12:00:00"
}
```

### Get Session History
```http
GET /api/v1/chat/session/{session_id}
```

### Clear Session
```http
DELETE /api/v1/chat/session/{session_id}
```

## Usage Example

### Using curl

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What tax bracket am I in if I earn ₦2,500,000 per year?"
  }'
```

### Using Python requests

```python
import requests

# Start a new conversation
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "What tax bracket am I in if I earn ₦2,500,000 per year?"
    }
)

data = response.json()
print(f"Bot: {data['response']}")
session_id = data['session_id']
print(f"Session ID: {session_id}")

# Continue the conversation
response2 = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "I am a salaried employee. How much tax will I pay?",
        "session_id": session_id
    }
)

data2 = response2.json()
print(f"Bot: {data2['response']}")
```

### Using JavaScript fetch

```javascript
const response = await fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: "What tax bracket am I in if I earn ₦2,500,000 per year?"
  })
});

const data = await response.json();
console.log('Bot:', data.response);
console.log('Session ID:', data.session_id);
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API route definitions
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Configuration and settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── chatbot_service.py # Chatbot logic with LangChain
├── .dockerignore              # Docker ignore file
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Environment variables template
├── .gitignore
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker build instructions
├── requirements.txt           # Python dependencies
└── README.md
```

## Configuration

Edit the `.env` file to customize:

- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `MODEL_NAME`: Gemini model to use (default: gemini-pro)
- `TEMPERATURE`: Response creativity (0.0-1.0, default: 0.7)
- `MAX_OUTPUT_TOKENS`: Maximum response length (default: 2048)
- `CORS_ORIGINS`: Allowed CORS origins (default: *)

## What the Chatbot Does

The Nigerian Tax Reform AI Chatbot helps taxpayers by:

1. **Identifying tax brackets** - Determines which Nigerian tax bracket users fall into based on their annual income (in Naira)
2. **Calculating tax liability** - Provides step-by-step calculations using the 2026 Nigerian tax brackets:
   - First ₦300,000: 7%
   - Next ₦300,000: 11%
   - Next ₦500,000: 15%
   - Next ₦500,000: 19%
   - Next ₦1,400,000: 21%
   - Above ₦3,200,000: 24%
3. **Explaining tax reliefs** - Information about Consolidated Relief Allowance and other deductions
4. **Clarifying taxable income** - What counts as taxable vs. non-taxable income under Nigerian law
5. **Guiding through scenarios** - Help with PAYE, self-employment, business income, and more
6. **FIRS requirements** - Information about filing deadlines and Federal Inland Revenue Service requirements

The bot asks clarifying questions to better understand each user's unique situation and provides helpful, easy-to-understand guidance specific to Nigerian tax law.

## Important Notes

- This chatbot provides general tax information, not professional tax advice
- Always consult with a qualified tax professional for complex situations
- Session data is stored in memory and will be lost on server restart
- For production use, implement persistent storage for conversation history

## Troubleshooting

### API Key Issues
- Ensure your Google API key is valid and has Gemini API access enabled
- Check that the `.env` file is in the backend root directory
- Verify the key has no extra spaces or quotes

### Import Errors
- Make sure you're in the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change the port: `uvicorn app.main:app --reload --port 8001`
- Or kill the process using port 8000

## License

MIT
