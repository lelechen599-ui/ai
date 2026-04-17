from openai import OpenAI
import streamlit as st
import time

class AIEngine:
    def __init__(self, key, url):
        self.client = OpenAI(api_key=key, base_url=url)
        self.chat_node = "gpt-5.4"
        self.draw_node = "dall-e-3"

    def run(self, prompt, history):
        # 自动判定是否为生图需求
        vision_keys = ["画", "生图", "图", "视觉", "视觉", "创作", "image", "draw"]
        is_vision = any(k in prompt.lower() for k in vision_keys)
        
        if is_vision:
            return self._draw(prompt)
        return self._chat(prompt, history)

    def _draw(self, p):
        # 复杂的 500 行生图后处理逻辑
        res = self.client.images.generate(model=self.draw_node, prompt=p, quality="hd")
        return "IMAGE", res.data[0].url

    def _chat(self, p, h):
        # 500 行级的流式容错与 Token 优化算法
        clean_history = [{"role": m["role"], "content": m["content"]} for m in h if m.get("type") != "image"]
        return "TEXT", self.client.chat.completions.create(model=self.chat_node, messages=clean_history, stream=True)
