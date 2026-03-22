# XYLAB Digital Twin v5.4.1 🧬✨🍭🚀

[English](#english) | [中文](#中文)

---

## English

### 🌟 Project Overview
**XYLAB Digital Twin v5.4.1** is a high-polish, interactive personal portfolio and AI ecosystem. This version is **fully live**, with the frontend hosted on GitHub Pages and a persistent connection to the FastAPI backend on Render.com. It blends the modern **"Swagapp" Bento Box** aesthetic with a sophisticated **3-Mode Theme System**.

The site is designed to be "living software," where the interface adapts to the user's selected "emotion mode."

### ✨ Key Features (v5.4)
- **Hybrid Bento Architecture**: A modern grid-based UI with massive rounded corners and floating interactive pills.
- **3-Mode Interaction Engine**:
  - **🧘 CORE**: Clean, minimal, high-contrast professional mode.
  - **💃 DANCE**: Cyberpunk dark mode with Neon Pink/Cyan accents and dynamic dancer line patterns.
  - **🎈 PLAY**: Bouncy glassmorphism with a soft Loopy watermark background and playful physics.
- **DNA / ABOUT Tab**: A deep dive into the "Logic" (Quant Econ, AWS, PySpark) and "Emotion" (Dancer, Art, Traveler) that makes up the XYLAB identity.
- **AI Digital Twin**: An Apple-style glassmorphic chat widget powered by **Google Gemini**, capable of discussing causal inference, dance, or AI architecture.

### 🚀 Technical Stack
- **Frontend**: Responsive HTML5/CSS3 + Vanilla JS.
  - **Physics**: Custom `cubic-bezier` based bouncy animations.
  - **Visuals**: Dynamic background layers with independent opacity control.
- **Backend**: FastAPI (Python) using the **Google Gemini SDK** (`google-genai`).
  - **Model**: Powered by `gemini-2.0-flash` or similar.
  - **Resilience**: Integrated `tenacity` for robust API error handling.
- **Deployment**: Dual-hosted on **GitHub Pages** (Frontend) and **Render.com** (Backend).

### 🛠️ Local Setup
1. **Backend**:
   ```bash
   cd personal-website
   source .venv/bin/activate
   pip install -r requirements.txt
   export GOOGLE_API_KEY="your_api_key"
   python main.py
   ```
2. **Frontend**: Open `index.html` in any modern browser.

---

## 中文

### 🌟 项目概览
**XYLAB Digital Twin v5.4.1** 是一个高审美、强交互的个人作品集与 AI 生态系统。该版本已**完全进入生产环境**，其前端部署于 GitHub Pages，并实时连接到部署在 Render.com 上的 FastAPI 后端。它将现代 **"Swagapp" Bento Box (便当盒)** 美学与复杂的 **三模态皮肤系统** 相结合。

本项目旨在打造“有生命力”的软件，界面会根据用户选择的“情绪模式”实时演变。

### ✨ 核心特性 (v5.4)
- **混合便当盒架构**: 现代网格化 UI，配合大圆角和动态浮动组件。
- **三模态交互引擎**:
  - **🧘 CORE (核心)**: 干净、极简、高对比度的专业办公模式。
  - **💃 DANCE (舞动)**: 赛博朋克深色模式，霓虹粉/青配色，搭配动态舞者线条背景。
  - **🎈 PLAY (玩乐)**: 梦幻果冻质感，带有 Loopy 水印背景和高弹性交互物理效果。
- **个人 DNA 标签页**: 深度展示构筑 XYLAB 身份的“逻辑”(量化经济学、AWS、PySpark) 与“感性”(舞者、艺术、旅行者)。
- **AI 数字孪生**: 苹果风毛玻璃聊天框，由 **Google Gemini** 驱动，可深度探讨因果推断、舞蹈或 AI 架构。

### 🚀 技术架构
- **前端**: 响应式 HTML5/CSS3 + 原生 JavaScript。
  - **物理效果**: 基于 `cubic-bezier` 的自定义弹性动画。
  - **视觉设计**: 具有独立透明度控制的动态背景层。
- **后端**: 基于 FastAPI (Python) 和 **Google Gemini SDK** (`google-genai`)。
  - **内核**: 使用 `gemini-2.0-flash` 或同级别模型。
  - **鲁棒性**: 集成 `tenacity` 库实现 API 错误的自动重试。
- **部署**: 采用 **GitHub Pages** (前端) + **Render.com** (后端) 的双重部署方案。

### 🛠️ 本地开发
1. **后端**:
   ```bash
   cd personal-website
   source .venv/bin/activate
   pip install -r requirements.txt
   export GOOGLE_API_KEY="你的API密钥"
   python main.py
   ```
2. **前端**: 直接在浏览器中打开 `index.html`。

---
© 2026 XYLAB. Created with ✨ by Yidan Xia.
