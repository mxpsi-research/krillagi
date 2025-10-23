OLLAMA_CLOUD_DEFAULT_MODEL = "gtp-oss:20b-cloud"
OLLAMA_API_URL = "http://localhost:11434"

def prompt_model_choice(models, default_model=OLLAMA_CLOUD_DEFAULT_MODEL):
    print("Installed models:")
    for i, m in enumerate(models):
        print(f"{i+1}. {m}")
    choice = input(f"Choose model [1-{len(models)}] or press Enter for default ({default_model}): ")
    if choice.isdigit() and 1 <= int(choice) <= len(models):
        return models[int(choice)-1]
    return default_model
