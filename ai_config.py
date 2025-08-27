# API Configuration File
# IMPORTANT: Change the API key here to your actual OpenAI API key

# OpenAI API Configuration
OPENAI_API_KEY = "your-openai-api-key-here"
OPENAI_MODEL = "gpt-4"
OPENAI_BASE_URL = "https://api.openai.com/v1"

# Alternative AI API Options (uncomment to use)
# For Anthropic Claude:
# ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
# AI_PROVIDER = "anthropic"

# For Google Gemini:
# GOOGLE_API_KEY = "your-google-api-key-here"
# AI_PROVIDER = "google"

# For any OpenAI-compatible API:
# CUSTOM_API_KEY = "your-custom-api-key-here"
# CUSTOM_BASE_URL = "https://your-custom-api-endpoint.com/v1"
# AI_PROVIDER = "custom"

# Default provider (change this to switch AI providers)
AI_PROVIDER = "openai"

# API Request Settings
MAX_TOKENS = 2000
TEMPERATURE = 0.7
REQUEST_TIMEOUT = 30

# Chat Settings
MAX_CONVERSATION_HISTORY = 20
CHAT_MODEL_CONTEXT_LIMIT = 8000
