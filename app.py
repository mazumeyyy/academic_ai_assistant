"""
Academic AI Assistant - Main Application
A complete AI assistant for academic purposes using Ollama
"""

# pyrefly: ignore [missing-import]
import streamlit as st
import os
import time
from utils.document_processor import DocumentProcessor
from utils.vector_store import VectorStoreHandler
from utils.llm_handler import LLMHandler
from utils.quiz_generator import QuizGenerator

# Page configuration
st.set_page_config(
    page_title="Academic AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Theme toggle function
def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Get current theme
is_dark = st.session_state.theme == 'dark'

# Academic-themed CSS with Dark/Light Mode
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&family=Source+Sans+Pro:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    /* ===== CSS VARIABLES FOR THEMES ===== */
    :root {{
        /* Light Mode - Academic Classic */
        --bg-primary: {'#1a1f2e' if is_dark else '#faf9f7'};
        --bg-secondary: {'#242b3d' if is_dark else '#ffffff'};
        --bg-tertiary: {'#2d3548' if is_dark else '#f5f3f0'};
        --bg-gradient: {'linear-gradient(135deg, #1a1f2e 0%, #2d3548 100%)' if is_dark else 'linear-gradient(135deg, #faf9f7 0%, #e8e4df 100%)'};
        
        --text-primary: {'#e8e6e3' if is_dark else '#2c3e50'};
        --text-secondary: {'#b0aaa0' if is_dark else '#5a6c7d'};
        --text-muted: {'#7a7570' if is_dark else '#8b9aa8'};
        
        --accent-primary: {'#6b8cce' if is_dark else '#1e5f74'};
        --accent-secondary: {'#8fa5d4' if is_dark else '#2a7f62'};
        --accent-gold: {'#d4a574' if is_dark else '#c9a227'};
        --accent-burgundy: {'#b87a7a' if is_dark else '#8b2635'};
        
        --border-color: {'#3d4556' if is_dark else '#d4cfc7'};
        --border-light: {'#2d3548' if is_dark else '#e8e4df'};
        
        --shadow-sm: {'0 2px 8px rgba(0,0,0,0.3)' if is_dark else '0 2px 8px rgba(44,62,80,0.08)'};
        --shadow-md: {'0 4px 20px rgba(0,0,0,0.4)' if is_dark else '0 4px 20px rgba(44,62,80,0.12)'};
        --shadow-lg: {'0 8px 40px rgba(0,0,0,0.5)' if is_dark else '0 8px 40px rgba(44,62,80,0.15)'};
        
        --success: {'#5cb85c' if is_dark else '#2a7f62'};
        --warning: {'#f0ad4e' if is_dark else '#c9a227'};
        --error: {'#d9534f' if is_dark else '#8b2635'};
        --info: {'#6b8cce' if is_dark else '#1e5f74'};
        
        --sidebar-bg: {'linear-gradient(180deg, #1e2636 0%, #2a3447 100%)' if is_dark else 'linear-gradient(180deg, #1e5f74 0%, #2a7f62 100%)'};
    }}
    
    /* ===== GLOBAL RESET & FONTS ===== */
    * {{
        font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Merriweather', Georgia, serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    
    code, pre, .stCode {{
        font-family: 'Fira Code', monospace;
    }}
    
    /* ===== MAIN APP CONTAINER ===== */
    [data-testid="stAppViewContainer"] {{
        background: var(--bg-gradient);
    }}
    
    [data-testid="stAppViewContainer"] > div {{
        background: transparent;
    }}
    
    .main .block-container {{
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 2rem 3rem;
        margin: 1rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
    }}
    
    /* ===== HEADER STYLING ===== */
    .main-header {{
        font-size: 2.8rem;
        font-weight: 900;
        font-family: 'Merriweather', Georgia, serif;
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-gold) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
        animation: fadeInDown 0.8s ease-out;
        text-shadow: none;
    }}
    
    .sub-header {{
        font-size: 1.2rem;
        color: var(--accent-gold);
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 400;
        font-style: italic;
        letter-spacing: 1px;
        opacity: 0.9;
    }}
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg);
        border-right: 3px solid var(--accent-gold);
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: #ffffff;
    }}
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] [role="heading"] {{
        color: #ffffff !important;
        font-family: 'Merriweather', Georgia, serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{
        color: rgba(255,255,255,0.9) !important;
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: rgba(255,255,255,0.95) !important;
        font-weight: 500;
    }}
    
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.2);
        margin: 1.5rem 0;
    }}
    
    /* Sidebar Info Box */
    [data-testid="stSidebar"] [data-testid="stAlert"] {{
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }}
    
    /* ===== THEME TOGGLE BUTTON ===== */
    .theme-toggle {{
        background: {'rgba(255,255,255,0.15)' if is_dark else 'rgba(0,0,0,0.1)'};
        border: 2px solid {'rgba(255,255,255,0.3)' if is_dark else 'rgba(255,255,255,0.5)'};
        border-radius: 50px;
        padding: 8px 20px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 10px 0;
    }}
    
    .theme-toggle:hover {{
        background: {'rgba(255,255,255,0.25)' if is_dark else 'rgba(0,0,0,0.2)'};
        transform: scale(1.02);
    }}
    
    /* ===== MAIN CONTENT HEADERS ===== */
    .stMarkdown h1 {{
        color: var(--accent-primary);
        font-size: 2rem;
        border-bottom: 3px solid var(--accent-gold);
        padding-bottom: 0.75rem;
        margin-bottom: 1.5rem;
        font-family: 'Merriweather', Georgia, serif;
    }}
    
    .stMarkdown h2 {{
        color: var(--accent-primary);
        font-size: 1.5rem;
        margin-top: 2rem;
        padding-left: 15px;
        border-left: 4px solid var(--accent-gold);
    }}
    
    .stMarkdown h3 {{
        color: var(--accent-secondary);
        font-size: 1.25rem;
    }}
    
    .stMarkdown p {{
        color: var(--text-primary);
        line-height: 1.7;
        font-size: 1.05rem;
    }}
    
    /* ===== BUTTONS - Academic Style ===== */
    .stButton > button {{
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        text-transform: none;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
        filter: brightness(1.1);
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px);
    }}
    
    /* Primary Button Variant */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--accent-burgundy) 0%, var(--accent-primary) 100%);
        box-shadow: 0 4px 15px rgba(139, 38, 53, 0.3);
    }}
    
    /* ===== INPUT FIELDS - Scholarly Look ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: var(--bg-secondary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px {'rgba(107, 140, 206, 0.2)' if is_dark else 'rgba(30, 95, 116, 0.15)'} !important;
        outline: none !important;
    }}
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: var(--text-muted) !important;
        font-style: italic;
    }}
    
    /* ===== SELECT BOX ===== */
    .stSelectbox > div > div {{
        background-color: var(--bg-secondary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 10px !important;
    }}
    
    .stSelectbox [data-baseweb="select"] {{
        background-color: var(--bg-secondary) !important;
    }}
    
    /* ===== SLIDER ===== */
    .stSlider > div > div > div {{
        background-color: var(--border-color) !important;
    }}
    
    .stSlider [data-baseweb="slider"] div {{
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
    }}
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploaderDropzone"] {{
        background: var(--bg-tertiary) !important;
        border: 3px dashed var(--accent-primary) !important;
        border-radius: 16px !important;
        transition: all 0.3s ease;
        padding: 2rem !important;
    }}
    
    [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: var(--accent-gold) !important;
        background: {'rgba(107, 140, 206, 0.1)' if is_dark else 'rgba(30, 95, 116, 0.05)'} !important;
        transform: scale(1.01);
    }}
    
    [data-testid="stFileUploaderDropzone"] p {{
        color: var(--text-secondary) !important;
    }}
    
    /* ===== ALERT BOXES ===== */
    [data-testid="stAlert"] {{
        border-radius: 12px !important;
        border-left: 5px solid !important;
        animation: slideInLeft 0.4s ease-out;
    }}
    
    /* Success Alert */
    .stSuccess, [data-testid="stAlert"]:has(.success) {{
        background: {'rgba(92, 184, 92, 0.15)' if is_dark else 'rgba(42, 127, 98, 0.08)'} !important;
        border-left-color: var(--success) !important;
    }}
    
    /* Error Alert */
    .stError {{
        background: {'rgba(217, 83, 79, 0.15)' if is_dark else 'rgba(139, 38, 53, 0.08)'} !important;
        border-left-color: var(--error) !important;
    }}
    
    /* Warning Alert */
    .stWarning {{
        background: {'rgba(240, 173, 78, 0.15)' if is_dark else 'rgba(201, 162, 39, 0.08)'} !important;
        border-left-color: var(--warning) !important;
    }}
    
    /* Info Alert */
    .stInfo {{
        background: {'rgba(107, 140, 206, 0.15)' if is_dark else 'rgba(30, 95, 116, 0.08)'} !important;
        border-left-color: var(--info) !important;
        border: none !important;
        border-left: 5px solid var(--info) !important;
        border-radius: 12px !important;
    }}
    
    /* ===== METRICS ===== */
    [data-testid="stMetric"] {{
        background: var(--bg-tertiary);
        border: 2px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }}
    
    [data-testid="stMetric"]:hover {{
        border-color: var(--accent-primary);
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }}
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: var(--accent-primary);
        font-family: 'Merriweather', Georgia, serif;
        font-weight: 700;
    }}
    
    [data-testid="stMetric"] [data-testid="stMetricLabel"] {{
        color: var(--text-secondary);
    }}
    
    /* ===== CHAT MESSAGES ===== */
    [data-testid="stChatMessage"] {{
        background: var(--bg-tertiary);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
    }}
    
    [data-testid="stChatMessage"][data-role="user"] {{
        background: {'rgba(107, 140, 206, 0.1)' if is_dark else 'rgba(30, 95, 116, 0.05)'};
        border-left: 4px solid var(--accent-primary);
    }}
    
    [data-testid="stChatMessage"][data-role="assistant"] {{
        background: {'rgba(42, 127, 98, 0.1)' if is_dark else 'rgba(42, 127, 98, 0.05)'};
        border-left: 4px solid var(--accent-secondary);
    }}
    
    /* Chat Input */
    [data-testid="stChatInput"] {{
        border: 2px solid var(--border-color) !important;
        border-radius: 25px !important;
        background: var(--bg-secondary) !important;
    }}
    
    [data-testid="stChatInput"]:focus-within {{
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px {'rgba(107, 140, 206, 0.2)' if is_dark else 'rgba(30, 95, 116, 0.15)'} !important;
    }}
    
    /* ===== RADIO BUTTONS ===== */
    .stRadio > div {{
        gap: 0.75rem;
    }}
    
    .stRadio label {{
        color: var(--text-primary) !important;
        font-weight: 500;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }}
    
    .stRadio label:hover {{
        background: var(--bg-tertiary);
    }}
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        background: var(--bg-tertiary) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-weight: 600;
        border: 1px solid var(--border-color);
    }}
    
    .streamlit-expanderContent {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 10px 10px;
    }}
    
    /* ===== DIVIDER ===== */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
        margin: 2.5rem 0;
        opacity: 0.6;
    }}
    
    /* ===== LABELS ===== */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stSlider label,
    .stRadio label,
    .stCheckbox label {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        font-family: 'Source Sans Pro', sans-serif !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-tertiary);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 10px;
        border: 2px solid var(--bg-tertiary);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, var(--accent-secondary), var(--accent-primary));
    }}
    
    /* ===== SPINNER ===== */
    .stSpinner > div {{
        border-top-color: var(--accent-primary) !important;
    }}
    
    /* ===== ACADEMIC DECORATIVE ELEMENTS ===== */
    .academic-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, var(--accent-gold), {'#b8956a' if is_dark else '#a88a1f'});
        color: {'#1a1f2e' if is_dark else '#ffffff'};
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        box-shadow: var(--shadow-sm);
    }}
    
    .feature-card {{
        background: var(--bg-tertiary);
        border: 2px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }}
    
    .feature-card:hover {{
        border-color: var(--accent-primary);
        box-shadow: var(--shadow-md);
        transform: translateY(-4px);
    }}
    
    /* ===== FOOTER ===== */
    .footer-text {{
        text-align: center;
        color: var(--text-muted);
        font-size: 0.9rem;
        padding: 2rem 0;
        border-top: 1px solid var(--border-light);
        margin-top: 3rem;
    }}
    
    .footer-text a {{
        color: var(--accent-primary);
        text-decoration: none;
        font-weight: 600;
    }}
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            opacity: 1;
        }}
        50% {{
            opacity: 0.7;
        }}
    }}
    
    /* ===== RESPONSIVE ADJUSTMENTS ===== */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2rem;
        }}
        
        .sub-header {{
            font-size: 1rem;
        }}
        
        .main .block-container {{
            padding: 1rem 1.5rem;
            margin: 0.5rem;
        }}
    }}
    
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []

