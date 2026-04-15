from ollama import ask_gemma


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

        response = response.strip()
        response = response.replace("*", "")
        if len(response) < 10:
            return "⚠️ *Ответ получился слишком коротким. Попробуй ещё раз.*"
        return response

    except Exception as e:
        print("Ошибка Ollama:", e)
        return "❌ *ИИ временно недоступна.*"


def show_generation_message(bot, chat_id, msg_id):
    from texts import generation_loading_text
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=generation_loading_text(),
            parse_mode="Markdown",
        )
    except:
        pass


def escape_markdown(text):
    if not text:
        return ""

    for ch in ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]:
        text = text.replace(ch, f"\\{ch}")
    return text
