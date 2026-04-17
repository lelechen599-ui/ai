import streamlit as st

def inject_ios_engine(theme="Light"):
    # 定义 iOS 26 核心色板
    if theme == "Light":
        bg, text, glass, shadow = "#FFFFFF", "#1D1D1F", "rgba(255, 255, 255, 0.6)", "rgba(0,0,0,0.05)"
    else:
        bg, text, glass, shadow = "#000000", "#F5F5F7", "rgba(28, 28, 30, 0.7)", "rgba(0,0,0,0.3)"

    st.markdown(f"""
    <style>
    /* 全局过渡动画：模拟 iOS 线性回弹 */
    [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
        transition: background-color 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* iOS 26 核心毛玻璃：Glassmorphism 2.0 */
    .stChatMessage {{
        background: {glass} !important;
        backdrop-filter: blur(40px) saturate(210%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(210%) !important;
        border-radius: 32px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        padding: 40px !important;
        margin: 20px auto !important;
        max-width: 900px;
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    /* 鼠标悬停的高级感：物理浮起与光晕 */
    .stChatMessage:hover {{
        transform: scale(1.02) translateY(-10px);
        background: {glass.replace('0.6', '0.8')} !important;
        box-shadow: 0 40px 80px {shadow};
        border-color: rgba(0, 122, 255, 0.4) !important;
    }}

    /* 悲伤懒羊羊 Trademark：底部旗舰定位 */
    .sheep-footer {{
        margin-top: 150px;
        text-align: center;
        font-family: 'SF Pro Text', sans-serif;
        letter-spacing: 8px;
        color: #D2D2D7;
        font-size: 14px;
        font-weight: 300;
        padding-bottom: 50px;
    }}
    
    .sheep-footer span {{ color: #FFD60A; opacity: 0.8; }} /* 给羊加点亮色 */

    /* 针对手机端的 1000 行级适配优化 */
    @media (max-width: 768px) {{
        .stChatMessage {{ padding: 20px !important; margin: 10px !important; border-radius: 20px !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)
