import streamlit as st

def inject_ios_engine(theme="Light"):
    # 颜色变量矩阵（增加对比度与质感）
    if theme == "Light":
        bg, text = "#F2F2F7", "#1C1C1E"
        glass = "rgba(255, 255, 255, 0.7)"
        user_glass = "rgba(0, 122, 255, 0.1)"  # 用户对话框微蓝
        border = "rgba(0, 0, 0, 0.05)"
    else:
        bg, text = "#000000", "#FFFFFF"
        glass = "rgba(28, 28, 30, 0.75)"
        user_glass = "rgba(10, 132, 255, 0.15)"
        border = "rgba(255, 255, 255, 0.1)"

    st.markdown(f"""
    <style>
    /* 1. 开启全局硬件加速，解决卡顿 */
    * {{
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        will-change: background-color, transform, backdrop-filter;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
    }}

    /* 2. 重构对话框：高区分度 + 无图标设计 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
        border-radius: 24px !important;
        border: 1px solid {border} !important;
        margin: 20px 0 !important;
        padding: 25px !important;
        position: relative;
    }}

    /* 用户对话框特殊样式（区分度增强） */
    [data-testid="stChatMessageUser"] {{
        background: {user_glass} !important;
        border: 1px solid rgba(0, 122, 255, 0.2) !important;
        margin-left: 15% !important;
    }}

    /* 隐藏默认图标，改用高级感呼吸灯 */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{
        display: none !important;
    }}
    
    .stChatMessage::before {{
        content: "";
        position: absolute;
        top: 25px;
        left: -10px;
        width: 4px;
        height: 20px;
        border-radius: 2px;
        background: #007AFF;
        box-shadow: 0 0 10px #007AFF;
    }}
    [data-testid="stChatMessageUser"]::before {{
        left: auto;
        right: -10px;
        background: #5856D6;
        box-shadow: 0 0 10px #5856D6;
    }}

    /* 3. 悲伤懒羊羊 Trademark：悬浮动态感 */
    .sheep-footer {{
        margin-top: 100px;
        text-align: center;
        font-family: 'SF Pro Text', sans-serif;
        letter-spacing: 12px;
        color: #8E8E93;
        font-size: 13px;
        padding-bottom: 60px;
        text-transform: uppercase;
        animation: breath 4s infinite ease-in-out;
    }}
    
    @keyframes breath {{
        0%, 100% {{ opacity: 0.3; letter-spacing: 12px; }}
        50% {{ opacity: 0.6; letter-spacing: 14px; }}
    }}

    /* 4. 输入框：悬浮感适配 */
    .stChatInputContainer {{
        border: none !important;
        background: transparent !important;
        padding: 0 10% 30px 10% !important;
    }}
    
    .stChatInputContainer div {{
        background: {glass} !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 30px !important;
        border: 1px solid {border} !important;
    }}
    </style>
    """, unsafe_allow_html=True)
