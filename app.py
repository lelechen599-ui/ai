# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time

# ==============================================================================
# 1. 系统核心配置
# ==============================================================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4"
IMAGE_MODEL = "dall-e-3"

# 强制初始化状态机
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# 初始化客户端
client = OpenAI(
    api_key=re.sub(r'[^\x00-\x7f]', '', API_KEY).strip(),
    base_url=re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
)

# ==============================================================================
# 2. 视觉动力学引擎 (iOS 26 旗舰毛玻璃 & 深度动态切换)
# ==============================================================================
st.set_page_config(page_title="Genesis OS", layout="wide", initial_sidebar_state="collapsed")

def apply_ui_logic():
    # 动态色值定义
    is_dark = st.session_state.theme == "Dark"
    bg = "#000000" if is_dark else "#F2F2F7"
    text = "#FFFFFF" if is_dark else "#1C1C1E"
    glass = "rgba(28, 28, 30, 0.75)" if is_dark else "rgba(255, 255, 255, 0.75)"
    u_glass = "rgba(10, 132, 255, 0.15)" if is_dark else "rgba(0, 122, 255, 0.08)"
    border = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.05)"
    status_shadow = "rgba(88, 86, 214, 0.5)" if is_dark else "rgba(0, 122, 255, 0.3)"

    st.markdown(f"""
    <style>
    /* 1. 硬件加速与平滑过渡 */
    * {{ transition: all 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); }}
    [data-testid="stAppViewContainer"] {{ background-color: {bg} !important; }}

    /* 2. 彻底删除标志图标 */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}

    /* 3. 高级感对话框重构 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(40px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(200%) !important;
        border-radius: 26px !important;
        border: 1px solid {border} !important;
        padding: 30px 40px !important;
        margin: 25px 0 !important;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
    }}

    /* 身份指示：光感呼吸条 */
    .stChatMessage::before {{
        content: ""; position: absolute; top: 32px; left: -10px;
        width: 4px; height: 26px; border-radius: 4px;
        background: #007AFF; box-shadow: 0 0 15px rgba(0, 122, 255, 0.5);
    }}

    /* 用户对话框：高区分度右偏设计 */
    [data-testid="stChatMessageUser"] {{
        background: {u_glass} !important;
        margin-left: 12% !important;
        border: 1px solid rgba(0, 122, 255, 0.2) !important;
    }}
    [data-testid="stChatMessageUser"]::before {{
        left: auto; right: -10px; background: #5856D6; box-shadow: 0 0 15px {status_shadow};
    }}

    /* 悬停物理反馈 */
    .stChatMessage:hover {{
        transform: translateY(-8px) scale(1.005);
        box-shadow: 0 25px 50px rgba(0,0,0,0.1);
    }}

    /* 悲伤懒羊羊 Trademark 呼吸标识 */
    .sheep-tm {{
        text-align: center; margin-top: 150px; padding-bottom: 50px;
        color: #8E8E93; font-family: sans-serif; font-size: 13px;
        letter-spacing: 12px; text-transform: uppercase;
        animation: sheepPulse 5s infinite ease-in-out;
    }}
    @keyframes sheepPulse {{
        0%, 100% {{ opacity: 0.3; transform: scale(0.98); }}
        50% {{ opacity: 0.6; transform: scale(1); letter-spacing: 15px; }}
    }}

    /* 隐藏多余 UI */
    header, footer {{ visibility: hidden; }}
    .stMarkdown p {{ color: {text} !important; font-size: 16px; line-height: 1.7; }}
    </style>
    """, unsafe_allow_html=True)

apply_ui_logic()

# ==============================================================================
# 3. 侧边栏：极简交互控制台
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#007AFF;'>Genesis OS</h2>", unsafe_allow_html=True)
    st.caption("v7.5 High-End Architecture")
    st.markdown("---")
    
    # 模式切换
    mode = st.selectbox("系统视觉模式", ["极简白 (Light)", "深邃黑 (Dark)"], 
                        index=0 if st.session_state.theme == "Light" else 1)
    new_mode = "Light" if "极简白" in mode else "Dark"
    if new_mode != st.session_state.theme:
        st.session_state.theme = new_mode
        st.rerun()

    if st.button("🗑️ 清空时空数据", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==============================================================================
# 4. 主工作区渲染
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-weight:100; letter-spacing:-2px;'>Genesis <span style='font-weight:800; color:#007AFF;'>Vision</span></h1>", unsafe_allow_html=True)

# 历史对话流
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], use_container_width=True, caption="Artistic Vision Active")
        else:
            st.markdown(msg["content"])

# 输入驱动
if prompt := st.chat_input("向 AI 发出指令（聊天或画图）..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 后台逻辑响应
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        # 视觉/文本双模判定
        is_visual = any(k in last_prompt.lower() for k in ["画", "生图", "视觉", "image", "draw", "设计", "图片"])
        
        try:
            if is_visual:
                with st.spinner("🎨 正在同步视觉神经元..."):
                    res = client.images.generate(model=IMAGE_MODEL, prompt=last_prompt)
                    img_url = res.data[0].url
                    st.image(img_url, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": img_url, "type": "image"})
            else:
                res_box = st.empty()
                full_txt = ""
                # 剔除历史中的图片以防 API 报错
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:] if m.get("type") != "image"]
                
                stream = client.chat.completions.create(model=CHAT_MODEL, messages=history, stream=True)
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_txt += chunk.choices[0].delta.content
                        res_box.markdown(full_txt + "▌")
                res_box.markdown(full_txt)
                st.session_state.messages.append({"role": "assistant", "content": full_txt})
        except Exception as e:
            st.error(f"系统链路中断: {str(e)}")
    st.rerun()

# ==============================================================================
# 5. 悲伤懒羊羊 Trademark
# ==============================================================================
st.markdown("""<div class="sheep-tm">© 2026 DIGITAL MEDIA TECHNOLOGY |™ 悲伤懒羊羊</div>""", unsafe_allow_html=True)
