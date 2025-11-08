import streamlit as st 
import random

# --------------------------
# بيانات داخلية لتوليد الأسئلة
# --------------------------

concepts = [
    "variables", "loops", "functions", "recursion", "OOP", "arrays",
    "conditions", "exceptions", "strings", "dictionaries"
]

mcq_templates = [
    ("What is the output of the following code?\n\n{code}\n\nA) {a}\nB) {b}\nC) {c}\nD) {d}\n", "A"),
    ("Which of the following is TRUE about {concept}?\nA) {a}\nB) {b}\nC) {c}\nD) {d}\n", "B")
]

true_false_templates = [
    ("{concept}: {statement} (True/False)", "True"),
    ("Is the following statement correct?\n{statement} (True/False)", "False")
]

debug_templates = [
    ("Find the error in this code and fix it:\n\n{code}", None),
    ("What will cause this code to crash?\n\n{code}", None)
]

# --------------------------
# دوال توليد البيانات
# --------------------------

def random_code_snippet():
    snippets = [
        "x = 5\nprint(x * 2)",
        "for i in range(3):\n    print(i)",
        "def add(a, b):\n    return a + b\nprint(add(2, 3))",
        "nums = [1, 2, 3]\nprint(nums[1])",
        "s = 'hello'\nprint(s.upper())"
    ]
    return random.choice(snippets)


def random_answers():
    return {
        "a": str(random.randint(1, 20)),
        "b": str(random.randint(1, 20)),
        "c": str(random.randint(1, 20)),
        "d": str(random.randint(1, 20)),
    }


def generate_mcq():
    template, correct = random.choice(mcq_templates)
    code = random_code_snippet()
    ans = random_answers()
    concept = random.choice(concepts)
    text = template.format(code=code, concept=concept, **ans)
    return text, correct


def generate_true_false():
    template, correct = random.choice(true_false_templates)
    statement = random.choice([
        "A loop always runs at least once",
        "A function can return multiple values",
        "Strings are immutable",
        "Python uses indentation to define blocks"
    ])
    concept = random.choice(concepts)
    text = template.format(concept=concept, statement=statement)
    return text, correct


def generate_debug():
    code = random.choice([
        "for i in range(5)\n    print(i)",
        "x = [1, 2, 3]\nprint(x[3])",
        "def f()\n    return 10",
        "print(unknown_var)"
    ])

    template = random.choice(debug_templates)

    if "{code}" in template[0]:
        text = template[0].format(code=code)
    else:
        text = template[0]

    return text, None


def generate_test(num_questions=5):
    questions = []
    for i in range(1, num_questions + 1):
        q_type = random.choice(["mcq", "tf", "debug"])

        if q_type == "mcq":
            q, a = generate_mcq()
        elif q_type == "tf":
            q, a = generate_true_false()
        else:
            q, a = generate_debug()

        questions.append((i, q, a))
    return questions


# --------------------------
# واجهة Streamlit + التصحيح
# --------------------------

st.title("✅ مولّد اختبارات برمجية تلقائيًا")
st.write("اضغط زر التوليد لإنشاء اختبار جديد بدون أي API خارجية.")

num = st.slider("عدد الأسئلة:", 3, 20, 7)

if st.button("✨ توليد اختبار"):
    questions = generate_test(num)

    user_answers = {}
    correct_answers = {}

    for idx, q, a in questions:
        st.subheader(f"Q{idx}")
        st.code(q)

        if a:  # أسئلة لها إجابة
            user_answers[idx] = st.text_input(f"إجابتك للسؤال {idx}:", key=f"ans_{idx}")
            correct_answers[idx] = a
        else:  # أسئلة Debug
            st.info("🔧 هذا السؤال للتصحيح ولا يحتاج إجابة.")
            correct_answers[idx] = None

        st.markdown("---")

    # ------------ زر التصحيح ------------
    if st.button("✅ تصحيح الإجابات"):
        st.subheader("نتيجة التصحيح:")

        progress = st.progress(0)  # شريط تقدم
        total = 0
        correct_count = 0
        total_questions = len(user_answers)

        for idx, qindex in enumerate(user_answers):
            user = user_answers[qindex].strip().lower()
            correct = correct_answers[qindex].strip().lower()

            if user == correct:
                st.success(f"✅ سؤال {qindex}: إجابة صحيحة!")
                correct_count += 1
            else:
                st.error(f"❌ سؤال {qindex}: إجابة خاطئة. الصحيحة هي: **{correct_answers[qindex]}**")

            total += 1
            progress.progress(int((idx + 1) / total_questions * 100))  # تحديث شريط التقدم

        # ------------ حساب الدرجة والنسبة ------------
        score = correct_count
        percentage = (correct_count / total) * 100 if total > 0 else 0

        st.write("---")
        st.subheader("📊 النتيجة النهائية")
        st.info(f"✅ الدرجة: **{score} / {total}**")
        st.info(f"📈 نسبة النجاح: **{percentage:.2f}%**")
