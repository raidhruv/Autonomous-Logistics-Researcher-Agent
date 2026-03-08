from config.settings import get_settings

settings = get_settings()

print(settings.MODEL_NAME)
print(settings.VECTOR_DB_PATH)