# Sidebar Configuration
st.sidebar.title("🎓 Academic AI Assistant")
st.sidebar.caption("by Avinash")

# Theme Toggle
st.sidebar.markdown("---")
theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
theme_label = "Switch to Dark Mode" if st.session_state.theme == 'light' else "Switch to Light Mode"
if st.sidebar.button(f"{theme_icon} {theme_label}", key="theme_toggle", use_container_width=True):
    toggle_theme()
    st.rerun()

# Feature selection
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Features")
feature = st.sidebar.radio(
    "Choose what you want to do:",
    [
        "📖 Document Q&A",
        "📝 Summarize Text",
        "💡 Explain Concept",
        "❓ Generate Quiz",
        "💬 Chat with AI"
    ]
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info("""
    ### 📌 How to Use:
    
    1. **Document Q&A**: Upload PDFs/text files and ask questions
    2. **Summarize**: Get quick summaries of long texts
    3. **Explain**: Understand complex concepts easily
    4. **Quiz**: Test your knowledge
    5. **Chat**: Have a conversation with AI
    
    ### 💡 Tips:-
    - Be specific with your questions
    - Upload relevant study materials
    - Try different features for best learning
""")

# Main Content Area
st.markdown('<h1 class="main-header">🎓 Academic AI Assistant by Avinash</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">भविष्यको शिक्षा, एआईको साथ।</p>', unsafe_allow_html=True)

# Initialize handlers (only once)
@st.cache_resource
def initialize_handlers():
    """Initialize all handlers with caching"""
    doc_processor = DocumentProcessor()
    vector_handler = VectorStoreHandler()
    llm_handler = LLMHandler(model_name="llama3.2:3b")
    quiz_gen = QuizGenerator(model_name="llama3.2:3b")
    return doc_processor, vector_handler, llm_handler, quiz_gen

doc_processor, vector_handler, llm_handler, quiz_gen = initialize_handlers()

# ================== FEATURE 1: DOCUMENT Q&A ==================
if feature == "📖 Document Q&A":
    st.header("📖 Document Question & Answer")
    st.markdown("Upload your study materials and ask questions about them!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Upload your documents (PDF or TXT)",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload lecture notes, textbooks, or any study material"
        )
    
    with col2:
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
            for file in uploaded_files:
                st.write(f"📄 {file.name}")
    
    if uploaded_files:
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing your documents... This may take a minute ⏳"):
                try:
                    # Create documents directory if it doesn't exist
                    os.makedirs("./data/documents", exist_ok=True)
                    
                    # Save uploaded files
                    file_paths = []
                    for uploaded_file in uploaded_files:
                        file_path = f"./data/documents/{uploaded_file.name}"
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        file_paths.append(file_path)
                        st.session_state.processed_files.append(uploaded_file.name)
                    
                    # Process documents
                    documents = doc_processor.process_multiple_files(file_paths)
                    
                    if documents:
                        # Create vector store
                        st.session_state.vectorstore = vector_handler.create_vectorstore(documents)
                        st.session_state.qa_chain = llm_handler.create_qa_chain(st.session_state.vectorstore)
                        
                        st.success(f"""
                        ✅ **Success!** Processed {len(documents)} chunks from your documents.
                        
                        You can now ask questions below! 👇
                        """)
                    else:
                        st.error("❌ No content could be extracted from the files. Please check your documents.")
                
                except Exception as e:
                    st.error(f"❌ Error processing documents: {str(e)}")
    
    # Q&A Interface
    if st.session_state.qa_chain:
        st.markdown("---")
        st.subheader("💭 Ask Questions About Your Documents")
        
        question = st.text_input(
            "What would you like to know?",
            placeholder="e.g., What is the main topic discussed in this document?",
            key="qa_input"
        )
        
        if st.button("🔍 Get Answer", type="primary") and question:
            with st.spinner("Thinking... 🤔"):
                start_time = time.time()
                answer = llm_handler.ask_question(st.session_state.qa_chain, question)
                end_time = time.time()
                
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "time": end_time - start_time
                })
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.subheader("📜 Conversation History")
            
            for idx, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.container():
                    st.markdown(f"**Q{len(st.session_state.chat_history) - idx}:** {chat['question']}")
                    st.info(f"**Answer:** {chat['answer']}")
                    st.caption(f"⏱️ Response time: {chat['time']:.2f}s")
                    st.markdown("---")
            
            if st.button("🗑️ Clear History"):
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.info("👆 Upload and process documents first to start asking questions!")

