from config.settings import get_settings

s = get_settings()

print(s.TAVILY_API_KEY)
print(s.GROQ_API_KEY)