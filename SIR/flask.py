import tkinter as tk
import sqlite3

# إنشاء اتصال بقاعدة البيانات
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# وظيفة للبحث عن سؤال
def search_question():
    query = search_entry.get()
    algorithm = algorithm_var.get()
    if query:
        if algorithm == "Boolean":
            cursor.execute('SELECT id, question, answer FROM questions WHERE question LIKE ?', ('%' + query + '%',))
        elif algorithm == "Extended Boolean":
            cursor.execute('SELECT id, question, answer FROM questions WHERE question LIKE ?', ('%' + query + '%',))
        elif algorithm == "Vector Space":
            cursor.execute('SELECT id, question, answer FROM questions WHERE question LIKE ?', ('%' + query + '%',))
        results = cursor.fetchall()
        display_results(results, query)

# وظيفة لعرض نتائج البحث
def display_results(results, query):
    for widget in results_frame.winfo_children():
        widget.destroy()  # إزالة العناصر السابقة
    if results:
        for id, question, answer in results:
            # تمييز الكلمة في النتائج
            highlighted_question = question.replace(query, f"{query}", 1)  # تمييز الكلمة المدخلة
            result_frame = tk.Frame(results_frame, bg="#ffffff", pady=10, padx=10, borderwidth=1, relief="raised")
            result_frame.pack(fill='x', padx=10, pady=5)

            question_label = tk.Label(result_frame, text=highlighted_question, bg="#ffffff", font=("Helvetica", 12, "bold"), fg="#333333")
            question_label.pack(anchor='w')

            more_button = tk.Button(result_frame, text="Show More", command=lambda a=answer: show_answer(a), bg="#4db6ac", fg="white", font=("Helvetica", 10, "bold"))
            more_button.pack(side='right', padx=5)

# وظيفة لعرض الإجابة الكاملة
def show_answer(answer):
    answer_window = tk.Toplevel(window)
    answer_window.title("Answer")
    answer_window.geometry("400x300")
    answer_window.configure(bg="#b2ebf2")

    answer_label = tk.Label(answer_window, text=answer, wraplength=350, justify="left", bg="#b2ebf2", font=("Helvetica", 12))
    answer_label.pack(pady=10, padx=10)

    close_button = tk.Button(answer_window, text="Close", command=answer_window.destroy, bg="#f44336", fg="white", font=("Helvetica", 10, "bold"))
    close_button.pack(pady=10)

# إنشاء الصفحة الرئيسية للبحث
def create_search_page():
    global search_entry, results_frame, algorithm_var
    search_frame = tk.Frame(window, bg="#b2ebf2", padx=10, pady=10)
    search_frame.grid(row=0, column=0, sticky="nsew")

    search_label = tk.Label(search_frame, text="Search for a Question:", bg="#b2ebf2", font=("Helvetica", 14, "bold"), fg="#333333")
    search_label.pack(pady=10)

    search_entry = tk.Entry(search_frame, width=60, font=("Helvetica", 12), borderwidth=2, relief="groove")
    search_entry.pack(pady=5)

    algorithm_label = tk.Label(search_frame, text="Select Retrieval Algorithm:", bg="#b2ebf2", font=("Helvetica", 12, "bold"), fg="#333333")
    algorithm_label.pack(pady=5)

    algorithm_var = tk.StringVar(value="Boolean")
    algorithms = ["Boolean", "Extended Boolean", "Vector Space"]
    for algorithm in algorithms:
        alg_radio = tk.Radiobutton(search_frame, text=algorithm, variable=algorithm_var, value=algorithm, bg="#b2ebf2", font=("Helvetica", 10))
        alg_radio.pack(anchor='w')

    search_button = tk.Button(search_frame, text="Search", command=search_question, bg="#2196f3", fg="white", font=("Helvetica", 12, "bold"))
    search_button.pack(pady=10)

    results_frame = tk.Frame(window, bg="#b2ebf2", padx=10, pady=10)
    results_frame.grid(row=1, column=0, sticky="nsew")

# إعداد نافذة التطبيق
window = tk.Tk()
window.title("Q&A Search Page")
window.geometry("800x600")
window.configure(bg="#b2ebf2")

# توسيط محتويات الصفحة
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

create_search_page()  # إنشاء الصفحة الرئيسية عند بدء التطبيق

# تشغيل النافذة
window.mainloop()

# إغلاق الاتصال عند الخروج
conn.close()