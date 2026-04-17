# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time
import datetime

# ==============================================================================
# 1. 核心系统参数 (一次性解决连接问题)
# ==============================================================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4"
IMAGE_MODEL = "dall-e-3"

# 强制初始化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# 客户端鲁棒性初始化
try:
    k = re.sub(r'[^\x00-\x7f]', '', API_KEY).strip()
    u = re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
    client = OpenAI(api_key=k, base_url=u)
except:
    st.error("SYSTEM CRITICAL: API LINK FAILED")

# ==============================================================================
# 2. 视觉动力学：iOS 26 旗舰毛玻璃与微光闪烁商标 (CSS 引擎)
# ==============================================================================
st.set_page_config(page_title="Genesis OS", layout="wide", initial_sidebar_state="collapsed")

def apply_apple_visuals(mode):
    if mode == "Light":
        bg, text, glass, u_glass, border = "#F2F2F7", "#1C1C1E", "rgba(255, 255, 255, 0.75)", "rgba(0, 122, 255, 0.08)", "rgba(0, 0, 0, 0.05)"
        accent, u_accent, shimmer = "#007AFF", "#5856D6", "#8E8E93"
    else:
        bg, text, glass, u_glass, border = "#000000", "#FFFFFF", "rgba(28, 28, 30, 0.8)", "rgba(10, 132, 255, 0.15)", "rgba(255, 255, 255, 0.1)"
        accent, u_accent, shimmer = "#0A84FF", "#BF5AF2", "#D1D1D6"

    st.markdown(f"""
    <style>
    /* 硬件加速 */
    * {{ transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1); will-change: transform, opacity; }}
    [data-testid="stAppViewContainer"] {{ background-color: {bg} !important; }}

    /* 无头像设计：侧边光柱身份识别 */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}

    /* AI 气泡样式：靠左 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(45px) saturate(210%) !important;
        -webkit-backdrop-filter: blur(45px) saturate(210%) !important;
        border-radius: 28px !important;
        border: 1px solid {border} !important;
        padding: 25px 35px !important;
        margin: 30px 0 !important;
        position: relative;
        max-width: 80% !important;
    }}
    .stChatMessage::before {{
        content: ""; position: absolute; top: 25px; left: -14px;
        width: 6px; height: 35px; border-radius: 3px;
        background: {accent}; box-shadow: 0 0 20px {accent};
    }}

    /* 用户气泡样式：强制右偏 + 莫兰迪蓝 */
    [data-testid="stChatMessageUser"] {{
        background: {u_glass} !important;
        border: 1px solid rgba(88, 86, 214, 0.2) !important;
        margin-left: auto !important; 
        margin-right: 0 !important;
    }}
    [data-testid="stChatMessageUser"]::before {{
        left: auto; right: -14px; background: {u_accent}; box-shadow: 0 0 20px {u_accent};
    }}

    /* 苹果级悬停交互 */
    .stChatMessage:hover {{ transform: translateY(-10px) scale(1.008); box-shadow: 0 40px 100px rgba(0,0,0,0.1); }}

    /* 🌟 微光闪烁商标 (Shimmer Effect) */
    .shimmer-tm {{
        text-align: center; margin-top: 180px; padding-bottom: 80px;
        font-family: sans-serif; font-size: 13px; text-transform: uppercase;
        background: linear-gradient(90deg, {shimmer} 0%, #FFFFFF 50%, {shimmer} 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmerAni 4s linear infinite; letter-spacing: 12px;
    }}
    @keyframes shimmerAni {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
    .shimmer-tm span {{ font-weight: 800; color: #FFD60A; -webkit-text-fill-color: #FFD60A; }}

    /* 隐藏页眉页脚 */
    header, footer {{ visibility: hidden; }}
    .stMarkdown p {{ color: {text} !important; line-height: 1.8; }}
    </style>
    """, unsafe_allow_html=True)

apply_apple_visuals(st.session_state.theme)

# ==============================================================================
# 3. 侧边栏及内核控制
# ==============================================================================
with st.sidebar:
    st.markdown(f"<h1 style='color:#007AFF;'>Genesis OS</h1>", unsafe_allow_html=True)
    st.caption("v12.0 Final Edition")
    st.markdown("---")
    
    m_opt = st.radio("模式", ["极简白 (Light)", "深邃黑 (Dark)"], index=0 if st.session_state.theme=="Light" else 1)
    st.session_state.theme = "Light" if "Light" in m_opt else "Dark"
    
    if st.button("重置时空", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==============================================================================
# 4. 主界面：对话与视觉引擎
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-weight:100; letter-spacing:-2px; color:#1d1d1f;'>Genesis <span style='font-weight:800; color:#007AFF;'>Vision</span></h1>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("type") == "image":
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("向系统发出指令..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 核心处理逻辑
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_p = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        is_v = any(k in last_p.lower() for k in ["画", "生图", "视觉", "图片", "image", "draw"])
        try:
            if is_v:
                with st.spinner("🎨 正在同步视觉神经元..."):
                    res = client.images.generate(model=IMAGE_MODEL, prompt=last_p)
                    url = res.data[0].url
                    st.image(url, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": url, "type": "image"})
            else:
                box = st.empty()
                txt = ""
                hist = [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages[-8:] if x.get("type") != "image"]
                stream = client.chat.completions.create(model=CHAT_MODEL, messages=hist, stream=True)
                for chunk in stream:
                    # 容错：必须检查 choices 是否为空
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            txt += delta
                            box.markdown(txt + "▌")
                box.markdown(txt)
                st.session_state.messages.append({"role": "assistant", "content": txt})
        except Exception as e:
            st.error(f"LINK ERROR: {e}")
    st.rerun()

# 商标
st.markdown(f'<div class="shimmer-tm">© 2026 DMT LAB |<span>™</span> 悲伤懒羊羊</div>', unsafe_allow_html=True)
