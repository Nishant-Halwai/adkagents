# Google ADK Agent Examples

This project contains several examples of AI agents built using the **Google Agent Development Kit (ADK)**. These examples demonstrate various capabilities, from simple single-tool agents to complex multi-model implementations with fallback mechanisms.

## 🚀 Project Overview

The repository is organized into different modules, each showcasing a specific feature of the ADK:

- **`agentverse/`**: 🧪 **Basic Agent**
  - A simple implementation of a root agent.
  - Demonstrates how to define a basic tool (`get_current_time`) and attach it to an agent.
  - Uses a single model configuration.

- **`multitool/`**: 🛠️ **Multi-Tool Agent**
  - Showcases an agent equipped with multiple specialized tools.
  - Includes tools for retrieving weather information (`get_weather`) and the current time (`get_current_time`).
  - Demonstrate instructions for complex tool orchestration.

- **`multimodel/`**: 🤖 **Multi-Model Fallback Agent**
  - Demonstrates advanced model management using **LiteLLM**.
  - Configured with a primary model (**Gemini**) and fallback models (**GPT-4**, **Claude**) to ensure high availability and reliability.
  - Includes error handling and automatic retries.

## 🛠️ Tech Stack

- **Framework**: [Google ADK](https://github.com/google-gemini/adk) (Agent Development Kit)
- **Model Orchestration**: [LiteLLM](https://github.com/BerriAI/litellm)
- **Primary LLM**: Gemini 1.5/2.5 Flash
- **Fallback LLMs**: OpenAI GPT-4o-mini, Anthropic Claude 3 Haiku

## ⚙️ Setup & Installation

### 1. Git & Ignored Files
This repository is configured to ignore sensitive and local configuration files:
- **`.env`**: Contains private API keys.
- **`.adk/`**: ADK-specific internal state/configurations.

**Note for Developers:** If you are pulling this repository, you must manually create your own `.env` files in the respective directories or the root as described below.

### 2. Environment Configuration
Create a `.env` file with your API keys:

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. Install Dependencies
You **must** have the Google Agent Development Kit installed in your system:

```bash
pip install google-adk litellm python-dotenv
```

## 📖 Usage

### Running Agents
Each example is designed to be standalone. Navigate to any of the module directories and run the agent:

```bash
python agentverse/agent.py
# or
python multitool/agent.py
# or
python multimodel/agent.py
```

### Developer Note: Creating New Agents
When developing new features, it is recommended to create a separate file or directory for every new agent to keep the examples isolated and clean.

### Testing Fallbacks
You can test the multi-model fallback logic using the test script:

```bash
python multitool/tes.py
```

## 📂 Project Structure

```text
├── agentverse/          # Simple agent example
├── multimodel/          # Agent with multi-model fallback
├── multitool/           # Agent with multiple tools
│   ├── agent.py         # Main agent logic
│   └── tes.py           # Fallback testing script
├── .env                 # Environment variables (Git-ignored)
└── .gitignore           # Git ignore rules
```

## 🤝 Contributing
Feel free to add more examples or improve existing ones by submitting a pull request.
