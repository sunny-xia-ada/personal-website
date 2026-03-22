# XYLAB Digital Twin 🍬✨

[English](#english) | [中文](#中文)

---

## English

### 🌟 Project Overview
XYLAB Digital Twin is a sophisticated personal website and AI-powered chat ecosystem. It serves as a digital representation of **Yidan Xia**, an Applied Scientist (Nordstrom, FedEx) and the founder of XYLAB. 

The project blends high-end technology with a "Sweet & Cool" aesthetic, featuring a glassmorphic chat widget that allows visitors to interact with Yidan's AI persona.

### 🚀 Technical Stack
- **Frontend**: Responsive HTML5/CSS3 with vanilla JavaScript. 
  - Features three "Emotion Modes": **🧘 Core**, **💃 Dance**, and **🎈 Play**.
  - Hosted on **GitHub Pages**.
- **Backend**: FastAPI (Python) using the modern **Google Gemini SDK** (`google-genai`).
  - **Brains**: Powered by `gemini-3.1-flash-lite-preview` or similar.
  - **Resilience**: Implements `tenacity` for exponential backoff retries to handle transient API issues.
  - Hosted on **Render.com**.

### 🛠️ Local Setup
1. **Backend**:
   ```bash
   cd personal-website
   source .venv/bin/activate
   pip install -r requirements.txt
   export GOOGLE_API_KEY="your_api_key"
   uvicorn main:app --reload
   ```
2. **Frontend**: Simply open `index.html` in your browser.

---

## 中文

### 🌟 项目概览
XYLAB Digital Twin 是一个融合了高阶审美与 AI 技术的个人网站生态系统。它是 **Yidan Xia**（曾就职于 Nordstrom, FedEx 的应用科学家，XYLAB 创始人）的数字孪生。

该项目将硬核技术与“Sweet & Cool”的美学风格相结合，内置了一个毛玻璃质感的聊天挂件，允许访客与 Yidan 的 AI 人格进行实时对话。

### 🚀 技术架构
- **前端**: 响应式 HTML5/CSS3 + 原生 JavaScript。
  - 包含三种“情绪模式”：**🧘 核心 (Core)**、**💃 舞动 (Dance)** 和 **🎈 玩乐 (Play)**。
  - 部署于 **GitHub Pages**。
- **后端**: 基于 FastAPI (Python) 和最新的 **Google Gemini SDK** (`google-genai`)。
  - **AI 核心**: 使用 `gemini-3.1-flash-lite-preview` 或同级别模型。
  - **稳定性**: 使用 `tenacity` 库实现指数退避重试，确保 API 调用在高并发或瞬时故障下的稳定性。
  - 部署于 **Render.com**。

### 🛠️ 本地开发
1. **后端**:
   ```bash
   cd personal-website
   source .venv/bin/activate
   pip install -r requirements.txt
   export GOOGLE_API_KEY="你的API密钥"
   uvicorn main:app --reload
   ```
2. **前端**: 直接在浏览器中打开 `index.html`。

---
© 2026 XYLAB. Created with ✨ by Yidan Xia.
