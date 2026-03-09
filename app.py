"""Neuclid - Deterministic AI Math Mentor
Main Streamlit application with premium dark UI.
"""

import streamlit as st
import json
import time
import uuid
import base64
import os
from PIL import Image
import io

_LOGO_PATH = os.path.join(os.path.dirname(__file__), "LogoBg removed.png")

st.set_page_config(
    page_title="Neuclid | AI Math Mentor",
    page_icon=_LOGO_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

def _logo_base64() -> str:
    """Load logo as base64 for inline HTML embedding."""
    try:
        with open(_LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

_LOGO_B64 = _logo_base64()

# ── Inject Premium CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

:root {
    --primary: #FFB100;
    --primary-dim: rgba(255, 177, 0, 0.15);
    --primary-glow: rgba(255, 177, 0, 0.3);
    --bg-deep: #0A192F;
    --bg-card: #112240;
    --bg-elevated: #1d2d50;
    --border: rgba(255, 255, 255, 0.06);
    --border-primary: rgba(255, 177, 0, 0.2);
    --text-primary: #e6f1ff;
    --text-secondary: #8892b0;
    --text-muted: #495670;
    --success: #64ffda;
    --error: #ff6b6b;
    --warning: #ffd93d;
}

/* Global reset */
.stApp {
    background: var(--bg-deep) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--bg-elevated); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* Custom header */
.neuclid-header {
    position: sticky;
    top: 0;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    background: rgba(10, 25, 47, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    margin: -1rem -1rem 2rem -1rem;
    animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
    from { transform: translateY(-100%); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.neuclid-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.neuclid-logo-icon {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: var(--bg-deep);
    font-weight: 900;
    box-shadow: 0 0 20px var(--primary-glow);
    animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px var(--primary-glow); }
    50% { box-shadow: 0 0 35px var(--primary-glow), 0 0 60px rgba(255,177,0,0.1); }
}

.neuclid-logo-text {
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}

.neuclid-logo-badge {
    font-size: 0.6rem;
    font-weight: 700;
    color: var(--primary);
    background: var(--primary-dim);
    padding: 3px 8px;
    border-radius: 20px;
    border: 1px solid var(--border-primary);
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* Section titles */
.section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.section-title .icon {
    color: var(--primary);
    font-size: 1.2rem;
}

/* Cards */
.neuclid-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    animation: fadeInUp 0.5s ease-out;
}

.neuclid-card:hover {
    border-color: var(--border-primary);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

@keyframes fadeInUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Input mode selector tabs */
.input-tab {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--text-secondary);
}

.input-tab.active {
    background: var(--primary-dim);
    border-color: var(--primary);
    color: var(--primary);
    box-shadow: 0 0 20px rgba(255,177,0,0.1);
}

/* Pipeline stages */
.pipeline-stage {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: var(--bg-card);
    margin: 8px 0;
    transition: all 0.4s ease;
    animation: fadeInLeft 0.5s ease-out;
}

.pipeline-stage.active {
    border-color: var(--primary);
    background: var(--primary-dim);
    box-shadow: 0 0 25px rgba(255,177,0,0.15);
}

.pipeline-stage.completed {
    border-color: rgba(100,255,218,0.3);
}

.pipeline-stage.pending {
    opacity: 0.4;
    filter: grayscale(0.5);
}

@keyframes fadeInLeft {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.stage-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.stage-icon.completed {
    background: rgba(100,255,218,0.15);
    color: var(--success);
}

.stage-icon.active {
    background: var(--primary);
    color: var(--bg-deep);
    animation: pulse 2s ease-in-out infinite;
}

.stage-icon.pending {
    background: var(--bg-elevated);
    color: var(--text-muted);
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.stage-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stage-sublabel {
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    margin-top: 2px;
}

/* Connector line between stages */
.pipeline-connector {
    width: 2px;
    height: 20px;
    background: linear-gradient(to bottom, var(--primary-glow), transparent);
    margin: 0 0 0 35px;
}

/* Confidence meter */
.confidence-meter {
    text-align: center;
    padding: 1.5rem;
}

.confidence-value {
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--primary);
    line-height: 1;
    text-shadow: 0 0 30px var(--primary-glow);
}

.confidence-bar {
    width: 100%;
    height: 6px;
    background: var(--primary-dim);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 12px;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), #ffcc00);
    border-radius: 3px;
    transition: width 1.5s ease;
}

/* Memory lesson cards */
.lesson-card {
    padding: 12px 14px;
    background: rgba(255,177,0,0.03);
    border-left: 3px solid var(--primary);
    border-radius: 0 8px 8px 0;
    margin: 8px 0;
    transition: all 0.3s ease;
}

.lesson-card:hover {
    background: rgba(255,177,0,0.08);
    transform: translateX(4px);
}

.lesson-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-primary);
}

.lesson-meta {
    font-size: 0.65rem;
    color: var(--text-muted);
    font-style: italic;
    margin-top: 4px;
}

/* Step-by-step explanation */
.step-item {
    display: flex;
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    animation: fadeInUp 0.4s ease-out;
}

.step-number {
    color: var(--primary);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 0.85rem;
    flex-shrink: 0;
    min-width: 60px;
}

.step-content {
    font-size: 1rem;
    line-height: 1.7;
    color: var(--text-primary);
}

/* Feedback buttons */
.feedback-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
}

.feedback-correct {
    background: rgba(100,255,218,0.1);
    color: var(--success);
    border: 1px solid rgba(100,255,218,0.3);
}

.feedback-correct:hover {
    background: rgba(100,255,218,0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(100,255,218,0.2);
}

.feedback-incorrect {
    background: rgba(255,107,107,0.1);
    color: var(--error);
    border: 1px solid rgba(255,107,107,0.3);
}

.feedback-incorrect:hover {
    background: rgba(255,107,107,0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(255,107,107,0.2);
}

/* JSON trace viewer */
.trace-block {
    background: #050C16;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-secondary);
    overflow-x: auto;
    max-height: 300px;
    overflow-y: auto;
}

/* HITL Modal */
.hitl-modal {
    background: var(--bg-card);
    border: 2px solid var(--primary);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 0 60px rgba(255,177,0,0.15);
    animation: scaleIn 0.4s ease-out;
}

@keyframes scaleIn {
    from { transform: scale(0.9); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.hitl-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    background: rgba(255,177,0,0.1);
    color: var(--primary);
    border: 1px solid var(--border-primary);
}

/* Memory saved confirmation */
.memory-saved {
    background: var(--bg-card);
    border: 2px solid var(--primary);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    animation: scaleIn 0.5s ease-out;
}

.memory-saved-icon {
    width: 64px;
    height: 64px;
    background: var(--primary-dim);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    font-size: 2rem;
    color: var(--primary);
    animation: pulse-glow 2s ease-in-out infinite;
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-executing {
    background: rgba(255,177,0,0.1);
    color: var(--primary);
    border: 1px solid var(--border-primary);
}

.status-pass {
    background: rgba(100,255,218,0.1);
    color: var(--success);
    border: 1px solid rgba(100,255,218,0.3);
}

.status-fail {
    background: rgba(255,107,107,0.1);
    color: var(--error);
    border: 1px solid rgba(255,107,107,0.3);
}

/* Solve button */
.solve-btn {
    width: 100%;
    padding: 16px;
    background: var(--primary);
    color: var(--bg-deep);
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 800;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(255,177,0,0.3);
    letter-spacing: 0.5px;
}

.solve-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(255,177,0,0.4);
}

.solve-btn:active {
    transform: scale(0.97);
}

/* Source chip */
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 500;
    color: var(--text-secondary);
    margin: 3px;
}

/* Streamlit element overrides */
.stTextArea textarea {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 20px rgba(255,177,0,0.1) !important;
}

.stTextInput input {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 20px rgba(255,177,0,0.1) !important;
}

.stButton > button {
    background: var(--primary) !important;
    color: var(--bg-deep) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255,177,0,0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 25px rgba(255,177,0,0.35) !important;
}

.stExpander {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

div[data-testid="stExpander"] details {
    border: none !important;
}

div[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.stFileUploader {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border-primary) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
}

.stTabs [aria-selected="true"] {
    background: var(--primary-dim) !important;
    border-color: var(--primary) !important;
    color: var(--primary) !important;
}

.stSpinner > div {
    border-top-color: var(--primary) !important;
}

/* Footer */
.neuclid-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 2rem;
    margin: 2rem -1rem -1rem -1rem;
    border-top: 1px solid var(--border);
    background: rgba(10,25,47,0.8);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
}

.footer-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--success);
    display: inline-block;
    margin-right: 6px;
    animation: blink 3s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Hide streamlit column gaps */
div[data-testid="column"] { padding: 0 8px !important; }

/* Ambient background animation */
.ambient-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    overflow: hidden;
}

.ambient-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.03;
    animation: float 20s ease-in-out infinite;
}

