from assistant_core import create_assistant_core

assistant = create_assistant_core()

task = assistant.create_task("Купить батарейки", description="Для занятия по робототехнике")

print("Создана задача:")
print(task)

print("\nВсе задачи:")
for item in assistant.get_all_tasks():
    print(f"- {item.title} [{item.status.value}]")

assistant.complete_task(task.id)

print("\nПосле завершения:")
for item in assistant.get_all_tasks():
    print(f"- {item.title} [{item.status.value}]")