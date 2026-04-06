import streamlit as st
import time
import os
import streamlit.components.v1 as components

# === НАСТРОЙКИ ТЕСТА ===
TIME_LIMIT = 5 * 60  # Время в секундах (5 минут)

questions = [
    {"image": "1.png", "answer": "ромб", "explanation": "Ответ: ромб. 1. FEGH - параллелограмм. 2. FC=GD, CH=DH, ∠C=∠D следовательно CFH=DHG, тогда FH=GH. 3. Параллелограмм, у которого смежные стороны равны - ромб.", "points": 1},
    {"image": "2.png", "answer": "8", "explanation": "Ответ: 8. 1. ∠BCD=30°, тогда ∠C=60°, следовательно трапеция равнобедренная. 2. ∠B=120°, ∠ABC=∠ACB=30° следовательно треугольник АВС равнобедренный, тогда AC=AB=BD=x, CD=2x (∠BCD=30°). 3. 20=5x, x=4, 2x=CD=8.", "points": 1},
    {"image": "3.png", "answer": "120", "explanation": "Ответ: 120. Сумма углов, прилежащих к боковой стороне, равна 180°. 180-60=120.", "points": 1},
    {"image": "4.png", "answer": "60", "explanation": "Ответ: 60. В равнобедренной трапеции углы при каждом основании равны.", "points": 1},
    {"image": "5.png", "answer": "15", "explanation": "Ответ: 15. В равнобедренной трапеции диагонали равны.", "points": 1},
    {"image": "6.png", "answer": "6", "explanation": "Ответ: 6. В равнобедренной трапеции СЕ = DF. Тогда CE=(24-12)/2.", "points": 1},
    {"image": "7.png", "answer": "равнобедренная", "explanation": "Ответ: Равнобедренная. Боковые стороны равны - равнобедренная.", "points": 1},
    {"image": "8.png", "answer": "10", "explanation": "Ответ: 10. Из формулы m=(a+b)/2, где m средняя линия, получаем AB=(20-15)*2.", "points": 1},
    {"image": "9.png", "answer": "5", "explanation": "Ответ: 5. Длина отрезка, соединяющего середины диагоналей трапеции, равна полуразности оснований. (20-10)/2=5.", "points": 1},
    {"image": "10.png", "answer": "108", "explanation": "Ответ: 108. S=(a+b)/2 * h.", "points": 1},
    {"image": "11.png", "answer": "6", "explanation": "Ответ: 6. h = c * sin(α).", "points": 1},
    {"image": "12.png", "answer": "40", "explanation": "Ответ: 40. S = m * h, m - средняя линия.", "points": 1},
    {"image": "13.png", "answer": "50", "explanation": "Ответ: 50. S = 1/2 * d1 * d2 * sin(φ).", "points": 1},
    {"image": "14.png", "answer": "прямоугольная", "explanation": "Ответ: Прямоугольная.", "points": 1}
]

max_points = sum(q["points"] for q in questions)

# === ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ ===
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'test_finished' not in st.session_state:
    st.session_state.test_finished = False
if 'saved_answers' not in st.session_state:
    st.session_state.saved_answers = [""] * len(questions)
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# === ИНТЕРФЕЙС ===
st.title("Устный счет: Трапеция")

if not st.session_state.test_finished:
    # Расчет оставшегося времени в Python
    elapsed = time.time() - st.session_state.start_time
    remaining_seconds = int(TIME_LIMIT - elapsed)

    if remaining_seconds <= 0:
        st.warning("Время вышло! Пожалуйста, нажмите кнопку 'Завершить тест' внизу страницы, чтобы увидеть результат.")
        remaining_seconds = 0

    # Плавный таймер на JavaScript (не перезагружает страницу)
    components.html(
        f"""
        <div id="timer" style="font-size:20px; font-family:sans-serif; padding:15px; border-radius:8px; background-color:#f0f2f6; color:#ff4b4b; text-align:center; font-weight:bold; margin-bottom: 20px;">
        </div>
        <script>
        var remaining = {remaining_seconds};
        var timerElement = document.getElementById("timer");
        
        var x = setInterval(function() {{
            if (remaining <= 0) {{
                clearInterval(x);
                timerElement.innerHTML = "⏳ Время вышло! Нажмите Завершить тест.";
            }} else {{
                var m = Math.floor(remaining / 60);
                var s = remaining % 60;
                timerElement.innerHTML = "⏱️ Осталось времени: " + m + "м " + s + "с";
                remaining -= 1;
            }}
        }}, 1000);
        </script>
        """, 
        height=80
    )

    # Все задания обернуты в форму, чтобы не терять фокус при вводе
    with st.form("quiz_form"):
        user_name = st.text_input("Введите ваше имя:", value=st.session_state.user_name)

        for i, q in enumerate(questions):
            st.markdown(f"### Задание {i + 1}")
            
            # Картинки теперь компактные (width=350)
            if os.path.exists(q["image"]):
                st.image(q["image"], width=350)
            else:
                st.error(f"⚠️ Картинка '{q['image']}' не найдена!")

            # Уникальный ключ для каждого ответа внутри формы
            st.text_input("Ваш ответ:", key=f"ans_{i}")
            st.markdown("---")

        submitted = st.form_submit_button("Завершить тест", type="primary")

        if submitted:
            # При нажатии кнопки мы надежно копируем все ответы в сессию
            st.session_state.user_name = user_name
            for i in range(len(questions)):
                st.session_state.saved_answers[i] = st.session_state[f"ans_{i}"]
            
            st.session_state.test_finished = True
            st.rerun()

else:
    # === ЭКРАН РЕЗУЛЬТАТОВ ===
    name = st.session_state.user_name.strip() or "Участник"
    correct_count = 0
    wrong_count = 0
    no_answer_count = 0
    total_score = 0

    st.success("Тест завершен!")
    st.subheader("Результаты и разбор заданий")

    for i, q in enumerate(questions):
        # Берем сохраненные ответы
        user_ans = st.session_state.saved_answers[i].strip().lower()
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
                st.image(q["image"], width=250) # На результатах картинки еще меньше
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

    # Кнопка начать заново (очищает всю память)
    if st.button("Начать заново", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
