# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import re
import time

# ==========================================
# 1. 配置区 (确保 Key 和地址准确)
# ==========================================
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"
CHAT_MODEL = "gpt-5.4" 
IMAGE_MODEL = "dall-e-3" # 常见的生图模型名，如果报错请咨询卖家具体的模型名

# ==========================================
# 2. UI 引擎 (保持 iOS 26 极简白)
# ==========================================
st.set_page_config(page_title="Genesis AI Multi", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
    .stChatMessage {
        background-color: rgba(245, 245, 247, 0.4) !important;
        backdrop-filter: blur(15px);
        border-radius: 20px !important;
        border: 1px solid rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }
    .stChatMessage:hover { background-color: rgba(255, 255, 255, 0.8) !important; transform: translateY(-3px); }
    .trademark-footer { text-align: center; padding: 60px 0; color: #d2d2d7; font-size: 13px; }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 核心逻辑
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

client = OpenAI(
    api_key=re.sub(r'[^\x00-\x7f]', '', API_KEY).strip(),
    base_url=re.sub(r'[^\x00-\x7f]', '', BASE_URL).strip()
)

st.markdown("<h1 style='text-align:center; color:#1d1d1f; font-family:sans-serif;'>Genesis <span style='color:#4285f4;'>Vision</span></h1>", unsafe_allow_html=True)

# 渲染历史
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], caption="AI 生成的艺术作品", use_column_width=True)
        else:
            st.markdown(msg["content"])

# 输入处理
if prompt := st.chat_input("输入指令（输入“画...”即可触发创作）"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 判定是否为生图需求
        is_draw_request = any(keyword in prompt for keyword in ["画", "生图", "draw", "image", "生成图片"])
        
        try:
            if is_draw_request:
                with st.spinner("✨ 正在构思艺术画面..."):
                    # 调用生图接口
                    response = client.images.generate(
                        model=IMAGE_MODEL,
                        prompt=prompt,
                        n=1,
                        size="1024x1024"
                    )
                    image_url = response.data[0].url
                    st.image(image_url, use_column_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": image_url, "type": "image"})
            else:
                # 普通对话模式
                resp_box = st.empty()
                full_content = ""
                stream = client.chat.completions.create(
                    model=CHAT_MODEL,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m.get("type") != "image"],
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_content += chunk.choices[0].delta.content
                        resp_box.markdown(full_content + "▌")
                st.session_state.messages.append({"role": "assistant", "content": full_content})
                st.rerun()
                
        except Exception as e:
            st.error(f"通讯异常: {str(e)}")

st.markdown("<div class='trademark-footer'>© 2026 Digital Media DMT Lab |™ 悲伤懒羊羊.</div>", unsafe_allow_html=True)
