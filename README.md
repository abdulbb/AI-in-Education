# AI-in-Education

This repository accompanies the Interuniversity Course on AI in Education, bringing together Computer Science/AI students from Johannes Kepler University (JKU) and Teacher Training students from University of Passau. It features simple web prototypes of AI-powered educational tools: an English Writing Tutor and a Python Coding Tutor.

## Project Overview

- **english-tutor.html:**  
  An interactive AI-based English writing tutor where students can input assignments, drafts, and (optionally) grading rubrics. The tool offers real-time feedback and guidance, supporting learning and self-improvement.

- **python-tutor.html:**  
  An AI coding tutor for kids, presenting challenges at various levels. Learners can write and test Python code and receive friendly, conversational AI feedback to help them progress.

- **cors_proxy.py:**  
  A small local Python proxy to enable browser-based HTML files to communicate with a local LLM (language model) server. This proxy automatically adds CORS headers, so the web apps can interact with your local AI server (like LM Studio).

## Requirements

- **LM Studio** (or any local LLM server running an OpenAI-like API, e.g., http://127.0.0.1:1234)
- **Python 3.x** for the CORS proxy
- Modern web browser (for the HTML frontends)

## Setup & Usage

1. **Start your local AI server:**  
   - Launch LM Studio or another LLM server (must use OpenAI chat API format, default: http://127.0.0.1:1234).

2. **Start the CORS proxy server:**  
   ```bash
   python3 cors_proxy.py
   ```
   This will start a proxy on `http://127.0.0.1:8000`

3. **Open the HTML app:**  
   - Open `english-tutor.html` or `python-tutor.html` directly in your browser.

4. **How it works:**  
   - The HTML apps will send AI requests to the proxy at `http://127.0.0.1:8000/v1/chat/completions`, which forwards them to your local AI server (e.g., LM Studio).
   - If you need to change AI server details (host/port), edit the settings in `cors_proxy.py`.

## Notes

- All AI interactions run locally—no data leaves your machine!
- Teacher Training students are encouraged to test, evaluate, and suggest improvements to better suit pedagogical goals.
