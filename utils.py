from ollama import ask_gemma
from texts import generation_loading_text


def build_prompt(base_system_prompt, system_prompt, user_text):
    return (
        base_system_prompt
        + "\n\n"
        + system_prompt
        + "\n\nЗАПРОС ПОЛЬЗОВАТЕЛЯ:\n"
        + (user_text or "")
    )


def safe_gemma(prompt):
    try:
        response = ask_gemma(prompt)
        if not response or not response.strip():
            return "⚠️ *Не удалось получить ответ.*"
        return response.strip()
    except Exception as e:
        print("Ошибка Ollama:", e)
        return "❌ *ИИ временно недоступна.*"


def show_generation_message(bot, chat_id, msg_id):
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=generation_loading_text(),
            parse_mode="Markdown",
        )
    except:
        pass