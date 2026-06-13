from assistant_core import create_assistant_core

assistant = create_assistant_core()

task = assistant.tasks.create("Купить батарейки", description="Для занятия по робототехнике")

print("Создана задача:")
print(task)

print("\nВсе задачи:")
for item in assistant.tasks.get_list():
    print(f"- {item.title} [{item.status.value}]")

assistant.tasks.complete(task.id)

print("\nПосле завершения:")
for item in assistant.tasks.get_list():
    print(f"- {item.title} [{item.status.value}]")