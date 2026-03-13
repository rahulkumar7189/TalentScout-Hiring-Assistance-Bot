# TalentScout Hiring Assistant 🤖

**Author:** [Rahul Kumar](https://github.com/rahulkumar7189)

## Project Overview

An AI-powered hiring assistant chatbot built with **Streamlit** and **LangChain**, using **Groq's LLaMA 3.3 70B** model. This project was developed as an intelligent Hiring Assistant for "TalentScout," a fictional recruitment agency specializing in technology placements. 

The primary goal of the chatbot is to assist in the initial screening of candidates by:
1. **Information Gathering:** Collecting essential personal details (Name, Contact Info, Experience, Desired Position).
2. **Tech Stack Declaration:** Prompting candidates to declare their specific proficiency in programming languages, frameworks, databases, and tools.
3. **Technical Question Generation:** Generating precisely 3-5 tailored technical questions based directly on the candidate's declared tech stack.
4. **Context Handling & Fallback:** Maintaining conversation flow and intelligently handling off-topic responses without deviating from the recruitment focus.

---

## Features

- **Conversational Screening** — Collects candidate information naturally, asking one or two questions at a time to avoid overwhelming the user. Includes UI validations and role examples.
- **Tailored Technical Questions** — Generates 3–5 technical questions based on the candidate's declared tech stack.
- **Smart Conversation Handling** — Handles off-topic inputs gracefully using a strict fallback mechanism to steer candidates back on track. 
- **Automatic Data Extraction** — Parses structured JSON from the LLM response at interview completion and persists it to a local JSON database.
- **UI Enhancements** — Built with a custom Streamlit sidebar and styled headers for a professional presentation.
- **Interview Reset** — One-click "Start New Interview" button after completion.

---

## Technical Details (Architecture)

| Layer | Technology |
|---|---|
| **Programming Language** | Python 3.10+ |
| **Frontend / UI** | Streamlit (Custom Sidebar & HTML styling) |
| **LLM Orchestration** | LangChain |
| **Large Language Model** | Groq (llama-3.3-70b-versatile) |
| **Data Storage** | Local JSON file (`candidates_data.json`) - Simulated backend |
| **Environment Config** | `python-dotenv` |

---

## Project Structure

```
talentscout_bot/
├── app.py                   # Streamlit entry point (thin UI layer)
├── config.py                # Centralised settings (API key, model, paths)
├── requirements.txt         # Python dependencies
├── .env                     # API key (git-ignored)
├── .env.example             # Template for .env
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── candidates_data.json     # Auto-generated candidate records (git-ignored)
└── src/                     # Core application package
    ├── __init__.py           # Package exports
    ├── chatbot.py            # TalentScoutBot class (orchestrator)
    ├── llm.py                # LLM factory (build_llm, build_chain)
    ├── prompts.py            # System prompt and validation instructions
    ├── database.py           # JSON-based data persistence (Simulated Backend)
    └── utils.py              # Response processing (JSON extraction Regex)
```

### Module Responsibilities

| Module | Purpose |
|---|---|
| `config.py` | Loads `.env`, exposes `GROQ_API_KEY`, `MODEL_NAME`, `MODEL_TEMPERATURE`, `DB_PATH` |
| `src/llm.py` | `build_llm()` creates Groq model; `build_chain()` assembles LangChain pipeline |
| `src/prompts.py` | `SYSTEM_PROMPT` containing information gathering rules, fallback mechanisms, and strict formatting tools. |
| `src/database.py` | Manages local storage simulations (`load_candidates()`, `save_candidate()`). |
| `src/utils.py` | regex operations to extract the final candidate payload. |
| `src/chatbot.py` | `TalentScoutBot` class — ties LLM and utils together, exposes `get_response()` |
| `app.py` | Streamlit UI — Custom layout, active session state, chat rendering, user input handling. |

---

## Prerequisites

- **Python 3.10+**
- A **Groq API key** — get one at [console.groq.com](https://console.groq.com/)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/rahulkumar7189/TalentScout-Hiring-Assistance-Bot.git
cd TalentScout-Hiring-Assistance-Bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## How It Works

1. **User opens the app** → The bot sends an initial greeting and begins the interview.
2. **Information gathering** → The bot asks for personal details one or two at a time (name, email, phone, experience, location, desired position, tech stack). It provides role examples to guide candidate input.
3. **Technical assessment** → Once the tech stack is collected, the bot generates 3-5 tailored technical questions and waits for answers. It handles off-topic responses gracefully and redirects candidates back to the assessment.
4. **Wrap-up** → After technical questions, the bot asks if the candidate has any questions about the company or role.
5. **Data persistence** → When the candidate confirms they're done, the bot emits a structured JSON block which is automatically extracted, parsed, and saved to `candidates_data.json`.

---

## Technical Documentation & Prompt Design

### Prompt Design
The core intelligence of the chatbot is driven by `src/prompts.py`. The system prompt enforces several crucial behavioral patterns:
*   **Structured Data Collection:** Dictates a specific order of fields to collect gracefully, preventing the bot from overwhelming users with sudden form-fill requests.
*   **Contextual Questioning:** Instructions guide the LLM to generate 3-5 challenging but non-pedantic questions directly mapped to the declared tech stack.
*   **Fallback Mechanism:** Explicit rules are given to handle off-topic or evasive responses. The bot acknowledges the user's input politely but safely steers the conversation back to the recruitment track.
*   **Strict JSON Finalization:** The prompt culminates by forcing the model to output a strictly schemas validation-ready markdown JSON block once the interview is concluded.

### Challenges & Solutions
*   **JSON Extraction Predictability:** Early iterations sometimes resulted in the model failing to place the JSON correctly or emitting conversational fluffs inside the codeblock.
    *   *Solution:* We enforced a strict regex parser (`src/utils.py`) that ignores conversational text and only attempts extraction from ` ```json ` blocks.
*   **Conversation Focus:** The model had a tendency to entertain off-topic discussions. 
    *   *Solution:* We implemented an explicit "Fallback Mechanism" instruction in the system prompt preventing derailment.

---

## Data Storage

Candidate records are stored in `candidates_data.json` with the following schema:

```json
{
    "status": "COMPLETED",
    "full_name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-234-567-8900",
    "years_of_experience": "5",
    "desired_position": "Full Stack Developer",
    "current_location": "New York, NY",
    "tech_stack": {
        "programming_languages": ["Python", "JavaScript"],
        "frameworks": ["Django", "React"],
        "databases": ["PostgreSQL", "MongoDB"],
        "tools": ["Docker", "Git"]
    },
    "technical_answers_summary": "...",
    "timestamp": "2026-03-13T19:25:00.000000"
}
```

---

## Customisation

### Change the LLM model

Edit `config.py`:

```python
MODEL_NAME = "llama-3.3-70b-versatile"   # change to any Groq-supported model
MODEL_TEMPERATURE = 0.3                   # adjust creativity
```

### Modify the interview flow

Edit `src/prompts.py` to change what information is collected, the number of technical questions, or the bot's personality.

### Switch LLM provider

1. `requirements.txt` — replace `langchain-groq` with e.g. `langchain-openai`
2. `.env` — replace `GROQ_API_KEY` with `OPENAI_API_KEY`
3. `config.py` — update the env var name and default model
4. `src/llm.py` — replace `ChatGroq` import with `ChatOpenAI`

---

## License

This project is for educational and demonstration purposes.
