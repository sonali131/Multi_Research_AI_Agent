# 🚀 ResearchMind – Multi-Agent AI Research System

ResearchMind is an end-to-end multi-agent AI system that performs **search, extraction, synthesis, and critique** in a single intelligent pipeline.

Built using **Python, Streamlit, Mistral AI, and Tavily**, this system mimics real-world AI agent workflows with planning, tool usage, memory, and iterative reasoning.

---

## 🧠 Key Features

- 🔍 Multi-agent architecture (4 specialized agents)
- ⚡ Planner-based reasoning loop (plan → execute → refine)
- 🌐 Real-time web search using Tavily API
- 🤖 LLM-powered reasoning via Mistral AI
- 🧩 Modular pipeline design
- 📊 Analytics dashboard for agent performance
- 📝 AI-generated structured research reports
- 🔄 Iterative refinement for improved output quality

---

## 🏗️ System Architecture

The system follows a **planner-executor model**:

1. **Planner Agent**
   - Breaks user query into subtasks

2. **Research Agent**
   - Fetches real-time data using Tavily

3. **Synthesis Agent**
   - Combines and structures information

4. **Critique Agent**
   - Refines and improves final output

---

## 🔁 Agent Workflow


User Query → Planner → Research → Synthesis → Critique → Final Report


Each step maintains **context/state**, enabling multi-step reasoning.

---

## 🧠 Memory & State

- Session-based context tracking
- Intermediate outputs passed between agents
- Ensures continuity across multi-step tasks

---

## 📊 Evaluation Approach

- Measured:
  - Accuracy
  - Relevance
  - Completeness

- Improvements:
  - Reduced hallucination via real-time search
  - Added iterative refinement loop
  - Optimized prompt structure

---

## ⚠️ Failure Handling

Handled key failure modes:

- ❌ Hallucinations → Fixed using real-time search
- ❌ Irrelevant outputs → Improved prompts
- ❌ Incomplete reasoning → Added refinement loop

---

## 🖥️ Tech Stack

- Python
- Streamlit
- Mistral AI (LLM)
- Tavily API (Search)
- Custom Agent Orchestration

---

## 🚀 Getting Started

### 1. Clone the repo


bash
git clone https://github.com/sonali131/Multi_Research_AI_Agent.git
cd Multi_Research_AI_Agent
2. Install dependencies
pip install -r requirements.txt
3. Setup environment variables

Create a .env file:

MISTRAL_API_KEY=your_key
TAVILY_API_KEY=your_key
4. Run the app
streamlit run app.py
📸 Demo Features
Query-based research pipeline
Real-time processing
Analytics dashboard
AI-generated reports
## 📸 Demo Screenshots

<img width="938" height="441" alt="Screenshot 2026-04-14 155537" src="https://github.com/user-attachments/assets/07333e9f-b0bb-4cbe-89af-be1c0602a6cf" />

<img width="941" height="441" alt="Screenshot 2026-04-14 155559" src="https://github.com/user-attachments/assets/7cbaea1f-1ce3-443b-ba5e-156dd58a081b" />

<img width="885" height="433" alt="Screenshot 2026-04-14 155635" src="https://github.com/user-attachments/assets/73722cef-56c5-461e-8e07-ebfb6da9cbe1" />

<img width="936" height="438" alt="Screenshot 2026-04-14 155704" src="https://github.com/user-attachments/assets/40535f40-bde7-4a06-a949-9d529c67c68b" />

📌 Example Query
What is the impact of big data?
🎯 Future Improvements
Persistent memory (vector DB)
Multi-user support
Advanced evaluation metrics
Autonomous long-horizon agents

👩‍💻 Author
Sonali Mishra
🔗 GitHub: https://github.com/sonali131
