from  pyswip import Prolog
import json

# ----------------------------
# AI Task Manager (Main File)
# ----------------------------

# 1️⃣ تحميل البيانات من ملف JSON
with open("tasks.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 2️⃣ إنشاء كائن بروولوج
prolog = Prolog()

# 3️⃣ تحميل ملف القواعد
prolog.consult("ai_task_manager.pl")

# 4️⃣ إرسال المهام إلى بروولوج كحقائق
for task in data["tasks"]:
    name = task["name"]
    priority = task["priority"]
    duration = task["duration"]
    prolog.assertz(f"task('{name}', {priority}, {duration})")

# 5️⃣ مثال: تنفيذ استعلام
for result in prolog.query("best_task(Task)."):
    print("أفضل مهمة:", result["Task"])
