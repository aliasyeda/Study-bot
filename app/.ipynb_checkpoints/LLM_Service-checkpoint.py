from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from app.config import settings
from app.database import MongoDB
from app.models import Message, ChatSession
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

class StudyBotService:
    def __init__(self):
        """Initialize the Study Bot"""
        # Connect to Groq's AI
        self.llm = ChatGroq(
            temperature=0.7,  # How creative the responses are (0=strict, 1=creative)
            groq_api_key=settings.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile"  # Which AI model to use
        )
        self.system_prompt = settings.SYSTEM_PROMPT
        self.db = MongoDB.database
        self.collection = self.db[settings.COLLECTION_NAME]
    
    def get_or_create_session(self, user_id: str, session_id: str = None) -> str:
        """Get existing session or create new one"""
        if not session_id:
            # Generate new unique ID for new conversation
            session_id = str(uuid.uuid4())
            
        # Check if this session already exists
        existing = self.collection.find_one({"session_id": session_id})
        
        if not existing:
            # Create new session in database
            session = ChatSession(
                session_id=session_id,
                user_id=user_id,
                messages=[]
            )
            self.collection.insert_one(session.dict())
            
        return session_id
    
    def get_chat_history(self, session_id: str, limit: int = 10) -> list:
        """Get last 10 messages from database for context"""
        session = self.collection.find_one({"session_id": session_id})
        
        if not session:
            return []
        
        # Get only the most recent messages
        messages = session.get("messages", [])
        return messages[-limit:] if messages else []
    
    def save_message(self, session_id: str, role: str, content: str):
        """Save a message to MongoDB"""
        message = Message(role=role, content=content)
        
        # Add message to session and update timestamp
        self.collection.update_one(
            {"session_id": session_id},
            {
                "$push": {"messages": message.dict()},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
    
    def format_history_for_llm(self, history: list) -> list:
        """Convert database history to format AI understands"""
        # Start with system instructions
        formatted = [SystemMessage(content=self.system_prompt)]
        
        # Add each message from history
        for msg in history:
            if msg["role"] == "user":
                formatted.append(HumanMessage(content=msg["content"]))
            else:
                formatted.append(AIMessage(content=msg["content"]))
        
        return formatted
    
    async def generate_response(self, user_id: str, message: str, session_id: str = None) -> dict:
        """Main function - generates bot response with context"""
        try:
            # Step 1: Get or create session
            session_id = self.get_or_create_session(user_id, session_id)
            
            # Step 2: Get chat history
            history = self.get_chat_history(session_id)
            
            # Step 3: Prepare messages for AI (history + new question)
            messages = self.format_history_for_llm(history)
            messages.append(HumanMessage(content=message))
            
            # Step 4: Get response from AI
            response = await self.llm.ainvoke(messages)
            
            # Step 5: Save both messages to database
            self.save_message(session_id, "user", message)
            self.save_message(session_id, "assistant", response.content)
            
            # Step 6: Return response to user
            return {
                "session_id": session_id,
                "user_id": user_id,
                "message": message,
                "response": response.content,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise