import streamlit as st
from styles import inject_ios_engine
from engine import AIEngine

# 1. 核心链路配置
API_KEY = "sk-zYqnIwoG9pI58Mbe7cMNIK9KyNPtnx7u5PcrtLbj0SBZ2VtG"
BASE_URL = "https://us.novaiapi.com/v1"

# 2. 状态机初始化（保持主题持久化）
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# 3. 动态样式注入
inject_ios_engine(st.session_state.theme)

# 4. 侧边栏：极简模式切换
with st.sidebar:
    st.markdown("### 💠 Genesis Control")
    # 使用 selectbox 替换 radio 减少点击时的动画冲突
    new_theme = st.selectbox("显示模式", ["Light", "Dark"], index=0 if st.session_state.theme=="Light" else 1)
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    
    if st.button("清空系统时空"):
        st.session_state.messages = []
        st.rerun()

# 5. 主内容区（去除多余图标后的高级对话流）
st.markdown("<h1 style='text-align:center; font-weight:200; letter-spacing:-1px;'>Genesis <span style='color:#007AFF; font-weight:800;'>Vision</span></h1>", unsafe_allow_html=True)

engine = AIEngine(API_KEY, BASE_URL)

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg.get("type") == "IMAGE":
            st.image(msg["content"], use_container_width=True)
        else:
            st.markdown(msg["content"])

# 6. 请求逻辑
if prompt := st.chat_input("在 Genesis OS 中检索或创作..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 自动处理逻辑（解决回复完不停止的问题）
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        resp_type, result = engine.run(st.session_state.messages[-1]["content"], st.session_state.messages)
        
        if resp_type == "IMAGE":
            st.image(result, use_container_width=True)
            st.session_state.messages.append({"role": "assistant", "content": result, "type": "IMAGE"})
        elif resp_type == "TEXT":
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
st.markdown("""<div class="sheep-footer">© 2026 DIGITAL MEDIA DMT LAB |<span>™</span> 悲伤懒羊羊</div>""", unsafe_allow_html=True)
