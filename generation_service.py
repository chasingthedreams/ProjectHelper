import random
import time

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

    mode = user_last_uniq_mode.get(user_id, "smart")

    response = safe_gemma(
        build_easier_prompt(
            last_topic,
            build_prompt,
            base_system_prompt,
            system_prompt_uniq
        )
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = mode
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

    mode = user_last_uniq_mode.get(user_id, "smart")

    response = safe_gemma(
        build_more_interesting_prompt(
            last_topic,
            build_prompt,
            base_system_prompt,
            system_prompt_uniq
        )
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = mode
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

    directions = [
        "учёба и школьная жизнь",
        "быт и повседневные проблемы",
        "организация рабочего места",
        "простые полезные вещи для дома",
        "здоровые привычки без медицины",
        "визуальные пособия для обучения",
        "простые физические модели",
        "простые химические или биологические наблюдения без лаборатории",
        "городская среда и удобство людей",
        "дизайн полезного предмета",
        "цифровая памятка или мини-инструкция",
        "простая настольная игра для обучения",
        "сравнение и проверка бытовых решений",
        "удобство хранения вещей",
        "безопасность в быту без сложных устройств",
        "простая модель процесса или явления",
        "помощь первокурсникам или школьникам",
        "улучшение учебного расписания или планирования",
        "простая инфографика по полезной теме",
        "макет полезного устройства из доступных материалов"
    ]

    project_types = [
        "практический предмет",
        "макет",
        "настольная игра",
        "инструкция",
        "плакат или инфографика",
        "сравнительный эксперимент",
        "наблюдение с выводами",
        "мини-прототип",
        "учебное пособие",
        "чек-лист",
        "простая модель",
        "демонстрационный стенд"
    ]

    materials = [
        "бумага, картон, клей, ножницы",
        "телефон, таблица и фотографии",
        "обычные предметы с рабочего стола",
        "коробка, бумага, маркеры",
        "пластиковая бутылка, картон, скотч",
        "тетрадь, ручка, линейка",
        "Canva или Figma без программирования",
        "Google Таблицы или Excel",
        "презентация, плакат и фото результата",
        "подручные материалы без покупки дорогих деталей"
    ]

    result_formats = [
        "готовый предмет, который можно показать руками",
        "макет с объяснением принципа работы",
        "плакат или инфографика с понятными выводами",
        "мини-исследование с таблицей и фотографиями",
        "настольная игра с правилами",
        "чек-лист или инструкция для реального использования",
        "простая модель явления",
        "сравнение нескольких способов решения проблемы",
        "прототип, который не обязан быть идеальным, но должен работать",
        "набор карточек, схем или шаблонов"
    ]

    banned_themes = [
        "экология",
        "сортировка мусора",
        "переработка пластика",
        "мини-теплица",
        "выращивание зелени",
        "органайзер для кабелей",
        "подставка для телефона",
        "умная мусорка",
        "бот",
        "искусственный интеллект",
        "приложение",
        "сайт"
    ]

    direction = random.choice(directions)
    project_type = random.choice(project_types)
    material = random.choice(materials)
    result_format = random.choice(result_formats)

    random_seed = f"{time.time()}-{random.randint(1000, 999999)}"

    rules_block = ""

    if last_topics:
        rules_block = (
                "\n\n⚠️ ПРАВИЛО ПРОТИВ ПОВТОРОВ:\n"
                "Ниже список прошлых тем пользователя. Нельзя повторять не только названия, "
                "но и общий смысл, идею, предмет, формат результата и область применения.\n\n"
                "ЗАПРЕЩЁННЫЕ ПРОШЛЫЕ ТЕМЫ:\n"
                + "\n".join(f"{i + 1}. {t[:180]}" for i, t in enumerate(last_topics))
        )

    user_prompt = (
            "Сгенерируй одну новую тему проекта по случайным условиям ниже.\n\n"
            f"Случайный код генерации: {random_seed}\n"
            f"Направление: {direction}\n"
            f"Тип проекта: {project_type}\n"
            f"Доступные материалы: {material}\n"
            f"Формат результата: {result_format}\n\n"
            "Главное требование:\n"
            "Тема должна быть такой, чтобы обычный студент реально мог захотеть её сделать.\n"
            "Не делай тему красивой только на словах. Она должна быть жизненной, понятной и выполнимой.\n\n"
            "Запрещённые направления для этой генерации:\n"
            + "\n".join(f"— {theme}" for theme in banned_themes)
            + "\n\n"
              "Не используй абстрактные формулировки вроде «повышение осведомлённости», "
              "«формирование культуры», «исследование влияния».\n"
              "Лучше придумай конкретную вещь, макет, игру, инструкцию, сравнение или простой прототип."
    )

    response = safe_gemma(
        build_prompt(
            base_system_prompt,
            system_prompt_uniq + rules_block,
            user_prompt
        )
    )

    user_last_uniq_topic[user_id] = response
    user_last_uniq_mode[user_id] = "classic"
    save_request(user_id, "uniq", user_prompt, response)

    return response
