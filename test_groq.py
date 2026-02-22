import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Test the connection
try:
    llm = ChatGroq(
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile" 
    )
    
    response = llm.invoke("Say 'Hello, my API key works!'")
    print("✅ SUCCESS! Response:", response.content)
    
except Exception as e:
    print("❌ ERROR:", e)