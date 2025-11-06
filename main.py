# استدعاء المكتبات المطلوبة
from pyswip import Prolog
import json
import os

# إنشاء كائن Prolog
prolog = Prolog()
current_path = os.getcwd()

# تحديد أسماء الملفات
json_file = f"tasks.json"
print(json_file)
prolog_file = "task_organizer.pl"

print(True if os.path.isfile(prolog_file) else False)
print(True if os.path.isfile(json_file) else False)


# تحميل المهام السابقة (لو الملف موجود)




# إدخال المهام من المستخدم
while True:
    print("\nأضف مهمة جديدة:")
    name = input("اسم المهمة: ")
    priority = input("الأولوية (High/Medium/Low): ")
    duration = input("المدة بالساعات: ")
    deadline = input("تاريخ الـ deadline (مثلاً 2025-11-05): ")

    new_task = {
        "name": name,
        "priority": priority,
        "duration": duration,
        "deadline": deadline
    }

    data["tasks"].append(new_task)
    print("✅ تمت إضافة المهمة بنجاح!")

    # حفظ البيانات في JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    more = input("هل تريد إضافة مهمة أخرى؟ (y/n): ").lower()
    if more != 'y':
        break

# كتابة المهام داخل ملف Prolog
with open(prolog_file, "w", encoding="utf-8") as f:
    for task in data["tasks"]:
        fact = f'task("{task["name"]}", "{task["priority"]}", {task["duration"]}, "{task["deadline"]}").\n'
        f.write(fact)

print(f"\n📄 تم تحديث ملف Prolog ({prolog_file}) بالمهام بنجاح!")

# ربط Python بملف Prolog
if os.path.exists(prolog_file):
    prolog.consult(prolog_file)
    print("✅ تم ربط Python بملف Prolog بنجاح!")

    # اختبار بسيط لاسترجاع المهام
    print("\n📋 استعلام من Prolog:")
    for result in prolog.query("task(Name, Priority, Duration, Deadline)"):
        print(f'🧠 {result["Name"]} | {result["Priority"]} | {result["Duration"]} | {result["Deadline"]}')
else:
    print("❌ لم يتم العثور على ملف ai_task_manager.pl")
