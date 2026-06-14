# PROJECT_STATE.md

Текущий снимок состояния проекта `assistant-core`.

Дата фиксации: 2026-06-14
Репозиторий: `BigBoySG/assistent-core`

## Назначение проекта

`assistant-core` — это ядро личного ассистента, оформленное как Python-библиотека. Идея проекта: вынести основную бизнес-логику в отдельный пакет, чтобы потом подключать к нему разные интерфейсы:

- CLI;
- Telegram-бот;
- веб-сервис;
- тесты;
- другие внешние адаптеры.

Главный принцип: интерфейсы не должны знать про детали хранения данных и внутреннюю сборку зависимостей. Они должны работать через публичную точку входа ядра.

## Что уже готово

### 1. Python package

Проект уже оформлен как Python-пакет с `src`-layout.

В `pyproject.toml` уже есть:

- имя пакета: `assistant-core`;
- версия: `0.1.0`;
- описание: `Core package for personal assistant`;
- требование Python: `>=3.11`;
- настройка `pythonpath = ["src"]`;
- настройка `testpaths = ["tests"]`;
- dev-зависимость `pytest>=8`.

### 2. Главная точка входа

Есть файл:

```text
src/assistant_core/core.py
```

В нём есть класс:

```python
class AssistantCore:
    def __init__(self, tasks: TasksApi) -> None:
        self.tasks = tasks
```

То есть ядро уже имеет центральный объект, через который внешний код может получать доступ к подсистемам ядра.

### 3. Composition factory

Есть файл:

```text
src/assistant_core/composition/factory.py
```

В нём есть функция:

```python
def create_assistant_core() -> AssistantCore:
    ...
```

Она собирает зависимости по цепочке:

```text
MemoryTaskRepository
→ TaskService
→ TasksApi
→ AssistantCore
```

Это правильное место, где указывается, что сейчас используется именно `MemoryTaskRepository`.

### 4. Публичный экспорт пакета

Есть файл:

```text
src/assistant_core/__init__.py
```

Он экспортирует:

```python
create_assistant_core
TaskPriority
TaskStatus
```

То есть внешний код уже может импортировать основные элементы напрямую из `assistant_core`.

### 5. Доменная сущность Task

Есть файл:

```text
src/assistant_core/domain/entities/task.py
```

Сущность `Task` уже реализована через `dataclass`.

У задачи есть поля:

- `title`;
- `id`;
- `description`;
- `status`;
- `priority`;
- `created_at`;
- `completed_at`;
- `updated_at`.

Что уже хорошо:

- `id` создаётся через `uuid4`;
- даты создаются в UTC;
- пустой `title` запрещён;
- `title` очищается через `strip()`;
- пустое описание превращается в `None`;
- проверяется тип `TaskStatus`;
- проверяется тип `TaskPriority`.

### 6. Статусы и приоритеты задач

Есть файл:

```text
src/assistant_core/domain/enums.py
```

Готовые статусы:

```python
TaskStatus.ACTIVE
TaskStatus.DONE
TaskStatus.CANCELLED
```

Готовые приоритеты:

```python
TaskPriority.LOW
TaskPriority.MEDIUM
TaskPriority.HIGH
```

### 7. Бизнес-методы задачи

В `Task` уже есть методы:

```python
complete()
reopen()
cancel()
rename()
change_description()
change_priority()
```

Важные правила:

- завершённая задача получает статус `DONE`;
- при завершении ставится `completed_at`;
- при изменениях обновляется `updated_at`;
- завершённую задачу нельзя редактировать;
- отменённую задачу нельзя редактировать;
- завершённую задачу нельзя отменить.

Вопрос, который ещё надо явно решить: можно ли делать `reopen()` для отменённой задачи.

### 8. Порт TaskRepository

Есть файл:

```text
src/assistant_core/ports/task_repository.py
```

Абстрактный репозиторий описывает контракт:

```python
save(task)
get_by_id(task_id)
get_list_all()
get_list_active()
delete_by_id(task_id)
delete_all()
```

Это значит, что сервис задач зависит от абстракции, а не от конкретного способа хранения.

### 9. MemoryTaskRepository

Есть файл:

```text
src/assistant_core/infrastructure/persistence/memory/memory_task_repository.py
```

Репозиторий хранит задачи в памяти:

```python
self._tasks: dict[str, Task] = {}
```

Готовые операции:

- сохранить задачу;
- получить задачу по id;
- получить все задачи;
- получить активные задачи;
- удалить задачу по id;
- удалить все задачи.

Важно: это временное хранилище. После перезапуска процесса данные исчезают.

### 10. TaskService

Есть файл:

```text
src/assistant_core/application/services/task_service.py
```

Сервис уже работает через `TaskRepository` и умеет:

```python
create_task()
get_task()
get_all_tasks()
get_active_tasks()
delete_task()
delete_all_tasks()
complete_task()
reopen_task()
cancel_task()
rename_task()
change_task_description()
change_task_priority()
```

Если задача не найдена, сервис выбрасывает `TaskNotFoundError`.

### 11. TasksApi

Есть файл:

```text
src/assistant_core/application/api/tasks_api.py
```

Это внешний API для работы с задачами через `core.tasks`.

Готовые методы:

```python
create()
get()
get_all()
get_active()
delete()
clear()
complete()
reopen()
cancel()
rename()
change_description()
change_priority()
```

