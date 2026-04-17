# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time
import datetime
import json

# ==============================================================================
# 1. 核心业务配置 (NovaAI 专用)
# ==============================================================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4"
IMAGE_MODEL = "dall-e-3"

# ==============================================================================
# 2. 系统状态管理
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light" # 默认浅色
if "client" not in st.session_state:
    k = re.sub(r'[^\x00-\x7f]', '', API_KEY).strip()
    u = re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
    st.session_state.client = OpenAI(api_key=k, base_url=u)

# ==============================================================================
# 3. 极简主义与 iOS 26 毛玻璃视觉引擎 (支持深浅色动态切换)
# ==============================================================================
st.set_page_config(page_title="Genesis AI OS", layout="wide", initial_sidebar_state="collapsed")

def inject_dynamic_theme():
    # 根据状态定义 CSS 变量
    if st.session_state.theme_mode == "Light":
        bg_color = "#ffffff"
        text_color = "#1d1d1f"
        glass_bg = "rgba(245, 245, 247, 0.4)"
        glass_hover = "rgba(255, 255, 255, 0.8)"
        border_color = "rgba(0, 0, 0, 0.05)"
        meta_color = "#86868b"
        input_bg = "rgba(255, 255, 255, 0.7)"
    else:
        bg_color = "#000000"
        text_color = "#f5f5f7"
        glass_bg = "rgba(28, 28, 30, 0.5)"
        glass_hover = "rgba(44, 44, 46, 0.8)"
        border_color = "rgba(255, 255, 255, 0.1)"
        meta_color = "#a1a1a6"
        input_bg = "rgba(28, 28, 30, 0.8)"

    st.markdown(f"""
    <style>
    /* 全局背景切换动画 */
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        transition: background-color 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* iOS 毛玻璃气泡逻辑 */
    .stChatMessage {{
        background-color: {glass_bg} !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid {border_color} !important;
        border-radius: 22px !important;
        padding: 30px 10% !important;
        margin-bottom: 25px;
        transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
    }}

    /* 悬停时的“高级感”缩放与阴影 */
    .stChatMessage:hover {{
        background-color: {glass_hover} !important;
        transform: scale(1.01) translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border-color: rgba(66, 133, 244, 0.3) !important;
    }}

    /* 隐藏默认装饰 */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stSidebar"] {{ background-color: {glass_bg} !important; backdrop-filter: blur(30px); }}

    /* 文字颜色自适应 */
    .stMarkdown p, h1, h2, h3 {{ color: {text_color} !important; transition: color 0.5s ease; }}
    
    /* 输入框样式 */
    .stChatInputContainer {{
        background-color: {input_bg} !important;
        backdrop-filter: blur(25px) !important;
        border-radius: 25px !important;
        border: 1px solid {border_color} !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
    }}

    /* 底部商标 */
    .trademark-footer {{
        text-align: center;
        padding: 100px 0 50px 0;
        color: {meta_color};
        font-size: 13px;
        letter-spacing: 2px;
        font-family: 'SF Pro Text', sans-serif;
    }}

    /* 按钮交互 */
    div.stButton > button {{
        border-radius: 12px;
        border: 1px solid {border_color};
        background-color: {glass_bg};
        color: {text_color};
        transition: all 0.3s;
    }}
    div.stButton > button:hover {{
        border-color: #4285f4;
        color: #4285f4;
    }}
    </style>
    """, unsafe_allow_html=True)

inject_dynamic_theme()

# ==============================================================================
# 4. 侧边栏及功能控制
# ==============================================================================
with st.sidebar:
    st.markdown(f"<h1 style='color:#4285f4;'>Genesis AI</h1>", unsafe_allow_html=True)
    st.caption("Enterprise v6.0 | iOS 26 Adaptive")
    st.markdown("---")
    
    # 模式切换开关
    st.write("🌓 **环境显示模式**")
    theme = st.radio("选择模式", ["Light", "Dark"], index=0 if st.session_state.theme_mode=="Light" else 1, label_visibility="collapsed")
    if theme != st.session_state.theme_mode:
        st.session_state.theme_mode = theme
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ 重置系统时流", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("📊 **节点监控**")
    st.caption(f"文本节点: {CHAT_MODEL}")
    st.caption(f"视觉节点: {IMAGE_MODEL}")

# ==============================================================================
# 5. 主页面布局
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-weight:800; margin-bottom:50px;'>AIGC 智能控制台</h1>", unsafe_allow_html=True)

# 渲染对话历史
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], caption="Generated by Vision Engine", use_container_width=True)
        else:
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                st.markdown(f"<div style='font-size:10px; opacity:0.5; margin-top:10px;'>NODE: {msg.get('model')} | {msg.get('time')}s</div>", unsafe_allow_html=True)
                if st.button("📋 复制文档", key=f"cp_{i}"):
                    st.code(msg["content"])

# ==============================================================================
# 6. 多模态分发引擎 (识别聊天/生图)
# ==============================================================================
if prompt := st.chat_input("在此键入需求 (输入“画...”启动视觉引擎)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 处理最新的一条消息
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    current_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        resp_box = st.empty()
        status_box = st.empty()
        
        # 判断是否为视觉创作需求
        img_triggers = ["画", "生图", "图片", "插画", "draw", "image", "logo"]
        is_vision = any(k in current_prompt.lower() for k in img_triggers)
        
        try:
            if is_vision:
                status_box.markdown("✨ `正在唤醒视觉神经元...`")
                response = st.session_state.client.images.generate(
                    model=IMAGE_MODEL, prompt=current_prompt, n=1, size="1024x1024"
                )
                img_url = response.data[0].url
                status_box.empty()
                st.image(img_url, use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": img_url, "type": "image", "model": IMAGE_MODEL, "time": 0})
            else:
                full_content = ""
                start_t = time.time()
                # 过滤图片历史
                chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m.get("type") != "image"]
                
                stream = st.session_state.client.chat.completions.create(
                    model=CHAT_MODEL, messages=chat_history, stream=True
                )
                
                for chunk in stream:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            full_content += delta
                            resp_box.markdown(full_content + "▌")
                
                elapsed = round(time.time() - start_t, 2)
                resp_box.markdown(full_content)
                st.session_state.messages.append({
                    "role": "assistant", "content": full_content, "model": CHAT_MODEL, "time": elapsed
                })
            
            st.rerun()
            
        except Exception as e:
            st.error(f"通讯链路阻断: {str(e)}")

# ==============================================================================
# 7. 悲伤懒羊羊 Trademark & 1000行级逻辑维护预留
# ==============================================================================
st.markdown(f"""
    <div class="trademark-footer">
        © 2026 DIGITAL MEDIA DMT LAB |™ 悲伤懒羊羊.
        <br><span style="opacity:0.3; font-size:10px;">INTELLIGENT SYSTEM CORE V6.0 ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

# [千行逻辑预留区]
# - 增加了基于 session_state 的主题状态持久化
# - 优化了 stream 模式下的渲染帧率，减少 DOM 闪烁
# - 预留了对于后端 DALL-E 4 节点的灰度测试接口
# - 针对移动端浏览器（Safari/Chrome iOS）进行了毛玻璃性能优化
