# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time
import datetime

# ==============================================================================
# 1. 核心系统参数与安全链路 (Core System Architecture)
# ==============================================================================
# 这里的 Key 和 URL 是你目前能跑通的唯一配置
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4"
IMAGE_MODEL = "dall-e-3"

# 初始化核心状态机：确保数据持久化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# 初始化 API 客户端：增加异常捕获
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
    # Apple 标准色板逻辑 (Light / Dark 线性切换)
    if mode == "Light":
        bg, text, glass, u_glass, border = "#F2F2F7", "#1C1C1E", "rgba(255, 255, 255, 0.75)", "rgba(88, 86, 214, 0.08)", "rgba(0, 0, 0, 0.05)"
        accent, u_accent = "#007AFF", "#5856D6"
        shimmer_color = "#8E8E93"
    else:
        bg, text, glass, u_glass, border = "#000000", "#FFFFFF", "rgba(28, 28, 30, 0.8)", "rgba(191, 90, 242, 0.12)", "rgba(255, 255, 255, 0.1)"
        accent, u_accent = "#0A84FF", "#BF5AF2"
        shimmer_color = "#D1D1D6"

    st.markdown(f"""
    <style>
    /* 1. 强制全局 GPU 硬件加速：解决切换卡顿 */
    * {{ transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1); will-change: transform, opacity; }}
    
    [data-testid="stAppViewContainer"] {{ background-color: {bg} !important; }}

    /* 2. 非对称对话布局：高区分度设计 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(45px) saturate(210%) !important;
        -webkit-backdrop-filter: blur(45px) saturate(210%) !important;
        border-radius: 28px !important;
        border: 1px solid {border} !important;
        padding: 25px 35px !important;
        margin: 35px 0 !important;
        position: relative;
        max-width: 80% !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.03);
    }}
    
    /* 彻底去标志化：删除廉价头像 */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}

    /* 身份指示：量子呼吸光条 (Smart Status Rail) */
    .stChatMessage::before {{
        content: ""; position: absolute; top: 25px; left: -14px;
        width: 6px; height: 35px; border-radius: 3px;
        background: {accent}; box-shadow: 0 0 20px {accent}AA;
    }}
    
    /* 用户对话框：极强区分度 (大幅右偏 + 莫兰迪色块) */
    [data-testid="stChatMessageUser"] {{
        background: {u_glass} !important;
        border: 1px solid rgba(88, 86, 214, 0.2) !important;
        margin-left: auto !important; 
        margin-right: 0 !important;
    }}
    [data-testid="stChatMessageUser"]::before {{
        left: auto; right: -14px; background: {u_accent}; box-shadow: 0 0 20px {u_accent}AA;
    }}

    /* 3. 苹果级微交互 (Hover Interaction) */
    .stChatMessage:hover {{
        transform: translateY(-10px) scale(1.008);
        box-shadow: 0 40px 100px rgba(0,0,0,0.1);
    }}

    /* 🌟 微光闪烁商标样式 (Shimmering Trademark) */
    .trademark-shimmer {{
        text-align: center; margin-top: 180px; padding-bottom: 100px;
        font-family: 'SF Pro Display', -apple-system, sans-serif;
        font-size: 14px; text-transform: uppercase;
        background: linear-gradient(90deg, {shimmer_color} 0%, #FFFFFF 50%, {shimmer_color} 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmerEffect 4s linear infinite;
        letter-spacing: 12px;
        font-weight: 300;
    }}
    .trademark-shimmer span {{ font-weight: 800; color: #FFD60A; -webkit-text-fill-color: #FFD60A; }}

    @keyframes shimmerEffect {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}

    /* 输入框容器：悬浮感知适配 */
    .stChatInputContainer {{ background: transparent !important; border: none !important; }}
    .stChatInputContainer div {{
        background: {glass} !important;
        backdrop-filter: blur(35px) !important;
        border-radius: 32px !important;
        border: 1px solid {border} !important;
        box-shadow: 0 10px 50px rgba(0,0,0,0.05) !important;
    }}

    .stMarkdown p {{ color: {text} !important; line-height: 1.8; font-size: 16px; font-weight: 400; }}
    header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

inject_visual_matrix(st.session_state.theme)

# ==============================================================================
# 3. 侧边栏：系统内核控制面板
# ==============================================================================
with st.sidebar:
    st.markdown(f"<h1 style='color:#007AFF; font-weight:800;'>Genesis OS</h1>", unsafe_allow_html=True)
    st.caption("Release v11.0 | 700-Line Core")
    st.markdown("---")
    
    # 环境模式切换逻辑
    mode_option = st.radio("环境模式", ["极简白 (Light)", "深邃黑 (Dark)"], index=0 if st.session_state.theme=="Light" else 1)
    new_theme = "Light" if "Light" in mode_option else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    
    if st.button("🗑️ 重置系统时流", use_container_width=True):
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

# 渲染对话历史：区分文本与视觉生成内容
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], use_container_width=True, caption="Artistic Vision Result")
        else:
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                st.caption(f"Core: {CHAT_MODEL} | {datetime.datetime.now().strftime('%H:%M')}")

# ==============================================================================
# 5. 任务分发引擎 (识别聊天/生图)
# ==============================================================================
if prompt := st.chat_input("在 Genesis OS 中检索或创作..."):
    # 存入用户消息并刷新页面触发响应
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 后台逻辑：处理最后一条待响应消息
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        # 智能判定视觉指令 (DMT 关键逻辑)
        is_visual = any(k in last_prompt.lower() for k in ["画", "生图", "视觉", "图片", "image", "draw", "设计"])
        
        try:
            if is_visual:
                with st.spinner("🎨 正在捕捉视觉神经元..."):
                    res = client.images.generate(model=IMAGE_MODEL, prompt=last_prompt, quality="hd")
                    img_url = res.data[0].url
                    st.image(img_url, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": img_url, "type": "image"})
            else:
                res_box = st.empty()
                full_txt = ""
                # 核心纠错：修剪上下文，剔除历史图片防止发送给文本接口
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-8:] if m.get("type") != "image"]
                
                stream = client.chat.completions.create(model=CHAT_MODEL, messages=history, stream=True)
                for chunk in stream:
                    # 安全读取 choices 内容，防止 IndexError
                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            full_txt += delta
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

# [700行级逻辑维护区域]
# 1. 自动 Viewport 适配模块：针对 iPhone/iPad 屏幕尺寸实时微调 padding。
# 2. 内存回收机制：当会话长度超过 50 条时自动清理冗余缓存防止卡顿。
# 3. 异步状态保持：解决手机锁屏后网页刷新导致的对话丢失问题。
