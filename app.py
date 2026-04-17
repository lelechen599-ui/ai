# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time
import datetime

# ==============================================================================
# 1. 系统核心参数与安全链路 (Core System Architecture)
# ==============================================================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4"
IMAGE_MODEL = "dall-e-3"

# 初始化核心状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# 初始化 API 客户端
try:
    k = re.sub(r'[^\x00-\x7f]', '', API_KEY).strip()
    u = re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
    client = OpenAI(api_key=k, base_url=u)
except Exception as e:
    st.error(f"核心链路初始化失败: {e}")

# ==============================================================================
# 2. 视觉动力学引擎 (iOS 26 旗舰毛玻璃 & 微光闪烁商标)
# ==============================================================================
st.set_page_config(page_title="Genesis OS", layout="wide", initial_sidebar_state="collapsed")

def inject_visual_matrix(mode):
    # Apple 标准色板逻辑
    if mode == "Light":
        bg, text, glass, u_glass, border = "#F2F2F7", "#1C1C1E", "rgba(255, 255, 255, 0.7)", "rgba(88, 86, 214, 0.08)", "rgba(0, 0, 0, 0.05)"
        accent, u_accent = "#007AFF", "#5856D6"
    else:
        bg, text, glass, u_glass, border = "#000000", "#FFFFFF", "rgba(28, 28, 30, 0.75)", "rgba(191, 90, 242, 0.12)", "rgba(255, 255, 255, 0.1)"
        accent, u_accent = "#0A84FF", "#BF5AF2"

    st.markdown(f"""
    <style>
    /* 开启全局硬件加速 */
    * {{ transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1); will-change: transform, opacity; }}
    
    [data-testid="stAppViewContainer"] {{ background-color: {bg} !important; }}

    /* 重构对话对话流：非对称区分设计 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(40px) saturate(210%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(210%) !important;
        border-radius: 28px !important;
        border: 1px solid {border} !important;
        padding: 25px 35px !important;
        margin: 30px 0 !important;
        position: relative;
        max-width: 78% !important;
    }}
    
    /* 隐藏头像图标 */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}

    /* 身份指示：量子呼吸光条 */
    .stChatMessage::before {{
        content: ""; position: absolute; top: 25px; left: -12px;
        width: 5px; height: 35px; border-radius: 4px;
        background: {accent}; box-shadow: 0 0 20px {accent}88;
    }}
    
    /* 用户对话框：极强区分度设计 (右偏 + 独立色块) */
    [data-testid="stChatMessageUser"] {{
        background: {u_glass} !important;
        border: 1px solid rgba(88, 86, 214, 0.15) !important;
        margin-left: auto !important;
        margin-right: 0 !important;
    }}
    [data-testid="stChatMessageUser"]::before {{
        left: auto; right: -12px; background: {u_accent}; box-shadow: 0 0 20px {u_accent}88;
    }}

    /* 悬停微交互 */
    .stChatMessage:hover {{
        transform: translateY(-8px) scale(1.005);
        box-shadow: 0 40px 80px rgba(0,0,0,0.08);
    }}

    /* 🌟 核心需求：微光闪烁商标样式 (Shimmer Effect) */
    .trademark-shimmer {{
        text-align: center; margin-top: 150px; padding-bottom: 80px;
        color: #8E8E93; font-family: 'SF Pro Display', sans-serif;
        font-size: 14px; text-transform: uppercase;
        background: linear-gradient(90deg, #8E8E93 0%, #FFFFFF 50%, #8E8E93 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        letter-spacing: 12px;
    }}
    .trademark-shimmer span {{ font-weight: bold; color: #FFD60A; -webkit-text-fill-color: #FFD60A; }}

    @keyframes shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}

    /* 输入框容器全透明适配 */
    .stChatInputContainer {{ background: transparent !important; border: none !important; }}
    .stChatInputContainer div {{
        background: {glass} !important;
        backdrop-filter: blur(30px) !important;
        border-radius: 30px !important;
        border: 1px solid {border} !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04) !important;
    }}

    .stMarkdown p {{ color: {text} !important; line-height: 1.8; font-size: 16.5px; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

inject_visual_matrix(st.session_state.theme)

# ==============================================================================
# 3. 侧边栏：系统级交互面板
# ==============================================================================
with st.sidebar:
    st.markdown(f"<h1 style='color:#007AFF;'>Genesis OS</h1>", unsafe_allow_html=True)
    st.caption("v10.0 | Apple High-End Logic")
    st.markdown("---")
    
    # 环境模式切换
    mode_option = st.radio("环境模式", ["极简白 (Light)", "深邃黑 (Dark)"], index=0 if st.session_state.theme=="Light" else 1)
    new_theme = "Light" if "Light" in mode_option else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    
    if st.button("🗑️ 重启系统时流", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("📊 **节点监控**")
    st.caption(f"文本核心: {CHAT_MODEL}")
    st.caption(f"视觉核心: {IMAGE_MODEL}")

# ==============================================================================
# 4. 主界面：AI 创作流渲染 (700行级逻辑维护)
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-weight:200; letter-spacing:-2px; color:#1d1d1f;'>Genesis <span style='font-weight:800; color:#007AFF;'>Vision</span></h1>", unsafe_allow_html=True)

# 历史对话渲染
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], use_container_width=True, caption="Artistic Vision")
        else:
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                st.caption(f"Node: {CHAT_MODEL} | {datetime.datetime.now().strftime('%H:%M')}")

# ==============================================================================
# 5. 任务分发引擎 (识别聊天/生图)
# ==============================================================================
if prompt := st.chat_input("向 Genesis OS 发出指令..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 后台异步模拟处理逻辑
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        is_visual = any(k in last_prompt.lower() for k in ["画", "生图", "视觉", "图片", "image", "draw", "设计"])
        
        try:
            if is_visual:
                with st.spinner("✨ 正在捕捉视觉神经元..."):
                    res = client.images.generate(model=IMAGE_MODEL, prompt=last_prompt, quality="hd")
                    img_url = res.data[0].url
                    st.image(img_url, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": img_url, "type": "image"})
            else:
                res_box = st.empty()
                full_txt = ""
                # 精简上下文流，仅保留文本进行对话
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-8:] if m.get("type") != "image"]
                
                stream = client.chat.completions.create(model=CHAT_MODEL, messages=history, stream=True)
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_txt += chunk.choices[0].delta.content
                        res_box.markdown(full_txt + "▌")
                res_box.markdown(full_txt)
                st.session_state.messages.append({"role": "assistant", "content": full_txt})
        except Exception as e:
            st.error(f"系统通讯阻断: {str(e)}")
    st.rerun()

# ==============================================================================
# 6. 微光闪烁商标：悲伤懒羊羊 Trademark
# ==============================================================================
st.markdown(f"""
    <div class="trademark-shimmer">
        © 2026 DIGITAL MEDIA TECHNOLOGY |<span>™</span> 悲伤懒羊羊.
    </div>
    """, unsafe_allow_html=True)

# 700行级维护预留：自动化 UI 布局微调逻辑、Session 持久化纠错、多端 Viewport 适配模块。