.ambient-orb:nth-child(1) {
    width: 600px;
    height: 600px;
    background: var(--primary);
    top: -10%;
    right: -5%;
    animation-delay: 0s;
}

.ambient-orb:nth-child(2) {
    width: 400px;
    height: 400px;
    background: #4fc3f7;
    bottom: -5%;
    left: -5%;
    animation-delay: -7s;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(30px, -30px) scale(1.05); }
    66% { transform: translate(-20px, 20px) scale(0.95); }
}
</style>

<!-- Ambient background orbs -->
<div class="ambient-bg">
    <div class="ambient-orb"></div>
    <div class="ambient-orb"></div>
</div>
""", unsafe_allow_html=True)


# ── Session State Init ──────────────────────────────────────────────────────
def init_session():
    defaults = {
        "session_id": str(uuid.uuid4())[:8],
        "stage": "input",  # input -> parsing -> hitl -> solving -> result -> feedback
        "input_text": "",
        "input_mode": "text",
        "ocr_result": None,
        "asr_result": None,
        "parsed_result": None,
        "execution_result": None,
        "rag_context": None,
        "experience_warnings": "",
        "experience_id": None,
        "feedback_given": False,
        "trace_log": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# Support URL query params for automation: ?problem=...&auto=true
_qp = st.query_params
if "problem" in _qp and not st.session_state.input_text:
    st.session_state.input_text = _qp["problem"]
if "auto" in _qp and _qp["auto"] == "true" and st.session_state.stage == "input" and st.session_state.input_text.strip():
    st.session_state.stage = "parsing"
    st.query_params.clear()
    st.rerun()


# ── Header ──────────────────────────────────────────────────────────────────
_logo_html = (
    f'<img src="data:image/png;base64,{_LOGO_B64}" style="height:40px; border-radius:10px; object-fit:contain;" alt="Neuclid">'
    if _LOGO_B64
    else '<div class="neuclid-logo-icon">N</div>'
)
st.markdown(f"""
<div class="neuclid-header">
    <div class="neuclid-logo">
        {_logo_html}
        <span class="neuclid-logo-text">Neuclid</span>
        <span class="neuclid-logo-badge">AI Math Mentor</span>
    </div>
    <div style="display:flex; align-items:center; gap:16px;">
        <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;">Session: {st.session_state.session_id}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Main Layout ─────────────────────────────────────────────────────────────
