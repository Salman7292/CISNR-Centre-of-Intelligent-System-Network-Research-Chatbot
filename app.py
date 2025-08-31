# app.py
from flask import Flask, request, jsonify, render_template
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CISNRRAGSystem:
    def __init__(self):
        try:
            # Load environment variables
            self.google_api_key = os.getenv("GOOGLE_API_KEY")
            self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
            self.index_name = os.getenv("PINECONE_INDEX_NAME", "ncai")
            
            if not self.google_api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is not set")
            if not self.pinecone_api_key:
                raise ValueError("PINECONE_API_KEY environment variable is not set")
            
            # Initialize embeddings
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=self.google_api_key
            )
            
            # Initialize vector store
            self.vectorstore = PineconeVectorStore.from_existing_index(
                index_name=self.index_name,
                embedding=self.embeddings
            )
            
            # Initialize LLM
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.3,
                google_api_key=self.google_api_key,
                max_tokens=1000
            )
            
            # Create prompt template
            self.prompt = PromptTemplate.from_template("""
You are an AI assistant representing CISNR (Centre of Intelligent System & Network Research) at UET Peshawar.
Your role is to provide information about CISNR's work and mission based ONLY on the provided context.

IMPORTANT INSTRUCTIONS:
1. When asked about yourself, respond as a representative of CISNR
2. Never mention that you are a language model or AI assistant from Google
3. Only use information from the provided context below
4. If the question is not related to CISNR, politely decline to answer
5. For irrelevant questions, use this exact response structure:
   - Politely acknowledge you can't answer
   - State that you specialize in CISNR-related topics
   - Suggest asking about CISNR's work instead
6. Keep responses professional, informative, and concise (3-5 sentences)
7. Use proper formatting with line breaks for readability

Context about CISNR:
{context}

Question: {question}

Answer in a clear, professional manner:
""")
            
            # Create retriever
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 6, "include_metadata": True}
            )
            
            # Create chain
            self.chain = (
                {
                    "context": self.retriever | self.format_docs,
                    "question": RunnablePassthrough()
                }
                | self.prompt
                | self.llm
                | StrOutputParser()
            )
            
            logger.info("CISNR RAG System initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {str(e)}")
            raise
    
    def format_docs(self, docs):
        formatted_docs = []
        for i, doc in enumerate(docs):
            content = doc.page_content.strip()
            metadata = doc.metadata
            source_info = f"[Source: {metadata.get('source', 'unknown')} | Score: {metadata.get('score', 'N/A'):.3f}]" if metadata else ""
            formatted_docs.append(f"Document {i+1}:\n{content}\n{source_info}")
        return "\n\n".join(formatted_docs)
    
    def query(self, question, user_context=None):
        try:
            # Add user context to question if available
            enhanced_question = question
            if user_context:
                enhanced_question = f"[User: {user_context['role']}] {question}"
            
            result = self.chain.invoke(enhanced_question)
            return result
            
        except Exception as e:
            logger.error(f"Error processing query '{question}': {str(e)}")
            return """I apologize, but I'm currently experiencing technical difficulties. 
Please try your question again later. For immediate assistance, 
contact the CISNR directorate at cisnr@uetpeshawar.edu.pk."""

# Initialize RAG system
try:
    rag_system = CISNRRAGSystem()
except Exception as e:
    logger.error(f"Failed to initialize RAG system: {str(e)}")
    rag_system = None

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    if not rag_system:
        return jsonify({
            'error': 'RAG system is not available',
            'response': 'I apologize, but the research assistant system is currently unavailable. Please try again later.'
        }), 503
    
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Extract user context if available
        user_context = {
            'role': data.get('role', 'researcher'),
            'user_id': data.get('user_id', 'unknown'),
            'session_id': data.get('session_id', 'unknown')
        }
        
        logger.info(f"Received message from {user_context['user_id']}: {message}")
        
        # Get response from RAG system
        response = rag_system.query(message, user_context)
        
        return jsonify({
            'question': message,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'source': 'cisnr-rag-system'
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'response': 'I apologize, but I encountered an error processing your request. Please try again.'
        }), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    status = 'healthy' if rag_system else 'degraded'
    code = 200 if rag_system else 503
    
    return jsonify({
        'status': status,
        'service': 'CISNR Research Assistant',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'dependencies': {
            'rag_system': rag_system is not None,
            'google_api': bool(os.getenv("GOOGLE_API_KEY")),
            'pinecone': bool(os.getenv("PINECONE_API_KEY"))
        }
    }), code

@app.route('/api/resources')
def resources():
    """API endpoint for research resources"""
    resources = [
        {
            "title": "Research Publications",
            "url": "/publications",
            "icon": "file-pdf",
            "category": "academic",
            "description": "Access our latest research papers and publications"
        },
        {
            "title": "Academic Programs",
            "url": "/programs",
            "icon": "graduation-cap",
            "category": "education",
            "description": "Learn about our academic offerings and collaborations"
        },
        {
            "title": "Research Team",
            "url": "/team",
            "icon": "users",
            "category": "people",
            "description": "Meet our researchers and faculty members"
        },
        {
            "title": "Facilities & Equipment",
            "url": "/facilities",
            "icon": "microscope",
            "category": "infrastructure",
            "description": "Explore our laboratories and research equipment"
        }
    ]
    
    return jsonify({
        'resources': resources,
        'count': len(resources),
        'last_updated': datetime.now().strftime("%Y-%m-%d")
    })

if __name__ == '__main__':
    from datetime import datetime
    
    # Set environment variables for Pinecone if not already set
    if not os.getenv("PINECONE_API_KEY"):
        os.environ["PINECONE_API_KEY"] = "your-pinecone-api-key-here"
    
    # Run the application
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    app.run(debug=debug, host='0.0.0.0', port=port)