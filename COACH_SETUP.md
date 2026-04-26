# AI Coach Setup Instructions

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Set Up OpenAI API Key

You need an OpenAI API key to use the AI Coach feature. Follow these steps:

### Option A: Environment Variable (Recommended)
1. Get your API key from https://platform.openai.com/api-keys
2. Create a `.env` file in this project directory:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
3. Alternatively, set it in your shell:
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY = "sk-your-api-key-here"
   
   # Mac/Linux
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```

### Option B: Streamlit Secrets
1. Create `.streamlit/secrets.toml` in this project:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```

## 3. Run the App
```bash
streamlit run app.py
```

## Features

### AI Coach Buttons (Available after making first guess)
- **Should I guess higher? 📈** - Get confirmation and reasoning for guessing higher
- **Should I guess lower? 📉** - Get confirmation and reasoning for guessing lower  
- **What's a new strategy? 💡** - Get a novel strategy to try (different from previously suggested ones)

### How It Works (RAG Principles)
The coach considers:
- Secret number
- Valid range (low-high)
- All your previous guesses
- How far off you were from the secret
- Previously suggested strategies (to avoid repetition)
- Current difficulty level

This context is sent to ChatGPT to generate personalized, contextual coaching advice.

## API Costs
The coach uses OpenAI's API, which has a cost per request. Each button click uses approximately 100-200 tokens. Monitor your usage at https://platform.openai.com/account/usage.

## Troubleshooting

**"Coach unavailable: Missing OPENAI_API_KEY"**
- Your API key is not set. Follow the Setup steps above.

**"Coach error: Invalid API key"**
- Your API key is incorrect. Double-check at https://platform.openai.com/api-keys

**"Coach error: Rate limit exceeded"**
- You've made too many requests too quickly. Wait a moment and try again.
