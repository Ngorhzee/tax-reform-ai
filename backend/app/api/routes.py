from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services.chatbot_service import TaxChatbotService

router = APIRouter()

# Initialize chatbot service
chatbot_service = TaxChatbotService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Tax Reform AI Chatbot is running"
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for tax assistance

    Accepts a user message and optional conversation history,
    returns AI assistant's response
    """
    try:
        response_text, session_id = await chatbot_service.get_response(
            user_message=request.message,
            session_id=request.session_id,
            chat_history=request.chat_history
        )

        return ChatResponse(
            response=response_text,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.delete("/chat/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a conversation session"""
    success = chatbot_service.clear_session(session_id)

    if success:
        return {"message": f"Session {session_id} cleared successfully"}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )


@router.get("/chat/session/{session_id}")
async def get_session_history(session_id: str):
    """Get conversation history for a session"""
    history = chatbot_service.get_session_history(session_id)

    if history:
        return {"session_id": session_id, "history": history}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )
