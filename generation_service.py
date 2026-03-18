from session_data import user_last_uniq_topic, user_last_uniq_mode
from states import user_data


def generate_smart_topic(
    user_id,
    get_last_topics,
    build_prompt,
    base_system_prompt,
    system_prompt_uniq,
    build_smart_uniq_prompt,
    safe_gemma,
    save_request
):
    response = safe_gemma(
        build_smart_uniq_prompt(
            user_id,
            get_last_topics,
            build_prompt,
            base_system_prompt,
            system_prompt_uniq
        )
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = "smart"
    save_request(user_id, "smart_uniq", str(user_data.get(user_id, {})), response)

    return response


def regenerate_smart_topic(
    user_id,
    get_last_topics,
    build_prompt,
    base_system_prompt,
    system_prompt_uniq,
    build_smart_uniq_prompt,
    safe_gemma,
    save_request
):
    response = safe_gemma(
        build_smart_uniq_prompt(
            user_id,
            get_last_topics,
            build_prompt,
            base_system_prompt,
            system_prompt_uniq
        )
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = "smart"
    save_request(user_id, "smart_uniq_regenerate", str(user_data.get(user_id, {})), response)

    return response


def make_topic_easier(
    user_id,
    build_prompt,
    base_system_prompt,
    system_prompt_uniq,
    build_easier_prompt,
    safe_gemma,
    save_request
):
    last_topic = user_last_uniq_topic.get(user_id)
    if not last_topic:
        return None

    response = safe_gemma(
        build_easier_prompt(
            last_topic,
            build_prompt,
            base_system_prompt,
            system_prompt_uniq
        )
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = "smart"
    save_request(user_id, "smart_make_easier", last_topic, response)

    return response


def make_topic_more_interesting(
    user_id,
    build_prompt,
    base_system_prompt,
    system_prompt_uniq,
    build_more_interesting_prompt,
    safe_gemma,
    save_request
):
    last_topic = user_last_uniq_topic.get(user_id)
    if not last_topic:
        return None

    response = safe_gemma(
        build_more_interesting_prompt(
            last_topic,
            build_prompt,
            base_system_prompt,
            system_prompt_uniq
        )
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = "smart"
    save_request(user_id, "smart_make_more_interesting", last_topic, response)

    return response


def generate_classic_topic(
    user_id,
    get_last_topics,
    build_prompt,
    base_system_prompt,
    system_prompt_uniq,
    safe_gemma,
    save_request
):
    last_topics = get_last_topics(user_id, limit=30)
    rules_block = ""

    if last_topics:
        rules_block = (
            "\n\n⚠️ ПРАВИЛО ДЛЯ ГЕНЕРАЦИИ:\n"
            "• НЕ повторяй темы из списка ниже\n"
            "• Каждый новый проект должен быть принципиально другим по сути и типу\n"
            "• Старайся делать тему такой, чтобы студент сказал «Хочу это сделать!»\n"
            "\nЗАПРЕЩЁННЫЕ ПОВТОРЫ:\n"
            + "\n".join(f"{i + 1}. {t[:120]}" for i, t in enumerate(last_topics))
        )

    response = safe_gemma(
        build_prompt(base_system_prompt, system_prompt_uniq + rules_block, "")
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = "classic"
    save_request(user_id, "uniq", "", response)

    return response