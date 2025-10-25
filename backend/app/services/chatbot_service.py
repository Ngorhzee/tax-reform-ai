from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain.memory import ConversationBufferMemory
from typing import Dict, List
import uuid
from app.core.config import settings


class TaxChatbotService:
    """Service for handling tax-related chatbot conversations using Google Gemini"""

    def __init__(self):
        """Initialize the chatbot with Google Gemini and LangChain"""
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=settings.TEMPERATURE,
            max_output_tokens=settings.MAX_OUTPUT_TOKENS,
            convert_system_message_to_human=True,
        )

        # System prompt for Nigerian tax assistance
        self.system_prompt = """You are a helpful and knowledgeable tax assistant AI specialized in Nigerian tax law for the 2026 tax year. Your role is to help Nigerian taxpayers understand their tax obligations under the new 2026 tax reforms.

NIGERIAN PERSONAL INCOME TAX BRACKETS FOR 2026:
The Nigerian Personal Income Tax uses a progressive tax system with the following brackets:

1. First ₦300,000 of annual income: 7%
2. Next ₦300,000 (₦300,001 - ₦600,000): 11%
3. Next ₦500,000 (₦600,001 - ₦1,100,000): 15%
4. Next ₦500,000 (₦1,100,001 - ₦1,600,000): 19%
5. Next ₦1,400,000 (₦1,600,001 - ₦3,000,000): 21%
6. Above ₦3,200,000: 24%

RELIEF ALLOWANCES (2026):
- Consolidated Relief Allowance: Higher of ₦200,000 or 1% of gross income + 20% of gross income
- This is deducted from gross income to arrive at taxable income

Key responsibilities:
1. Help users identify their tax bracket based on their annual income in Nigerian Naira (₦)
2. Calculate approximate tax liability using the Nigerian tax brackets
3. Explain taxable and non-taxable income under Nigerian law
4. Guide users through common tax scenarios (employment, self-employment, business income, etc.)
5. Provide information about available tax reliefs and allowances in Nigeria
6. Explain tax filing deadlines and FIRS (Federal Inland Revenue Service) requirements
7. Clarify differences between PAYE (Pay As You Earn) and self-assessment

Important guidelines:
- Always use Nigerian Naira (₦) as the currency
- Reference Nigerian tax laws and the 2026 tax reforms
- Always be clear that you're providing general information, not professional tax advice
- Ask clarifying questions one or two at a time to understand the user's situation
- Use simple language - avoid complex tax jargon where possible
- Encourage users to consult with a qualified Nigerian tax professional or registered tax consultant for complex situations
- Be patient and supportive, as taxes can be confusing
- When calculating tax, show your work step by step so users understand

Start by greeting the user warmly and asking about their income and tax situation to help determine their tax bracket."""

        # Memory storage for conversations (in production, use a database)
        self.memories: Dict[str, ConversationBufferMemory] = {}

    async def get_response(self, user_message: str, session_id: str = None) -> tuple[str, str]:
        """
        Get a response from the chatbot

        Args:
            user_message: The user's message
            session_id: Optional session ID for conversation continuity

        Returns:
            Tuple of (response_text, session_id)
        """
        # Generate or use existing session ID
        if not session_id:
            session_id = str(uuid.uuid4())

        # Get or create memory for this session
        if session_id not in self.memories:
            self.memories[session_id] = ConversationBufferMemory(return_messages=True)

        memory = self.memories[session_id]

        # Build message list with system prompt and history
        messages = [SystemMessage(content=self.system_prompt)]

        # Add conversation history from memory
        chat_memory = memory.chat_memory.messages
        messages.extend(chat_memory)

        # Add current user message
        messages.append(HumanMessage(content=user_message))

        # Get response from LLM
        response = await self.llm.ainvoke(messages)

        # Save to memory
        memory.chat_memory.add_user_message(user_message)
        memory.chat_memory.add_ai_message(response.content)

        return response.content, session_id

    def clear_session(self, session_id: str) -> bool:
        """Clear a conversation session"""
        if session_id in self.memories:
            del self.memories[session_id]
            return True
        return False

    def get_session_history(self, session_id: str) -> List[BaseMessage]:
        """Get conversation history for a session"""
        if session_id in self.memories:
            return self.memories[session_id].chat_memory.messages
        return []
