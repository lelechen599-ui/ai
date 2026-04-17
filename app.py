# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time
import datetime

# ==============================================================================
# 1. 核心业务配置
# ==============================================================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
PRIMARY_MODEL = "gpt-5.4"

MODEL_ZOO = {
    "Google Gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    "Custom Nodes": [PRIMARY_MODEL, "gpt-5.4-turbo"],
    "OpenAI Models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
}

# ==============================================================================
# 2. Apple iOS 26 浅色毛玻璃引擎 (CSS 深度定制)
# ==============================================================================
st.set_page_config(page_title="Genesis AI White", layout="wide", initial_sidebar_state="collapsed")

def inject_white_glass_css():
    st.markdown("""
    <style>
    /* 全局背景：纯净白 */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    /* 侧边栏：浅色毛玻璃 */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }

    /* 聊天气泡：浅色 Glassmorphism + 悬停动效 */
    .stChatMessage {
        background-color: rgba(245, 245, 247, 0.4) !important;
        backdrop-filter: blur(15px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(15px) saturate(160%) !important;
        border-radius: 20px !important;
        padding: 30px 10% !important;
        margin-bottom: 20px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    
    /* 鼠标悬停：白色玻璃升起感 */
    .stChatMessage:hover {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-color: rgba(66, 133, 244, 0.2); 
        transform: translateY(-4px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.08);
    }

    /* 元数据标签：浅灰质感 */
    .metadata-tag {
        font-family: 'SF Pro Display', sans-serif;
        font-size: 11px;
        color: #86868b;
        background: rgba(0, 0, 0, 0.03);
        padding: 4px 12px;
        border-radius: 12px;
        margin-right: 10px;
        border: 1px solid rgba(0, 0, 0, 0.03);
    }
    
    /* 底部输入框：浮动浅色玻璃 */
    .stChatInputContainer {
        bottom: 25px !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* 对话文字：深灰（iOS 标准色） */
    .stMarkdown p { color: #1d1d1f !important; }
    
    /* 标题：Google 经典配色 */
    .google-font {
        font-family: 'Product Sans', Arial, sans-serif;
        font-weight: bold;
    }

    /* 悲伤懒羊羊 Trademark：底部居中 */
    .trademark-footer {
        text-align: center;
        padding: 60px 0 40px 0;
        color: #d2d2d7;
        font-size: 13px;
        letter-spacing: 1px;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

inject_white_glass_css()

# ==============================================================================
# 3. 核心引擎与状态管理
# ==============================================================================
if "sessions" not in st.session_state:
    st.session_state.sessions = {"默认会话": []}
if "active_session" not in st.session_state:
    st.session_state.active_session = "默认会话"
if "locked_model" not in st.session_state:
    st.session_state.locked_model = None

client = OpenAI(
    api_key=re.sub(r'[^\x00-\x7f]', '', API_KEY).strip(),
    base_url=re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
)

# ==============================================================================
# 4. 侧边栏
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#4285f4;'>Genesis <span style='color:#ea4335;'>AI</span></h2>", unsafe_allow_html=True)
    st.caption("White Glass Edition v5.1")
    st.markdown("---")
    
    new_sess = st.text_input("➕ 新建创作主题", placeholder="主题名称...")
    if st.button("创建并切换", use_container_width=True) and new_sess:
        if new_sess not in st.session_state.sessions:
            st.session_state.sessions[new_sess] = []
            st.session_state.active_session = new_sess
            st.rerun()

    s_list = list(st.session_state.sessions.keys())
    st.session_state.active_session = st.selectbox("📂 当前主题", s_list, index=s_list.index(st.session_state.active_session))
    
    st.markdown("---")
    cat = st.selectbox("模型分类", list(MODEL_ZOO.keys()))
    pref_model = st.selectbox("指定模型", MODEL_ZOO[cat])
    
    if st.button("🗑️ 清空当前对话", use_container_width=True):
        st.session_state.sessions[st.session_state.active_session] = []
        st.session_state.locked_model = None
        st.rerun()

# ==============================================================================
# 5. 主页面渲染
# ==============================================================================
st.markdown(f"<p style='text-align:right; color:#86868b; font-size:12px;'>Space: {st.session_state.active_session}</p >", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#1d1d1f; font-weight:800; font-family:sans-serif; margin-bottom:50px;'>AIGC 创作控制台</h1>", unsafe_allow_html=True)

chat_history = st.session_state.sessions[st.session_state.active_session]

for i, msg in enumerate(chat_history):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.markdown(f"""
                <div style='display:flex; margin-top:10px; align-items:center;'>
                    <div class="metadata-tag">节点: {msg.get('model')}</div>
                    <div class="metadata-tag">耗时: {msg.get('time')}s</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📋 复制内容", key=f"cp_{i}"):
                st.code(msg["content"])

# ==============================================================================
# 6. 安全请求逻辑
# ==============================================================================
if prompt := st.chat_input("向 Google AI 提问..."):
    chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp_box = st.empty()
        status_box = st.empty()
        full_content = ""
        
        targets = [st.session_state.locked_model] if st.session_state.locked_model else [pref_model, PRIMARY_MODEL, "gemini-1.5-pro"]
        
        success = False
        start_t = time.time()
        final_m = ""

        for m_name in targets:
            if not m_name: continue
            status_box.markdown(f"<span style='color:#86868b; font-size:12px;'>正在连通节点: {m_name}...</span>", unsafe_allow_html=True)
            try:
                stream = client.chat.completions.create(
                    model=m_name,
                    messages=[{"role": m["role"], "content": m["content"]} for m in chat_history],
                    stream=True,
                    timeout=8
                )
                
                for chunk in stream:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            if not success:
                                status_box.empty()
                                success = True
                                final_m = m_name
                                st.session_state.locked_model = m_name
                            full_content += delta
                            resp_box.markdown(full_content + "▌")
                
                if success: break
            except:
                continue

        if success:
            elapsed = round(time.time() - start_t, 2)
            resp_box.markdown(full_content)
            chat_history.append({"role": "assistant", "content": full_content, "model": final_m, "time": elapsed})
            st.rerun()
        else:
            status_box.error("无法建立连接，请检查 API 余额。")

# ==============================================================================
# 7. 悲伤懒羊羊 Trademark
# ==============================================================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div class="trademark-footer">
        © 2026 Digital Media DMT Lab |™ 悲伤懒羊羊.
    </div>
    """, unsafe_allow_html=True)
