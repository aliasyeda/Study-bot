from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.llm_service import StudyBotService
import logging

router = APIRouter(prefix="/api/chat", tags=["chat"])
logger = logging.getLogger(__name__)

# Create one instance of the bot service
study_bot = StudyBotService()

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint: POST /api/chat
    What it does: Receives user message and returns bot response
    """
    try:
        # Call the main bot function
        response = await study_bot.generate_response(
            user_id=request.user_id,
            message=request.message,
            session_id=request.session_id
        )
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """
    Endpoint: GET /api/chat/history/{session_id}
    What it does: Returns all messages from a conversation
    """
    try:
        history = study_bot.get_chat_history(session_id)
        return {"session_id": session_id, "history": history}
        
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Endpoint: DELETE /api/chat/session/{session_id}
    What it does: Deletes a conversation
    """
    try:
        result = study_bot.collection.delete_one({"session_id": session_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": f"Session {session_id} deleted"}
        
    except Exception as e:
        logger.error(f"Session deletion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))