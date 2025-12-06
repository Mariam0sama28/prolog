// hate my life
document
  .getElementById("taskForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();           // ده من تشات مش فاهمة الباث باك ده 

    const name = document.getElementById("name").value.trim();
    const priority = document.getElementById("priority").value;
    const duration = document.getElementById("duration").value;
    const deadline = document.getElementById("deadline").value;

    if (name === "") {
      alert("write first task!");
      return;
    }

    // إرسال التاسك للباك إند
    const response = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, priority, duration, deadline }),
    });

    const data = await response.json();
    document.getElementById("msg").textContent = data.ok
      ? "Task added successfully!"
      : "Error adding task";

    loadTasks();
  });

// تحميل التاسكات من الباك إند
async function loadTasks() {
  const response = await fetch("/api/tasks");
  const data = await response.json();
  const tasks = data.tasks || [];

  const list = document.getElementById("tasksList");
  list.innerHTML = "";

  tasks.forEach((t, i) => {
    const li = document.createElement("li");
    li.textContent = `${t.name} - ${t.priority} - ${t.duration}h - ${t.deadline}`;

    // زرار حذف لكل مهمة
    const delBtn = document.createElement("button");
    delBtn.textContent = "X";
    delBtn.className = "btn danger";
    delBtn.onclick = async () => {
      await fetch(`/api/tasks/${i}`, { method: "DELETE" });
      loadTasks();
    };

    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

// زرار تحديث القائمة
document.getElementById("refreshBtn").addEventListener("click", loadTasks);

// زرار مسح كل المهام
document.getElementById("clearBtn").addEventListener("click", async () => {
  await fetch("/api/tasks", { method: "DELETE" });
  loadTasks();
});

// زرار توليد خطة من Prolog
document.getElementById("generatePlan").addEventListener("click", async () => {
  const response = await fetch("/api/plan");
  const data = await response.json();
  const plan = data.plan || [];

  const planCard = document.getElementById("planCard");
  const planList = document.getElementById("planList");
  planList.innerHTML = "";

  plan.forEach((p) => {
    const li = document.createElement("li");
    li.textContent = `${p.name} - ${p.priority} - ${p.duration}h - Day: ${p.day}`;
    planList.appendChild(li);
  });

  planCard.style.display = plan.length ? "block" : "none";
});

// تحميل القائمة عند بداية التشغيل
loadTasks();
