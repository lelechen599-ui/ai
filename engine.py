from openai import OpenAI
import streamlit as st
import time

class AIEngine:
    def __init__(self, key, url):
        self.client = OpenAI(api_key=key, base_url=url)
        self.chat_node = "gpt-5.4"
        self.draw_node = "dall-e-3"

    def run(self, prompt, history):
        # 增加语义预处理，防止空请求
        if not prompt.strip(): return None, None
        
        is_vision = any(k in prompt.lower() for k in ["画", "生图", "视觉", "image", "draw"])
        
        try:
            if is_vision:
                return self._draw(prompt)
            return self._chat(prompt, history)
        except Exception as e:
            return "ERROR", str(e)

    def _draw(self, p):
        res = self.client.images.generate(model=self.draw_node, prompt=p, quality="hd")
        return "IMAGE", res.data[0].url

    def _chat(self, p, h):
        # 逻辑优化：只传输必要的上下文，减少服务器负担
        clean_history = [{"role": m["role"], "content": m["content"]} for m in h[-10:] if m.get("type") != "IMAGE"]
        return "TEXT", self.client.chat.completions.create(model=self.chat_node, messages=clean_history, stream=True)
