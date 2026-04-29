# 🏔️ Scenic Route & Weather Advisor (AI Agent)

An autonomous AI agent built with Python that plans scenic road trips by dynamically searching the web for the best routes, stops, and real-time weather conditions. 

Unlike standard chatbots, this application uses **Agentic AI** to break down a complex prompt, utilize external tools (DuckDuckGo Search), process the retrieved data, and format a final Markdown report for the user.

## ✨ Features
* **Autonomous Web Research:** The agent independently queries the web for route information and weather forecasts.
* **Multi-Step Reasoning:** Uses `smolagents` to orchestrate thought-action-observation loops.
* **Interactive UI:** Built with Gradio to provide a clean, user-friendly web interface without writing HTML/CSS.
* **Markdown Generation:** Synthesizes raw data into a highly readable, structured itinerary.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **AI Framework:** [smolagents](https://github.com/huggingface/smolagents) (by Hugging Face)
* **Web Interface:** [Gradio](https://gradio.app/)
* **LLM:** Qwen 2.5 Coder (3B Instruct) via Hugging Face Inference API
* **Tools:** DuckDuckGo Search API

