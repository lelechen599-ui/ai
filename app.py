import streamlit as st
import time
from styles import inject_ios_engine
from engine import AIEngine

# 1. 核心链路配置
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"

# 2. 系统初始化
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.theme = "Light"

# 3. 注入 3000 行级视觉引擎
inject_ios_engine(st.session_state.theme)

# 4. 侧边栏：OS 控制台
with st.sidebar:
    st.markdown("<h1 style='color:#007AFF;'>Genesis OS</h1>", unsafe_allow_html=True)
    st.session_state.theme = st.radio("系统外观", ["Light", "Dark"])
    if st.button("清空系统内存"):
        st.session_state.messages = []
        st.rerun()

# 5. 主界面
st.markdown("<h1 style='text-align:center;'>AIGC 旗舰工作站</h1>", unsafe_allow_html=True)

# 6. 对话引擎驱动
engine = AIEngine(API_KEY, BASE_URL)

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg.get("type") == "IMAGE": st.image(msg["content"], use_container_width=True)
        else: st.markdown(msg["content"])

if prompt := st.chat_input("在 Genesis OS 中检索或创作..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        resp_type, result = engine.run(prompt, st.session_state.messages)
        
        if resp_type == "IMAGE":
            st.image(result, use_container_width=True)
            st.session_state.messages.append({"role": "assistant", "content": result, "type": "IMAGE"})
        else:
            res_box = st.empty()
            full_txt = ""
            for chunk in result:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_txt += chunk.choices[0].delta.content
                    res_box.markdown(full_txt + "▌")
            res_box.markdown(full_txt)
            st.session_state.messages.append({"role": "assistant", "content": full_txt})
            st.rerun()

# 7. 悲伤懒羊羊 Trademark
st.markdown("""
    <div class="sheep-footer">
        © 2026 DIGITAL MEDIA DMT LAB |<span>™</span> 悲伤懒羊羊
    </div>
    """, unsafe_allow_html=True)
