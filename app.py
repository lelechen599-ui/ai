# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time
import datetime

# ==============================================================================
# 1. 核心系统配置
# ==============================================================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4"
IMAGE_MODEL = "dall-e-3"

# ==============================================================================
# 2. 状态机初始化
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

client = OpenAI(
    api_key=re.sub(r'[^\x00-\x7f]', '', API_KEY).strip(),
    base_url=re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
)

# ==============================================================================
# 3. 视觉引擎：iOS 26 旗舰级毛玻璃 & 动态色彩
# ==============================================================================
st.set_page_config(page_title="Genesis OS", layout="wide", initial_sidebar_state="collapsed")

def inject_visual_core(mode):
    # 动态色彩矩阵
    if mode == "Light":
        bg, text, glass, u_glass, border = "#F2F2F7", "#1C1C1E", "rgba(255, 255, 255, 0.7)", "rgba(0, 122, 255, 0.08)", "rgba(0, 0, 0, 0.05)"
    else:
        bg, text, glass, u_glass, border = "#000000", "#FFFFFF", "rgba(28, 28, 30, 0.75)", "rgba(10, 132, 255, 0.12)", "rgba(255, 255, 255, 0.1)"

    st.markdown(f"""
    <style>
    /* 开启 GPU 硬件加速 */
    * {{ transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1); will-change: transform, opacity; }}
    
    [data-testid="stAppViewContainer"] {{ background-color: {bg} !important; }}

    /* 去标志化对话气泡 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(40px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(200%) !important;
        border-radius: 28px !important;
        border: 1px solid {border} !important;
        padding: 30px 40px !important;
        margin: 20px 0 !important;
        position: relative;
    }}
    
    /* 隐藏头像标志 */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}

    /* 智能呼吸光柱：替代廉价头像 */
    .stChatMessage::before {{
        content: ""; position: absolute; top: 30px; left: -12px;
        width: 5px; height: 30px; border-radius: 3px;
        background: #007AFF; box-shadow: 0 0 15px rgba(0, 122, 255, 0.6);
    }}
    
    /* 用户对话框：高区分度设计 */
    [data-testid="stChatMessageUser"] {{
        background: {u_glass} !important;
        border: 1px solid rgba(0, 122, 255, 0.2) !important;
        margin-left: 15% !important;
    }}
    [data-testid="stChatMessageUser"]::before {{
        left: auto; right: -12px; background: #5856D6; box-shadow: 0 0 15px rgba(88, 86, 214, 0.6);
    }}

    /* 苹果级悬停交互 */
    .stChatMessage:hover {{
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 30px 60px rgba(0,0,0,0.1);
    }}

    /* 底部信仰标识：悲伤懒羊羊 Trademark */
    .trademark {{
        text-align: center; margin-top: 120px; padding-bottom: 60px;
        color: #8E8E93; font-family: 'SF Pro Text', sans-serif;
        font-size: 13px; text-transform: uppercase;
        animation: sheepBreath 5s infinite ease-in-out;
    }}
    .trademark span {{ color: #FFD60A; margin-left: 5px; }}

    @keyframes sheepBreath {{
        0%, 100% {{ letter-spacing: 12px; opacity: 0.3; }}
        50% {{ letter-spacing: 15px; opacity: 0.7; }}
    }}

    /* 文字与组件 */
    .stMarkdown p {{ color: {text} !important; line-height: 1.6; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

inject_visual_core(st.session_state.theme)

# ==============================================================================
# 4. 侧边栏：系统内核控制
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#007AFF;'>Genesis OS</h2>", unsafe_allow_html=True)
    st.caption("Core Architecture v7.0")
    st.markdown("---")
    new_theme = st.selectbox("显示模式", ["Light", "Dark"], index=0 if st.session_state.theme=="Light" else 1)
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    if st.button("重启内核时流", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==============================================================================
# 5. 核心逻辑引擎：聊天与生图分发
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-weight:100; letter-spacing:-2px;'>Genesis <span style='font-weight:800; color:#007AFF;'>Vision</span></h1>", unsafe_allow_html=True)

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], use_container_width=True, caption="Artistic Vision")
        else:
            st.markdown(msg["content"])

if prompt := st.chat_input("在 Genesis OS 中检索或创作..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 处理逻辑
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    current_p = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        is_vision = any(k in current_p.lower() for k in ["画", "生图", "视觉", "image", "draw", "设计"])
        
        try:
            if is_vision:
                with st.spinner("🎨 正在同步视觉神经元..."):
                    res = client.images.generate(model=IMAGE_MODEL, prompt=current_p)
                    img_url = res.data[0].url
                    st.image(img_url, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": img_url, "type": "image"})
            else:
                res_box = st.empty()
                full_txt = ""
                # 上下文修剪
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-8:] if m.get("type") != "image"]
                
                stream = client.chat.completions.create(model=CHAT_MODEL, messages=history, stream=True)
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_txt += chunk.choices[0].delta.content
                        res_box.markdown(full_txt + "▌")
                res_box.markdown(full_txt)
                st.session_state.messages.append({"role": "assistant", "content": full_txt})
        except Exception as e:
            st.error(f"链路中断: {str(e)}")
    st.rerun()

# ==============================================================================
# 6. Trademark 脚注
# ==============================================================================
st.markdown(f"""<div class="trademark">© 2026 DIGITAL MEDIA TECHNOLOGY |<span>™</span> 悲伤懒羊羊</div>""", unsafe_allow_html=True)
