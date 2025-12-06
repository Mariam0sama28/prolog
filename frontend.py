from flask import Blueprint, Flask, jsonify, redirect, request, send_from_directory, url_for, render_template
import json, os
from pyswip import Prolog

bp = Blueprint('frontend', __name__)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "./static/tasks.json")
PROLOG_FILE = os.path.join(HERE, "./task_organizer.pl")  # الملف اللي فيه قواعد prolog

# تأكد من وجود ملف البيانات
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"tasks": []}, f, indent=2, ensure_ascii=False)

def read_tasks():
    try :
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            file= json.load(f)
            print(file)
            return file
    except:
        print('FILE_EMPTY')

def write_tasks(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@bp.get("/")
def index():
    return jsonify({"message": "Task added successfully!"})

@bp.route("/api/tasks", methods=["GET","POST","DELETE"])
def tasks():
    try :
        data = read_tasks()
        if request.method == "GET":
            print(data['tasks'])
            return render_template("index.html", tasks=data['tasks'])
        if request.method == "POST":
            body = request.get_json()
            data["tasks"].bpend(body)
            write_tasks(data)
            # أيضاً نحدّث ملف Prolog facts
            update_prolog_facts(data["tasks"])
            return jsonify({"ok": True})
        if request.method == "DELETE":
            # مسح كل المهام
            data["tasks"] = []
            write_tasks(data)
            update_prolog_facts(data["tasks"])
            return jsonify({"ok": True})
    except:
        return redirect(url_for(index))

@bp.route("/api/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    data = read_tasks()
    if 0 <= index < len(data["tasks"]):
        data["tasks"].pop(index)
        write_tasks(data)
        update_prolog_facts(data["tasks"])
    return jsonify({"ok": True})

@bp.route("/api/plan")
def plan():
    # استدعاء Prolog للحصول على الخطة
    prolog = Prolog()
    # تحميل ملف القواعد (task_organizer.pl) - تأكدي المسار صحيح
    prolog.consult(PROLOG_FILE)

    # assert كل المهام كـ facts داخل Prolog
    tasks = read_tasks().get("tasks", [])
    # أزل أي حقائق سابقة مؤقتة لو أردت (retractall)
    prolog.query("retractall(task(_,_,_,_))")
    for t in tasks:
        name = t.get("name", "").replace('"','\\"')
        priority = t.get("priority","low")
        duration = t.get("duration",0)
        deadline = t.get("deadline","none")
        q = f"assertz(task('{name}', {priority_literal(priority)}, {duration}, '{deadline}'))"
        # نجري الاستعلام
        list(prolog.query(q))

    # نفترض أن ملف Prolog يحتوي predicate اسمه build_schedule(Plan)
    # الذي يعيد قائمة من خرائط plan_item(Name, Priority, Duration, Day)
    plan_results = []
    for res in prolog.query("build_schedule(Plan)"):
        # Plan هنا صيغة Prolog; من الأفضل أن Prolog يطبع النتائج بطريقة يمكن لبايثون قراءتها
        plan_results = res.get("Plan", [])
        break

    # لتحويل نتائج Prolog البسيطة إلى JSON، سنفترض أن Prolog يولد facts output(Name,Priority,Duration,Day).
    # لذلك نستخدم استعلامات مباشرة:
    out = []
    for r in prolog.query("output(Name,Priority,Duration,Day)"):
        out.bpend({
            "name": r["Name"],
            "priority": str(r["Priority"]),
            "duration": r["Duration"],
            "day": r["Day"]
        })

    return jsonify({"plan": out})

def priority_literal(p):
    # تحويل النص إلى literal متوافق مع Prolog (مثال: high -> high)
    return p.lower()

def update_prolog_facts(tasks):
    # نحفظ ملف facts بسيط يمكن فتحه من Prolog أو للمراجعة
    with open(PROLOG_FILE, "w", encoding="utf-8") as f:
        f.write("% facts generated from tasks.json\n")
        for t in tasks:
            name = t.get("name","").replace("'", "\\'")
            priority = t.get("priority","low").lower()
            duration = t.get("duration",0)
            deadline = t.get("deadline","none")
            f.write(f"task('{name}', {priority}, {duration}, '{deadline}').\n")