Сейчас API возвращает доменные объекты `Task` напрямую. На текущем этапе это нормально. DTO пока можно не вводить.

### 12. Исключения

Есть файл:

```text
src/assistant_core/exceptions.py
```

Готовые исключения:

```python
AssistantCoreError
TaskNotFoundError
InvalidTaskOperationError
```

## Текущая архитектура

Основная цепочка зависимостей:

```text
create_assistant_core()
        ↓
AssistantCore
        ↓
core.tasks
        ↓
TasksApi
        ↓
TaskService
        ↓
TaskRepository
        ↓
MemoryTaskRepository
```

Смысл слоёв:

```text
domain         — сущности, enum, бизнес-правила;
ports          — абстрактные интерфейсы;
application    — сервисы и API сценариев;
infrastructure — конкретные реализации хранения;
composition    — сборка зависимостей;
core.py        — главная точка входа.
```

## Что пока не готово

### 1. Тесты

Тестовая инфраструктура в `pyproject.toml` уже заявлена, но тесты ещё надо написать.

Нужны минимум:

```text
tests/test_task_entity.py
tests/test_task_service.py
tests/test_tasks_api.py
tests/test_factory.py
```

### 2. Постоянное хранение данных

Сейчас есть только `MemoryTaskRepository`.

Позже понадобится одно из постоянных хранилищ:

- `JsonTaskRepository`;
- `SQLiteTaskRepository`;
- `PostgresTaskRepository`.

Для ближайшего развития лучше выбрать SQLite, но только после тестов.

### 3. DTO / сериализация

Сейчас внешний API возвращает доменные объекты напрямую.

Это можно оставить на первом этапе, но позже понадобится решить:

- оставляем доменные объекты публичными;
- или добавляем `TaskDTO` / `TaskView`;
- или добавляем методы сериализации.

### 4. Пользователи и владельцы задач

Пока задачи не привязаны к пользователю.

Это нормально для ядра первого этапа. Пользователей лучше добавлять после стабилизации задач.

### 5. Интерфейсы

Пока не подключены:

- Telegram-бот;
- веб-интерфейс;
- CLI.

Их не стоит делать до тестов ядра.

## Ближайший правильный шаг

Следующий шаг — написать тесты и зафиксировать поведение текущего ядра.

Приоритет:

```text
1. tests/test_task_entity.py
2. tests/test_task_service.py
3. tests/test_tasks_api.py
4. tests/test_factory.py
```

## Минимальный чек-лист тестов

### Task entity

- создаётся задача с нормальным названием;
- title очищается от пробелов;
- пустой title вызывает `InvalidTaskOperationError`;
- пустое description превращается в `None`;
- status по умолчанию `ACTIVE`;
- priority по умолчанию `MEDIUM`;
- `complete()` переводит задачу в `DONE`;
- `complete()` ставит `completed_at`;
- `reopen()` возвращает задачу в `ACTIVE`;
- `cancel()` переводит задачу в `CANCELLED`;
- нельзя редактировать `DONE` задачу;
- нельзя редактировать `CANCELLED` задачу;
- нельзя отменить `DONE` задачу;
- нельзя передать status не типа `TaskStatus`;
- нельзя передать priority не типа `TaskPriority`.

### TaskService

- создаёт задачу;
- получает задачу по id;
- выбрасывает `TaskNotFoundError` для неизвестного id;
- возвращает все задачи;
- возвращает только активные задачи;
- удаляет задачу;
- выбрасывает `TaskNotFoundError` при удалении неизвестной задачи;
- очищает все задачи;
- завершает задачу;
- переоткрывает задачу;
- отменяет задачу;
- переименовывает задачу;
- меняет описание;
- меняет приоритет.

### TasksApi

- `core.tasks.create()` создаёт задачу;
- `core.tasks.get()` получает задачу;
- `core.tasks.get_all()` возвращает список;
- `core.tasks.get_active()` возвращает активные задачи;
- `core.tasks.complete()` завершает задачу;
- `core.tasks.reopen()` открывает задачу;
- `core.tasks.cancel()` отменяет задачу;
- `core.tasks.rename()` меняет название;
- `core.tasks.change_description()` меняет описание;
- `core.tasks.change_priority()` меняет приоритет;
- `core.tasks.delete()` удаляет задачу;
- `core.tasks.clear()` очищает задачи.

### Factory

- `create_assistant_core()` возвращает `AssistantCore`;
- у ядра есть `core.tasks`;
- через `core.tasks.create()` можно создать задачу;
- созданную задачу можно получить через `core.tasks.get()`.

## Что не делать прямо сейчас

Пока не надо:

- делать Telegram-бота;
- делать сайт;
- подключать базу данных;
- добавлять пользователей;
- вводить DTO;
- делать авторизацию;
- усложнять архитектуру.

Сначала надо покрыть тестами уже готовое поведение.

## Текущая оценка готовности

```text
MVP ядра задач: 70–75%
Архитектура библиотеки: 60–65%
Готовность к подключению Telegram/сайта: 40–50%
```

Главная причина, почему не выше: пока нет подтверждённого тестового покрытия и постоянного хранилища.

## Следующая команда для разработки

После клонирования репозитория:

```bash
pip install -e .[dev]
pytest
```

Затем создать первые тесты:

```bash
mkdir -p tests
touch tests/test_task_entity.py
```

И начать с тестов на `Task`.
