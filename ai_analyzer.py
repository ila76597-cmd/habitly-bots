import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_ai_insight(stats):
    prompt = f"""
    Ты — добрый и мотивирующий коуч по привычкам.
    Пользователь пытается выстроить рутину. Вот его статистика за неделю:
    {stats}

    Напиши короткий, тёплый отчёт (60–80 слов):
    - Похвали за успехи
    - Укажи на проблему
    - Дай 1 практический совет
    Пиши на русском, как живой человек. Без шаблонов.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Ты молодец! Продолжай в том же духе — прогресс важнее идеала."