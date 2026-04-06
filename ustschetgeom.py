import streamlit as st
import time
import os

# === НАСТРОЙКИ ТЕСТА ===
TIME_LIMIT = 7 * 60  # Время в секундах (7 минут)

# Заполните этот список данными из вашего файла
# Формат: "image" - имя картинки, "answer" - правильный ответ, "explanation" - пояснение, "points" - баллы
# Замените ваш текущий список questions на этот:
questions = [
    {
        "image": "1.png",
        "answer": "ромб",
        "explanation": "Ответ: ромб[cite: 9]. 1. FEGH - параллелограмм[cite: 10]. 2. FC=GD, CH=DH, ∠C=∠D следовательно CFH=DHG, тогда FH=GH[cite: 11]. 3. Параллелограмм, у которого смежные стороны равны - ромб[cite: 11].",
        "points": 1
    },
    {
        "image": "2.png",
        "answer": "8",
        "explanation": "Ответ: 8[cite: 18]. 1. ∠BCD=30°, тогда ∠C=60°, следовательно трапеция равнобедренная[cite: 19]. 2. ∠B=120°, ∠ABC=∠ACB=30° следовательно треугольник АВС равнобедренный, тогда AC=AB=BD=x, CD=2x (∠BCD=30°)[cite: 20, 21]. 3. 20=5x, x=4, 2x=CD=8[cite: 22].",
        "points": 1
    },
    {
        "image": "3.png",
        "answer": "120",
        "explanation": "Ответ: 120[cite: 28]. Сумма углов, прилежащих к боковой стороне, равна 180°. 180-60=120[cite: 29].",
        "points": 1
    },
    {
        "image": "4.png",
        "answer": "60",
        "explanation": "Ответ: 60[cite: 33]. В равнобедренной трапеции углы при каждом основании равны[cite: 34].",
        "points": 1
    },
    {
        "image": "5.png",
        "answer": "15",
        "explanation": "Ответ: 15[cite: 40]. В равнобедренной трапеции диагонали равны[cite: 41].",
        "points": 1
    },
    {
        "image": "6.png",
        "answer": "6",
        "explanation": "Ответ: 6[cite: 52]. В равнобедренной трапеции СЕ = DF. Тогда CE=(24-12)/2[cite: 53].",
        "points": 1
    },
    {
        "image": "7.png",
        "answer": "равнобедренная",
        "explanation": "Ответ: Равнобедренная[cite: 57]. Боковые стороны равны - равнобедренная[cite: 58].",
        "points": 1
    },
    {
        "image": "8.png",
        "answer": "10",
        "explanation": "Ответ: 10[cite: 66]. Из формулы m=(a+b)/2, где m средняя линия, получаем AB=(20-15)*2[cite: 68].",
        "points": 1
    },
    {
        "image": "9.png",
        "answer": "5",
        "explanation": "Ответ: 5[cite: 80]. Длина отрезка, соединяющего середины диагоналей трапеции, равна полуразности оснований. (20-10)/2=5[cite: 81].",
        "points": 1
    },
    {
        "image": "10.png",
        "answer": "108",
        "explanation": "Ответ: 108[cite: 90]. S=(a+b)/2 * h[cite: 91].",
        "points": 1
    },
    {
        "image": "11.png",
        "answer": "6",
        "explanation": "Ответ: 6 [cite: 98]. h = c * sin(α)[cite: 100].",
        "points": 1
    },
    {
        "image": "12.png",
        "answer": "40",
        "explanation": "Ответ: 40[cite: 111]. S = m * h, m - средняя линия[cite: 112, 113].",
        "points": 1
    },
    {
        "image": "13.png",
        "answer": "50",
        "explanation": "Ответ: 50[cite: 121]. S = 1/2 * d1 * d2 * sin(φ)[cite: 123].",
        "points": 1
    },
    {
        "image": "14.png",
        "answer": "прямоугольная",
        "explanation": "Ответ: Прямоугольная[cite: 125].",
        "points": 1
    }
]

max_points = sum(q["points"] for q in questions)

# === ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (SESSION STATE) ===
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'answers' not in st.session_state:
    st.session_state.answers = [""] * len(questions)
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'test_finished' not in st.session_state:
    st.session_state.test_finished = False


def update_timer():
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TIME_LIMIT - elapsed)
    minutes = remaining // 60
    seconds = remaining % 60
    return f"Осталось: {minutes:02d}:{seconds:02d}", remaining


# === ИНТЕРФЕЙС ===
st.title("Устный счет: Трапеция")

if not st.session_state.test_finished:
    # --- Блок таймера ---
    timer_text, remaining = update_timer()

    # Чтобы таймер обновлялся, но не сбрасывал фокус с полей ввода каждые 1 сек,
    # мы выведем его в верхнюю панель и добавим кнопку "Обновить время",
    # либо время зафиксируется при отправке ответов.
    st.info(f"⏱️ {timer_text}")

    if remaining <= 0:
        st.warning("Время вышло! Тест завершен автоматически.")
        st.session_state.test_finished = True
        st.rerun()

    # --- Ввод имени ---
    st.session_state.name = st.text_input("Введите ваше имя:", value=st.session_state.name)

    # --- Вывод заданий (картинки) ---
    for i, q in enumerate(questions):
        st.markdown("---")
        st.subheader(f"Задание {i + 1}")

        # Проверка существования картинки
        if os.path.exists(q["image"]):
            st.image(q["image"], use_container_width=True)
        else:
            st.error(f"⚠️ Картинка '{q['image']}' не найдена в репозитории!")

        # Поле для ввода ответа
        user_input = st.text_input(
            "Ваш ответ:",
            value=st.session_state.answers[i],
            key=f"q_{i}"
        )
        st.session_state.answers[i] = user_input.strip()

    st.markdown("---")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Завершить тест", type="primary"):
            st.session_state.test_finished = True
            st.rerun()
    with col2:
        if st.button("🔄 Обновить таймер"):
            st.rerun()

else:
    # --- ЭКРАН РЕЗУЛЬТАТОВ ---
    name = st.session_state.name.strip() or "Участник"
    correct_count = 0
    wrong_count = 0
    no_answer_count = 0
    total_score = 0

    st.success("Тест завершен!")
    st.subheader("Результаты и разбор заданий")

    for i, q in enumerate(questions):
        user_ans = st.session_state.answers[i].strip().lower()
        correct_ans = str(q["answer"]).strip().lower()

        is_correct = False
        if not user_ans:
            no_answer_count += 1
            status_emoji = "⚪"
        elif user_ans == correct_ans:
            correct_count += 1
            total_score += q["points"]
            is_correct = True
            status_emoji = "✅"
        else:
            wrong_count += 1
            status_emoji = "❌"

        # Выпадающий блок для каждого вопроса
        with st.expander(f"{status_emoji} Задание {i + 1} | Ваш ответ: {user_ans or '(нет ответа)'}"):
            if os.path.exists(q["image"]):
                st.image(q["image"], width=300)
            st.write(f"**Правильный ответ:** {q['answer']}")
            if not is_correct:
                st.info(f"**Пояснение:** {q['explanation']}")

    percent = round((total_score / max_points) * 100, 1) if max_points > 0 else 0

    st.markdown("---")
    st.markdown(f"""### Итоги, {name}:
* **Точность:** {percent}%
* **Заданий верно решено:** {correct_count}
* **Заданий неверно решено:** {wrong_count}
* **Нет ответа:** {no_answer_count}
* **Ваш балл:** {total_score} из {max_points}""")

    if st.button("Начать заново"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()