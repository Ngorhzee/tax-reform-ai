from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import uuid
from app.core.config import settings
from app.models.schemas import Message


class TaxChatbotService:
    """Service for handling tax-related chatbot conversations using Google Gemini"""

    def __init__(self):
        """Initialize the chatbot with Google Gemini and LangChain"""
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=settings.TEMPERATURE,
            max_output_tokens=settings.MAX_OUTPUT_TOKENS,
        )

        # System prompt for tax assistance
        self.system_prompt = """You are a helpful and knowledgeable tax assistant AI. Your role is to help users understand their tax obligations and guide them through the tax filing process.

Key responsibilities:
1. Ask clarifying questions to understand the user's tax situation
2. Help users identify their tax bracket based on their income
3. Explain what income and expenses are taxable or deductible
4. Guide users through common tax scenarios (employment income, self-employment, investments, etc.)
5. Provide information about tax credits and deductions they may be eligible for
6. Help users understand tax deadlines and filing requirements

Important guidelines:
- Always be clear that you're providing general information, not professional tax advice
- Ask one or two questions at a time to avoid overwhelming the user
- Use simple, jargon-free language when possible
- If uncertain about specific tax laws, acknowledge limitations
- Encourage users to consult with a tax professional for complex situations
- Be patient and supportive, as taxes can be stressful

Start by greeting the user warmly and asking about their tax situation to better assist them."""

        # Conversation sessions storage (in production, use a database)
        self.sessions: Dict[str, List[Message]] = {}

    def _convert_messages_to_langchain(self, messages: List[Message]) -> List:
        """Convert Message objects to LangChain message format"""
        langchain_messages = [SystemMessage(content=self.system_prompt)]

        for msg in messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))

        return langchain_messages

    async def get_response(
        self, user_message: str, session_id: str = None, chat_history: List[Message] = None
    ) -> tuple[str, str]:
        """
        Get a response from the chatbot

        Args:
            user_message: The user's message
            session_id: Optional session ID for conversation continuity
            chat_history: Optional previous conversation history

        Returns:
            Tuple of (response_text, session_id)
        """
        # Generate or use existing session ID
        if not session_id:
            session_id = str(uuid.uuid4())

        # Use provided chat history or get from session storage
        if chat_history is None:
            chat_history = self.sessions.get(session_id, [])

        # Convert messages to LangChain format
        messages = self._convert_messages_to_langchain(chat_history)

        # Add current user message
        messages.append(HumanMessage(content=user_message))

        # Get response from LLM
        response = await self.llm.ainvoke(messages)

        # Store conversation in session
        chat_history.append(Message(role="user", content=user_message))
        chat_history.append(Message(role="assistant", content=response.content))
        self.sessions[session_id] = chat_history

        return response.content, session_id

    def clear_session(self, session_id: str) -> bool:
        """Clear a conversation session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def get_session_history(self, session_id: str) -> List[Message]:
        """Get conversation history for a session"""
        return self.sessions.get(session_id, [])