#  FEATURE 2: SUMMARIZE TEXT 
elif feature == "📝 Summarize Text":
    st.header("📝 Text Summarization")
    st.markdown("Get concise summaries of long texts!")
    
    text_input = st.text_area(
        "Paste the text you want to summarize:",
        height=300,
        placeholder="Paste your article, lecture notes, or any text here...",
        help="Works best with texts between 500-5000 words"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.slider(
            "Target summary length (words)",
            min_value=50,
            max_value=500,
            value=200,
            step=50
        )
    
    with col2:
        st.metric("Input Length", f"{len(text_input.split())} words")
    
    if st.button("✨ Generate Summary", type="primary") and text_input:
        if len(text_input.split()) < 50:
            st.warning("⚠️ Text is too short to summarize. Please provide at least 50 words.")
        else:
            with st.spinner("Creating summary... ✍️"):
                start_time = time.time()
                summary = llm_handler.summarize_text(text_input, summary_length)
                end_time = time.time()
                
                st.markdown("---")
                st.subheader("📋 Summary")
                st.success(summary)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Summary Length", f"{len(summary.split())} words")
                with col2:
                    st.metric("Time Taken", f"{end_time - start_time:.2f}s")

#  FEATURE 3: EXPLAIN CONCEPT 
elif feature == "💡 Explain Concept":
    st.header("💡 Concept Explainer")
    st.markdown("Get clear explanations of complex concepts!")
    
    concept = st.text_input(
        "What concept would you like to understand?",
        placeholder="e.g., Machine Learning, Photosynthesis, Quantum Physics...",
        help="Enter any academic concept or topic"
    )
    
    # Predefined quick concepts
    st.markdown("**Quick Examples:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🧠 Neural Networks"):
            concept = "Neural Networks"
    with col2:
        if st.button("🔬 DNA Replication"):
            concept = "DNA Replication"
    with col3:
        if st.button("📊 Statistics"):
            concept = "Statistical Significance"
    with col4:
        if st.button("⚛️ Atoms"):
            concept = "Atomic Structure"
    
    if st.button("🎯 Explain", type="primary") and concept:
        with st.spinner(f"Explaining {concept}... 📚"):
            start_time = time.time()
            explanation = llm_handler.explain_concept(concept)
            end_time = time.time()
            
            st.markdown("---")
            st.subheader(f"📖 Explanation: {concept}")
            st.info(explanation)
            st.caption(f"⏱️ Generated in {end_time - start_time:.2f}s")

#  FEATURE 4: GENERATE QUIZ 
elif feature == "❓ Generate Quiz":
    st.header("❓ Quiz Generator")
    st.markdown("Test your knowledge with AI-generated quizzes!")
    
    quiz_content = st.text_area(
        "Paste study material to generate quiz:",
        height=250,
        placeholder="Paste your lecture notes, textbook chapter, or any study material...",
        help="Provide content that covers the topics you want to test"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider(
            "Number of questions",
            min_value=3,
            max_value=10,
            value=5
        )
    
    with col2:
        quiz_type = st.selectbox(
            "Quiz Type",
            ["Multiple Choice", "True/False"]
        )
    
    if st.button("🎲 Generate Quiz", type="primary") and quiz_content:
        if len(quiz_content.split()) < 100:
            st.warning("⚠️ Please provide more content (at least 100 words) for better quiz generation.")
        else:
            with st.spinner("Creating your quiz... 🎯"):
                if quiz_type == "Multiple Choice":
                    questions = quiz_gen.generate_quiz(quiz_content, num_questions)
                else:
                    questions = quiz_gen.generate_true_false(quiz_content, num_questions)
                
                if questions:
                    st.success(f"✅ Generated {len(questions)} questions!")
                    st.markdown("---")
                    
                    # Initialize score tracking
                    if 'quiz_score' not in st.session_state:
                        st.session_state.quiz_score = 0
                        st.session_state.quiz_answers = {}
                    
                    # Display questions
                    for idx, q in enumerate(questions):
                        st.markdown(f"### Question {idx + 1}")
                        
                        if quiz_type == "Multiple Choice":
                            st.write(q['question'])
                            
                            user_answer = st.radio(
                                "Select your answer:",
                                q['options'],
                                key=f"q_{idx}",
                                label_visibility="collapsed"
                            )
                            
                            if st.button(f"Check Answer", key=f"check_{idx}"):
                                correct_letter = q['correct_answer']
                                user_letter = user_answer[0] if user_answer else ''
                                
                                if user_letter == correct_letter:
                                    st.success(f"✅ Correct! {q['explanation']}")
                                else:
                                    st.error(f"❌ Incorrect. The correct answer is {correct_letter}. {q['explanation']}")
                        
                        else:  # True/False
                            st.write(q['statement'])
                            
                            user_answer = st.radio(
                                "Is this statement true or false?",
                                ["TRUE", "FALSE"],
                                key=f"tf_{idx}",
                                label_visibility="collapsed"
                            )
                            
                            if st.button(f"Check Answer", key=f"check_tf_{idx}"):
                                if user_answer == q['answer']:
                                    st.success(f"✅ Correct! {q['explanation']}")
                                else:
                                    st.error(f"❌ Incorrect. The answer is {q['answer']}. {q['explanation']}")
                        
                        st.markdown("---")
                else:
                    st.error("❌ Could not generate quiz. Please try again or provide different content.")

#  FEATURE 5: CHAT WITH AI 
elif feature == "💬 Chat with AI":
    st.header("💬 Chat with AI")
    st.markdown("Have a conversation about any academic topic!")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about academics..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = llm_handler.simple_chat(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

# Footer
st.markdown("---")
st.markdown(f"""
    <div class="footer-text">
        <p>📚 <strong>Academic AI Assistant</strong> — Empowering Education Through AI</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">
            Made with ❤️ by <strong>Avinash</strong> | 
            {'🌙 Dark Mode' if is_dark else '☀️ Light Mode'} Active
        </p>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 1rem;">
            💡 Pro Tip: Use the sidebar to switch between features and toggle themes!
        </p>
    </div>
""", unsafe_allow_html=True)