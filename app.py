# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re, time, datetime

# ==============================================================================
# 1. 核心系统参数 (一次性解决连接问题)
# ==============================================================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4"
IMAGE_MODEL = "dall-e-3"

# 强制初始化状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# 安全初始化客户端
try:
    k = re.sub(r'[^\x00-\x7f]', '', API_KEY).strip()
    u = re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
    client = OpenAI(api_key=k, base_url=u)
except:
    st.error("CORE LINK FAILED")

# ==============================================================================
# 2. 视觉引擎：iOS 26 旗舰毛玻璃与微光闪烁商标
# ==============================================================================
st.set_page_config(page_title="Genesis OS", layout="wide", initial_sidebar_state="collapsed")

def apply_ui_core(mode):
    if mode == "Light":
        bg, text, glass, u_glass, border = "#F2F2F7", "#1C1C1E", "rgba(255, 255, 255, 0.7)", "rgba(0, 122, 255, 0.08)", "rgba(0, 0, 0, 0.05)"
        accent, u_accent, shimmer = "#007AFF", "#5856D6", "#8E8E93"
    else:
        bg, text, glass, u_glass, border = "#000000", "#FFFFFF", "rgba(28, 28, 30, 0.75)", "rgba(10, 132, 255, 0.15)", "rgba(255, 255, 255, 0.1)"
        accent, u_accent, shimmer = "#0A84FF", "#BF5AF2", "#D1D1D6"

    st.markdown(f"""
    <style>
    /* 硬件加速 */
    * {{ transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1); }}
    [data-testid="stAppViewContainer"] {{ background-color: {bg} !important; }}

    /* 身份识别：去标志化设计 */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}

    /* AI 气泡：靠左 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(40px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(200%) !important;
        border-radius: 26px !important;
        border: 1px solid {border} !important;
        padding: 25px 35px !important;
        margin: 25px 0 !important;
        position: relative;
        max-width: 80% !important;
    }}
    .stChatMessage::before {{
        content: ""; position: absolute; top: 25px; left: -10px;
        width: 5px; height: 30px; border-radius: 3px;
        background: {accent}; box-shadow: 0 0 15px {accent};
    }}

    /* 用户气泡：强制右偏 + 莫兰迪蓝 */
    [data-testid="stChatMessageUser"] {{
        background: {u_glass} !important;
        margin-left: auto !important; 
        margin-right: 0 !important;
    }}
    [data-testid="stChatMessageUser"]::before {{
        left: auto; right: -10px; background: {u_accent}; box-shadow: 0 0 15px {u_accent};
    }}

    /* 悬停物理反馈 */
    .stChatMessage:hover {{ transform: translateY(-5px) scale(1.005); box-shadow: 0 30px 60px rgba(0,0,0,0.05); }}

    /* 🌟 微光闪烁商标 (Shimmer Effect) */
    .shimmer-tm {{
        text-align: center; margin-top: 150px; padding-bottom: 60px;
        font-family: sans-serif; font-size: 13px; text-transform: uppercase;
        background: linear-gradient(90deg, {shimmer} 0%, #FFFFFF 50%, {shimmer} 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmerAni 4s linear infinite; letter-spacing: 10px;
    }}
    @keyframes shimmerAni {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
    .shimmer-tm span {{ font-weight: 800; color: #FFD60A; -webkit-text-fill-color: #FFD60A; }}

    header, footer {{ visibility: hidden; }}
    .stMarkdown p {{ color: {text} !important; line-height: 1.7; }}
    </style>
    """, unsafe_allow_html=True)

apply_ui_core(st.session_state.theme)

# ==============================================================================
# 3. 侧边栏与系统设置
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#007AFF;'>Genesis OS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    m_opt = st.radio("模式切换", ["Light (极简白)", "Dark (深邃黑)"])
    st.session_state.theme = "Light" if "Light" in m_opt else "Dark"
    if st.button("重启内核", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==============================================================================
# 4. 主工作流：非对称对话系统
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-weight:800; color:#007AFF;'>Genesis <span style='font-weight:200;'>Vision</span></h1>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("type") == "image":
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("在 Genesis OS 中检索或创作..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_p = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        is_v = any(k in last_p.lower() for k in ["画", "生图", "视觉", "图片", "image", "draw"])
        try:
            if is_v:
                with st.spinner("🎨 Creating..."):
                    res = client.images.generate(model=IMAGE_MODEL, prompt=last_p)
                    st.image(res.data[0].url, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": res.data[0].url, "type": "image"})
            else:
                box, txt = st.empty(), ""
                hist = [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages[-8:] if x.get("type") != "image"]
                stream = client.chat.completions.create(model=CHAT_MODEL, messages=hist, stream=True)
                for chunk in stream:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            txt += delta
                            box.markdown(txt + "▌")
                box.markdown(txt)
                st.session_state.messages.append({"role": "assistant", "content": txt})
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")
    st.rerun()

st.markdown(f'<div class="shimmer-tm">© 2026 DMT LAB |<span>™</span> 悲伤懒羊羊</div>', unsafe_allow_html=True)
