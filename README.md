# 🤖 AI Cold Email Agent

> **A multi-agent AI system that researches companies, identifies business pain points, generates personalized cold emails, and reviews their quality using LangGraph.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Workflow-1C3C3C?style=flat-square)](https://www.langchain.com/langgraph)
[![Groq](https://img.shields.io/badge/Groq-Qwen-FF6B35?style=flat-square)](https://groq.com/)
[![Tavily](https://img.shields.io/badge/Tavily-Web_Search-000000?style=flat-square)](https://tavily.com/)
[![Firecrawl](https://img.shields.io/badge/Firecrawl-Web_Scraping-FF6B00?style=flat-square)](https://www.firecrawl.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square\&logo=streamlit\&logoColor=white)](https://streamlit.io/)

---

## 🎯 Overview

The **AI Cold Email Agent** automates the process of creating research-based cold emails for business outreach.

Instead of manually researching a company and writing an email from scratch, the system uses multiple specialized AI agents that work together:

**Research → Pain Points → Email Generation → Review**

The final result is a concise, company-focused cold email with a quality score and factuality review.

---

## ✨ Features

* 🔍 **Company Research** — Collects company information using web search and website scraping.
* 🎯 **Pain Point Analysis** — Identifies potential business problems relevant to the provided service.
* ✍️ **AI Email Generation** — Creates personalized cold emails based on the collected research.
* 🛡️ **Factuality Protection** — Prevents the email generator from intentionally inventing statistics, clients, case studies, or business results.
* 📝 **Email Review** — Evaluates personalization, clarity, CTA, factuality, and overall quality.
* 🔄 **LangGraph Workflow** — Connects specialized agents into a structured execution flow.
* 🌐 **Streamlit Interface** — Provides a simple interface for running the complete workflow.
* ⚡ **Groq + Qwen** — Provides fast LLM inference.

---

## 🧠 Agent Architecture

```text
                ┌──────────────────┐
                │   User Input     │
                │ Company + Service│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Research Agent   │
                │ Tavily +         │
                │ Firecrawl        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Pain Point Agent │
                │ Business Problem │
                │ Analysis         │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Email Writer     │
                │ Personalized     │
                │ Cold Email       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Review Agent     │
                │ Quality +        │
                │ Factuality       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   Final Email    │
                └──────────────────┘
```

---

## 🛠️ Tech Stack

| Technology           | Purpose                              |
| -------------------- | ------------------------------------ |
| 🐍 **Python**        | Core application logic               |
| 🧩 **LangGraph**     | Multi-agent workflow orchestration   |
| 🧠 **Groq + Qwen**   | LLM-powered reasoning and generation |
| 🔎 **Tavily**        | Company web research                 |
| 🕷️ **Firecrawl**    | Website content extraction           |
| 🎨 **Streamlit**     | Interactive web interface            |
| 🔐 **python-dotenv** | Environment variable management      |

---

## 🔄 How It Works

### 1. 🔍 Research Agent

The agent receives a company name and website.

It uses **Tavily** to search the web and **Firecrawl** to extract website content.

The LLM then summarizes:

* What the company does
* Products/services
* Target customers
* Growth stage
* Recent news or achievements

---

### 2. 🎯 Pain Point Agent

The research is passed to the next agent.

It identifies:

* Top business pain points
* Which problem the user's service can solve
* Potential business impact

This gives the email writer meaningful context instead of generating a generic email.

---

### 3. ✍️ Email Writer Agent

The writer receives:

* Company information
* Research
* Pain points
* User's service
* Sender information

It generates a professional cold email with:

* Subject
* Personalized opening
* Problem
* Solution
* Business value
* CTA

The email is also instructed to avoid unsupported claims and fake social proof.

---

### 4. 📝 Review Agent

The generated email is evaluated across five dimensions:

```text
Personalization
Clarity
CTA
Factuality
Overall Score
```

The reviewer also checks whether the email contains unsupported:

* Statistics
* Revenue figures
* Percentages
* Clients
* Case studies
* Business achievements

---

## 🛡️ Factuality Protection

A major design goal of this project is reducing **AI-generated misinformation in sales outreach**.

The email writer is instructed to:

> Use only facts supported by the company research.

It must not create:

* ❌ Fake clients
* ❌ Fake case studies
* ❌ Fake statistics
* ❌ Fake revenue
* ❌ Fake performance results

Business assumptions can still be used, but they should be expressed as **potential problems rather than confirmed facts**.

This makes the generated outreach more reliable and professional.

---

## 📂 Project Structure

```text
ai-cold-email-agent/
│
├── agents.py          # AI agents and agent logic
├── app.py             # Streamlit application
├── graph.py           # LangGraph workflow
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-cold-email-agent.git
cd ai-cold-email-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

**Never commit API keys to GitHub.**

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 💡 Example Workflow

**Input**

```text
Company: Shopify
Website: https://www.shopify.com
Service: AI Chatbot for customer support
Role: AI Engineer
```

**Agent Pipeline**

```text
Company Research
       ↓
Pain Point Identification
       ↓
Cold Email Generation
       ↓
Factuality & Quality Review
       ↓
Final Email
```

---

## 🎓 What This Project Demonstrates

This project demonstrates practical experience with:

* Multi-agent AI systems
* LangGraph state-based workflows
* LLM application development
* Prompt engineering
* Web research pipelines
* Web scraping
* AI-generated content validation
* Factuality protection
* Agent orchestration
* Streamlit application development
* API-based AI integration

---

## 🚀 Future Improvements

Potential future improvements include:

* 👤 Decision-maker discovery
* 📧 Email sending integration
* 💾 Lead/database management
* 📊 Campaign analytics
* 🔁 Advanced self-correction loops
* 🧠 Better company-specific personalization
* 🔐 Stronger structured factuality validation
* 🚀 Production deployment

---

## 👨‍💻 Author

**Abdul Samad**
AI Engineer | Generative AI | AI Agents

Building practical AI systems using LLMs, RAG, agents, and automation.

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐.
