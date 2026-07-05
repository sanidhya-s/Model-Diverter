# Model-Diverter

An intelligent AI Model Router that analyzes a user's prompt, decomposes it into independent tasks, selects the most suitable AI model for each task, executes those tasks, and synthesizes the results into a single final response.

## Overview

Modern AI models excel at different tasks:

* GPT-5 → Coding, reasoning, mathematics
* Claude Sonnet → Long documents, writing, code review
* Gemini → Multimodal understanding, OCR, image analysis
* Grok → Real-time information and web research
* DeepSeek → Algorithms and mathematical reasoning
* Llama → Local inference and privacy-focused deployments

Instead of relying on a single model for every request, **Model-Diverter** intelligently routes each task to the model best suited for it.

Currently, execution is implemented using Gemini while the provider architecture is designed to support multiple AI providers in the future.

---

# Features

* Prompt decomposition into multiple independent tasks
* Automatic task classification
* Category and sub-category detection
* Intelligent model routing
* Provider abstraction layer
* Sequential task execution
* Final response synthesis
* Execution logging
* JSON-based configuration
* Extensible architecture for additional AI providers

---

# Architecture

```
                 User Prompt
                      │
                      ▼
             Prompt Decomposer
                      │
                      ▼
              Independent Tasks
                      │
                      ▼
               Intelligent Router
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
    GPT           Claude          Gemini
      │               │                │
      └───────────────┼────────────────┘
                      ▼
                Response Synthesizer
                      │
                      ▼
                 Final Response
```

---

# Project Structure

```
Model-Diverter/
│
├── config/
│   └── gemini_client.py
│
├── providers/
│   ├── base_provider.py
│   ├── gemini_provider.py
│   ├── openai_provider.py
│   ├── claude_provider.py
│   ├── grok_provider.py
│   ├── deepseek_provider.py
│   └── llama_provider.py
│
├── services/
│   ├── classifier.py
│   ├── decomposer.py
│   ├── router.py
│   ├── executor.py
│   └── synthesizer.py
│
├── utils/
│   └── loader.py
│
├── Docs/
│
├── categories.json
├── models.json
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# Workflow

1. User enters a prompt.
2. Gemini decomposes the prompt into multiple independent tasks.
3. Each task is classified into:

   * Category
   * Sub-category
4. The router determines the most appropriate AI model.
5. Tasks are executed sequentially (current implementation).
6. All responses are combined into one final answer.
7. The execution is saved to the `Docs/` folder with a timestamp.

---

# Configuration Files

## categories.json

Defines the supported taxonomy used for prompt classification.

Example:

```json
{
  "id": "CODING",
  "subCategories": [
    "CODE_GENERATION",
    "DEBUGGING"
  ]
}
```

---

## models.json

Defines each model's strengths and supported categories.

Example:

```json
{
  "GPT_5": {
    "categories": [
      "CODING",
      "MATHEMATICS"
    ],
    "strengths": [
      "CODE_GENERATION",
      "DEBUGGING"
    ]
  }
}
```

---

# Current Provider Support

| Provider | Status         |
| -------- | -------------- |
| Gemini   | ✅ Implemented  |
| OpenAI   | 🚧 Placeholder |
| Claude   | 🚧 Placeholder |
| Grok     | 🚧 Placeholder |
| DeepSeek | 🚧 Placeholder |
| Llama    | 🚧 Placeholder |

The provider abstraction allows new providers to be added without modifying the routing logic.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd Model-Diverter
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
API_KEY=YOUR_GEMINI_API_KEY
```

---

# Running the Project

```bash
python main.py
```

Example:

```
Enter your prompt:

Build an API similar to Stripe with subscriptions and webhooks.
```

---

# Output

The application displays:

* Generated tasks
* Routing decisions
* Execution progress
* Individual task responses
* Final synthesized response

It also stores the complete execution log inside:

```
Docs/
```

Example:

```
Docs/
└── 2026-07-06_22-18-34.txt
```

---

# Routing Strategy

Each task is scored against every available model using:

* Supported categories
* Model strengths
* Routing heuristics

The model with the highest score is selected.

---

# Future Roadmap

* Native OpenAI integration
* Native Claude integration
* Native Grok integration
* Native DeepSeek integration
* Ollama / Local LLM support
* Parallel execution across providers
* Dependency-aware task execution (DAG)
* Provider-specific rate limiting
* Cost-aware routing
* Latency-aware routing
* Response caching
* Streaming responses
* Retry and fallback mechanisms
* REST API using FastAPI
* Web dashboard
* Plugin system for custom providers
* Model benchmarking
* Automatic provider health monitoring

---

# Technologies Used

* Python
* Google Gemini API
* python-dotenv
* JSON
* Thread-safe architecture (future parallel execution)
* Modular provider pattern

---

# License

This project is intended for learning, experimentation, and research. Choose an appropriate open-source license (such as MIT, Apache 2.0, or GPL) before distributing or accepting external contributions.

---

# Contributing

Contributions are welcome.

Potential areas include:

* New AI provider integrations
* Improved routing algorithms
* Better prompt decomposition
* Cost optimization
* Performance improvements
* Testing and documentation

Please open an issue or submit a pull request to discuss proposed changes.

---

# Author

Developed as an AI orchestration and model routing platform to intelligently leverage the strengths of multiple large language models for complex user requests.