col_input, col_pipeline, col_memory = st.columns([3, 5, 3])


# ── LEFT COLUMN: Problem Input ──────────────────────────────────────────────
with col_input:
    st.markdown("""
    <div class="section-title">
        <span class="icon material-symbols-outlined">edit_note</span>
        Problem Input
    </div>
    """, unsafe_allow_html=True)

    tab_text, tab_image, tab_audio = st.tabs(["Text", "Image", "Audio"])

    with tab_text:
        text_input = st.text_area(
            "Type your math problem",
            value=st.session_state.input_text,
            height=200,
            placeholder="e.g. Solve for x: 3x^2 + 7x - 5 = 0\n\nFind the limit of sin(x)/x as x approaches 0\n\nWhat is P(A|B) if P(A)=0.3, P(B)=0.5, P(A and B)=0.15?",
            label_visibility="collapsed",
        )
        if text_input != st.session_state.input_text:
            st.session_state.input_text = text_input

    with tab_image:
        uploaded_image = st.file_uploader(
            "Upload a math problem image",
            type=["png", "jpg", "jpeg", "gif", "webp"],
            label_visibility="collapsed",
        )
        if uploaded_image:
            img_bytes = uploaded_image.read()
            st.image(img_bytes, caption="Uploaded Image", use_container_width=True)
            if st.button("Extract Text from Image", key="ocr_btn"):
                with st.spinner("Running OCR..."):
                    from tools.ocr_tool import extract_text_from_image
                    result = extract_text_from_image(img_bytes, uploaded_image.name)
                    st.session_state.ocr_result = result
                    st.session_state.input_text = result["text"]
                    st.session_state.input_mode = "image"

            if st.session_state.ocr_result:
                ocr = st.session_state.ocr_result
                conf_color = "var(--success)" if ocr["confidence"] > 0.8 else "var(--warning)" if ocr["confidence"] > 0.6 else "var(--error)"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin:8px 0;">
                    <span class="status-badge" style="background:rgba(255,177,0,0.1); color:var(--primary); border:1px solid var(--border-primary);">
                        {ocr["method"]}
                    </span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:{conf_color}; font-weight:700;">
                        {ocr["confidence"]*100:.0f}% confidence
                    </span>
                </div>
                """, unsafe_allow_html=True)
                edited = st.text_area("Edit extracted text:", value=ocr["text"], key="ocr_edit", height=120)
                if edited != ocr["text"]:
                    st.session_state.input_text = edited

    with tab_audio:
        uploaded_audio = st.file_uploader(
            "Upload audio file",
            type=["wav", "mp3", "ogg", "flac"],
            label_visibility="collapsed",
        )
        if uploaded_audio:
            st.audio(uploaded_audio)
            if st.button("Transcribe Audio", key="asr_btn"):
                with st.spinner("Transcribing..."):
                    from tools.asr_tool import transcribe_audio_file
                    audio_bytes = uploaded_audio.read()
                    result = transcribe_audio_file(audio_bytes)
                    st.session_state.asr_result = result
                    st.session_state.input_text = result["text"]
                    st.session_state.input_mode = "audio"

            if st.session_state.asr_result:
                asr = st.session_state.asr_result
                st.markdown(f"""
                <div style="margin:8px 0; padding:10px; background:var(--bg-card); border-radius:10px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">Raw Transcript</div>
                    <div style="font-size:0.85rem; color:var(--text-secondary); font-style:italic;">{asr["raw_text"]}</div>
                </div>
                """, unsafe_allow_html=True)
                edited_asr = st.text_area("Edit math text:", value=asr["text"], key="asr_edit", height=100)
                if edited_asr != asr["text"]:
                    st.session_state.input_text = edited_asr

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    solve_disabled = not st.session_state.input_text.strip()
    if st.button(
        "Run Deterministic Solve",
        disabled=solve_disabled,
        key="solve_btn",
        use_container_width=True,
    ):
        st.session_state.stage = "parsing"
        st.session_state.feedback_given = False
        st.session_state.trace_log = []
        st.rerun()


# ── CENTER COLUMN: Execution Pipeline ───────────────────────────────────────
with col_pipeline:
    stage = st.session_state.stage

    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
        <div class="section-title" style="margin-bottom:0; border-bottom:none;">
            <span class="icon material-symbols-outlined">account_tree</span>
            Execution Pipeline
        </div>
        <span class="status-badge {'status-executing' if stage in ['parsing','solving'] else 'status-pass' if stage == 'result' else ''}"
              style="{'display:flex' if stage != 'input' else 'display:none'}">
            {'EXECUTING' if stage in ['parsing','solving'] else 'COMPLETE' if stage == 'result' else 'AWAITING INPUT' if stage == 'hitl' else 'READY'}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline stages visualization
    stages_def = [
        ("Parse & Tokenize", "text_fields", "parsing"),
        ("De-noise & Structure", "filter_alt", "parsing"),
        ("HITL Validation", "person_search", "hitl"),
        ("RAG Retrieval", "search", "solving"),
        ("Core Solver", "memory", "solving"),
        ("Verification", "verified_user", "solving"),
        ("Explanation", "school", "result"),
    ]

    stage_order = ["input", "parsing", "hitl", "solving", "result", "feedback"]
    current_idx = stage_order.index(stage) if stage in stage_order else 0

    for i, (label, icon, req_stage) in enumerate(stages_def):
        req_idx = stage_order.index(req_stage) if req_stage in stage_order else 0

        if current_idx > req_idx or (current_idx == req_idx and stage == "result" and req_stage == "solving"):
            state_class = "completed"
            icon_class = "completed"
            sublabel = "Completed"
        elif current_idx == req_idx:
            state_class = "active"
            icon_class = "active"
            sublabel = "Processing..."
        else:
            state_class = "pending"
            icon_class = "pending"
            sublabel = "Pending"

        if stage == "hitl" and req_stage == "hitl":
            state_class = "active"
            icon_class = "active"
            sublabel = "Awaiting Human Review..."

        icon_symbol = {"completed": "check", "active": icon, "pending": icon}.get(icon_class, icon)

        st.markdown(f"""
        <div class="pipeline-stage {state_class}">
            <div class="stage-icon {icon_class}">
                <span class="material-symbols-outlined" style="font-size:18px;">
                    {'check' if state_class == 'completed' else icon}
                </span>
            </div>
            <div>
                <div class="stage-label" style="color:{'var(--success)' if state_class=='completed' else 'var(--primary)' if state_class=='active' else 'var(--text-muted)'};">
                    {label}
                </div>
                <div class="stage-sublabel">{sublabel}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if i < len(stages_def) - 1:
            st.markdown('<div class="pipeline-connector"></div>', unsafe_allow_html=True)

    # ── Execute pipeline based on stage ─────────────────────────────────
    if stage == "parsing":
        with st.spinner("Crew 1: Sanitizing input..."):
            from agents.crew1_sanitization import run_sanitization_crew
            result = run_sanitization_crew(st.session_state.input_text)
            st.session_state.parsed_result = result
            st.session_state.trace_log.extend(result["trace"])

            if result["needs_clarification"]:
                st.session_state.stage = "hitl"
            else:
                st.session_state.stage = "solving"
            st.rerun()

    elif stage == "hitl":
        parsed = st.session_state.parsed_result
        pj = parsed.get("parsed_json", {})
        st.markdown("""
        <div class="hitl-modal">
            <div class="hitl-badge">
                <span class="material-symbols-outlined" style="font-size:14px;">precision_manufacturing</span>
                HITL Validation
            </div>
            <h3 style="font-size:1.4rem; font-weight:800; margin:12px 0 8px;">Clarification Required</h3>
            <p style="color:var(--text-secondary); font-size:0.9rem;">
                The Parser detected ambiguity that needs your input before proceeding.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if pj.get("variables"):
            st.markdown(f"""
            <div style="margin-top:16px;">
                <div style="font-size:0.7rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px;">
                    Extracted Variables
                </div>
                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                    {''.join(f'<span class="source-chip">{v}</span>' for v in pj.get("variables", []))}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if pj.get("ambiguities") or pj.get("clarification_reason"):
            reasons = pj.get("ambiguities", [])
            if pj.get("clarification_reason"):
                reasons.append(pj["clarification_reason"])
            st.markdown(f"""
            <div style="margin-top:16px;">
                <div style="font-size:0.7rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px;">
                    Flagged Issues
                </div>
                {''.join(f'<div style="padding:6px 12px; margin:4px 0; background:rgba(255,107,107,0.1); border:1px solid rgba(255,107,107,0.2); border-radius:8px; font-size:0.8rem; color:var(--error);">{r}</div>' for r in reasons)}
            </div>
            """, unsafe_allow_html=True)

        clarification = st.text_area("Provide clarification:", key="hitl_input", height=100,
                                     placeholder="e.g., The variable 'n' represents a positive integer...")

        col_discard, col_rescan, col_resume = st.columns(3)
        with col_discard:
            if st.button("Discard", key="hitl_discard"):
                st.session_state.stage = "input"
                st.rerun()
        with col_rescan:
            if st.button("Re-scan", key="hitl_rescan"):
                st.session_state.stage = "parsing"
                st.rerun()
        with col_resume:
            if st.button("Resume Pipeline", key="hitl_resume"):
                if clarification.strip():
                    st.session_state.input_text += f"\n\nClarification: {clarification}"
                    pj = st.session_state.parsed_result.get("parsed_json", {})
                    pj["needs_clarification"] = False
                    st.session_state.parsed_result["parsed_json"] = pj
                    st.session_state.parsed_result["needs_clarification"] = False
                st.session_state.stage = "solving"
                st.rerun()

    elif stage == "solving":
        with st.spinner("Crew 2: Solving..."):
            from rag.retriever import retrieve_context, format_context_for_prompt
            from memory.vector_memory import get_experience_warnings

            parsed = st.session_state.parsed_result
            pj = parsed.get("parsed_json", {})
            domain = parsed.get("domain", "Mathematics")

            query = pj.get("problem_text", st.session_state.input_text)
            rag_queries = parsed.get("route_json", {}).get("rag_queries", [query])

            all_retrieved = []
            for q in rag_queries[:3]:
                all_retrieved.extend(retrieve_context(q))

            seen_texts = set()
            unique_retrieved = []
            for item in all_retrieved:
                if item["text"] not in seen_texts:
                    seen_texts.add(item["text"])
                    unique_retrieved.append(item)

            rag_context_str = format_context_for_prompt(unique_retrieved[:8])
            st.session_state.rag_context = unique_retrieved[:8]

            experience_warnings = get_experience_warnings(query)
            st.session_state.experience_warnings = experience_warnings

            from agents.crew2_execution import run_execution_crew
            result = run_execution_crew(pj, rag_context_str, experience_warnings)
            st.session_state.execution_result = result
            st.session_state.trace_log.extend(result["trace"])

            from memory.db import save_experience
            from memory.vector_memory import store_problem_embedding
            exp_id = save_experience(
                original_text=st.session_state.input_text,
                parsed_json=json.dumps(pj),
                problem_domain=domain,
                retrieved_context=rag_context_str[:2000],
                solver_code=result.get("solver_code", ""),
                final_answer=result.get("answer", ""),
                explanation=result.get("explanation", ""),
                verifier_outcome="PASS" if result.get("verification_passed") else "FAIL",
            )
            st.session_state.experience_id = exp_id
            store_problem_embedding(exp_id, query, {"domain": domain})

            st.session_state.stage = "result"
            st.rerun()

    elif stage == "result":
        result = st.session_state.execution_result
        if result:
            verified = result.get("verification_passed", False)
            confidence = result.get("confidence", 0.5)

            st.markdown(f"""
            <div class="neuclid-card" style="border-color:{'rgba(100,255,218,0.3)' if verified else 'rgba(255,107,107,0.3)'}; margin-top:1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span class="material-symbols-outlined" style="color:{'var(--success)' if verified else 'var(--error)'}; font-size:24px;">
                            {'verified' if verified else 'error'}
                        </span>
                        <span style="font-size:1.1rem; font-weight:700;">
                            {'Verification Passed' if verified else 'Verification Issues Found'}
                        </span>
                    </div>
                    <span class="status-badge {'status-pass' if verified else 'status-fail'}">
                        {'PASS' if verified else 'REVIEW'}
                    </span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style="padding:16px; background:var(--bg-deep); border-radius:12px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px;">
                        Final Answer
                    </div>
                    <div style="font-size:1.3rem; font-weight:700; color:var(--primary); line-height:1.6;">
                        {result.get("answer", "No answer computed")}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Step-by-step explanation
            st.markdown("""
            <div style="margin-top:1.5rem;">
                <div class="section-title">
                    <span class="icon material-symbols-outlined">menu_book</span>
                    Step-by-Step Explanation
                </div>
            </div>
            """, unsafe_allow_html=True)

            explanation = result.get("explanation", "")
            st.markdown(f"""
            <div class="neuclid-card">
                <div style="line-height:1.8; font-size:0.95rem; color:var(--text-primary);">
                    {explanation.replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Agent Trace
            with st.expander("Agent Trace & Debug Info"):
                for trace_item in st.session_state.trace_log:
                    st.markdown(f"""
                    <div style="margin:8px 0;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:700; font-size:0.85rem; color:var(--primary);">{trace_item['agent']}</span>
                            <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:var(--text-muted);">
                                {trace_item['duration_ms']:.0f}ms
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(trace_item["output"][:1500], language="text")

            # Solver code
            if result.get("solver_code"):
                with st.expander("Solver Python Code"):
                    st.code(result["solver_code"], language="python")


# ── RIGHT COLUMN: Memory & Context ──────────────────────────────────────────
with col_memory:
    st.markdown("""
    <div class="section-title">
        <span class="icon material-symbols-outlined">psychology</span>
        Memory & Context
    </div>
    """, unsafe_allow_html=True)

    # Confidence indicator
    if st.session_state.execution_result:
        conf = st.session_state.execution_result.get("confidence", 0)
        conf_pct = conf * 100
        conf_label = "Deterministic Lock" if conf > 0.9 else "High Confidence" if conf > 0.7 else "Needs Review"
        conf_color = "var(--success)" if conf > 0.9 else "var(--primary)" if conf > 0.7 else "var(--error)"
        st.markdown(f"""
        <div class="neuclid-card" style="text-align:center; margin-bottom:1rem;">
            <div style="font-size:0.65rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:2px; margin-bottom:10px;">
                Model Confidence
            </div>
            <div class="confidence-value" style="color:{conf_color};">{conf_pct:.1f}%</div>
            <div style="font-size:0.7rem; color:{conf_color}; margin-top:6px; font-weight:600;">{conf_label}</div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width:{conf_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Retrieved sources
    if st.session_state.rag_context:
        st.markdown("""
        <div style="font-size:0.7rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:10px;">
            Retrieved Sources
        </div>
        """, unsafe_allow_html=True)
        for item in st.session_state.rag_context[:5]:
            st.markdown(f"""
            <div class="lesson-card">
                <div class="lesson-title">{item['topic']}</div>
                <div class="lesson-meta">Source: {item['source']} | Relevance: {(1 - item['distance']):.0%}</div>
            </div>
            """, unsafe_allow_html=True)

    # Experience warnings
    if st.session_state.experience_warnings:
        st.markdown("""
        <div style="margin-top:1rem; font-size:0.7rem; font-weight:700; color:var(--warning); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:10px;">
            Past Experience Warnings
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="neuclid-card" style="border-color:rgba(255,217,61,0.3); font-size:0.8rem; color:var(--warning);">
            {st.session_state.experience_warnings.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

    # Recent memory entries
    try:
        from memory.db import get_recent_experiences
        recent = get_recent_experiences(5)
        if recent:
            st.markdown("""
            <div style="margin-top:1rem; font-size:0.7rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:10px;">
                Recent Problems
            </div>
            """, unsafe_allow_html=True)
            for exp in recent:
                correct_icon = "check_circle" if exp.get("is_correct") else "cancel"
                correct_color = "var(--success)" if exp.get("is_correct") else "var(--error)"
                text_preview = (exp.get("original_text", "")[:60] + "...") if len(exp.get("original_text", "")) > 60 else exp.get("original_text", "")
                st.markdown(f"""
                <div class="lesson-card" style="display:flex; align-items:center; gap:8px;">
                    <span class="material-symbols-outlined" style="font-size:16px; color:{correct_color};">{correct_icon}</span>
                    <div>
                        <div class="lesson-title" style="font-size:0.75rem;">{text_preview}</div>
                        <div class="lesson-meta">{exp.get('problem_domain', 'Math')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except Exception:
        pass

    # Feedback section
    if st.session_state.stage == "result" and not st.session_state.feedback_given:
        st.markdown("""
        <div style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid var(--border);">
            <div style="font-size:0.7rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:12px;">
                Was this solution correct?
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Correct", key="fb_correct", use_container_width=True):
                from memory.db import update_feedback
                update_feedback(st.session_state.experience_id, True, "User confirmed correct", None)
                st.session_state.feedback_given = True
                st.rerun()

        with col_no:
            if st.button("Incorrect", key="fb_incorrect", use_container_width=True):
                st.session_state.stage = "feedback"
                st.rerun()

    if st.session_state.stage == "feedback":
        st.markdown("""
        <div class="hitl-modal" style="margin-top:1rem;">
            <div class="hitl-badge">Correction</div>
            <h4 style="margin:8px 0; font-weight:700;">What went wrong?</h4>
        </div>
        """, unsafe_allow_html=True)

        feedback_text = st.text_area("Describe the error:", key="fb_text", height=80,
                                     placeholder="e.g., The answer should be 1, not 0. Use L'Hopital's rule.")
        learned_rule = st.text_input("Learned rule (for future problems):", key="fb_rule",
                                     placeholder="e.g., For lim x->0 sin(x)/x, use standard identity = 1")
        save_persistent = st.checkbox("Save as persistent rule for future problems", value=True, key="fb_persist")

        if st.button("Save Feedback", key="fb_save", use_container_width=True):
            if feedback_text.strip():
                from memory.db import update_feedback
                rule = learned_rule.strip() if learned_rule.strip() else feedback_text.strip()
                update_feedback(st.session_state.experience_id, False, feedback_text, rule)
                st.session_state.feedback_given = True
                st.session_state.stage = "result"

                st.markdown("""
                <div class="memory-saved">
                    <div class="memory-saved-icon">
                        <span class="material-symbols-outlined">memory</span>
                    </div>
                    <h3 style="font-size:1.3rem; font-weight:800;">Rule saved to experience memory.</h3>
                    <p style="color:var(--text-secondary); margin-top:8px; font-size:0.85rem;">
                        Future evaluations will prioritize this correction.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(2)
                st.rerun()

    if st.session_state.feedback_given:
        st.markdown("""
        <div style="margin-top:1rem; padding:12px; background:rgba(100,255,218,0.05); border:1px solid rgba(100,255,218,0.2); border-radius:10px; text-align:center;">
            <span class="material-symbols-outlined" style="color:var(--success); font-size:20px; vertical-align:middle;">check_circle</span>
            <span style="color:var(--success); font-size:0.85rem; font-weight:600; margin-left:6px;">Feedback recorded</span>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="neuclid-footer">
    <div style="display:flex; gap:24px; align-items:center;">
        <span><span class="footer-dot"></span>Engine: Neuclid v1.0</span>
        <span>CrewAI Multi-Agent</span>
        <span>RAG + Memory Active</span>
    </div>
    <div style="display:flex; gap:16px;">
        <span style="color:var(--primary);">Session: {st.session_state.session_id}</span>
    </div>
</div>
""", unsafe_allow_html=True)
