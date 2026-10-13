# Сервис Управления Студентами

## Демонстрация

Демонстрацию можно найти [здесь](https://bsu-famcs-students-application.vercel.app/)

## Описание

Полноценное приложение для управления оценками студентов. В настоящее время можно управлять только одним списком студентов. Приложение разделено на три основные части:

1. Сервер
2. CLI-приложение
3. Фронтенд

## Требования

1. Активный проект в Google Cloud
2. Google Cloud Bucket (например, `students-management`) с загруженным файлом `students.csv` (должен быть установлен публичный доступ)
3. Google Cloud Service Account (роль `Storage Owner` должна быть выдана)
4. Google Cloud Service Account ключ должен быть сохранен в `./backend/keys/gcloud.json`
5. Обновите константы в файле `./backend/main.py` в соответствии с вашим проектом Google Cloud (`BUCKET_NAME`, `FILE_PATH`)
6. Обновите константы в файле `./frontend/src/constants/api.ts` в соответствии с вашей конфигурацией API

## Сервер

### Стек технологий

- FastAPI
- Пакет google-cloud-storage
- Uvicorn

### Локальная разработка

Для запуска локального сервера используйте Uvicorn:

```
uvicorn backend.main:app
```

### Процесс развертывания

Для развертывания можно использовать файл `./backend/Dockerfile`. Например, вы можете легко задействовать Google Cloud Run для развертывания Docker-контейнера (с помощью Cloud Build для интеграции с репозиторием Github).

## CLI-приложение

### Стек технологий

- Python
- Пакет google-cloud-storage

### Локальная разработка

Запустите CLI-модуль:

```
python -m backend.cli
```

## Фронтенд

### Стек технологий

- React
- Tailwind
- shadcn/ui
- TanStack Query
- PNPM

### Локальная разработка

Установите зависимости и запустите React-приложение с помощью pnpm:

```
pnpm i && pnpm run dev
```

### Процесс развертывания

Вы можете использовать Vercel для развертывания и интеграции с репозиторием Github.

## Полная инструкция

1. Клонируем репозиторий

```
git@github.com:daniilkananenka/bsu-famcs-students-application.git
```

2. Создаем проект [Google Cloud](https://console.cloud.google.com/projectcreate)
3. Создаем [Google Cloud Storage Bucket](https://console.cloud.google.com/storage/create-bucket) с конфигурацией:

   - Name - `bsu-famcs-students-application-1`
   - Region - `Region - europe-west-1`
   - Убрать галочку с `Enforce public access prevention`
   - Access Control - `Fine-grained`

4. В созданый Google Cloud Storage Bucket загружаем файл `students.csv` (храниться в `data/students.csv`)
5. Открываем публичный доступ к загруженному файлу `students.csv`. Для этого:
   - Внутри бакета, справа от файла нажимаем кнопку в виде трех точек и выбираем пункт Edit Access
   - Добавляем новый entry - `Public - allUsers - Reader`
6. Создаем новый [сервисный аккаунт](https://console.cloud.google.com/iam-admin/serviceaccounts/create). Для этого:
   - Нажимаем Grant Access
   - Вводим название (например `bsu-famcs-students-application-storage-user`)
   - В качестве роли выбираем `Storage Object User`
7. Экспортируем ключ JSON для сервисного аккаунта. Для этого:
   - Справа от сервисного аккаунта нажимаем кнопку в виде трех точек и выбираем пункт Manage Keys
   - Нажимаем кнопку `Add key` - `Create new key` - `JSON`
8. Сохраняем ключ в виде файла локально в проекте `./backend/keys/gcloud.json`
9. Обновляем конфигурацию бакета в файле `main.py` и `cli.py`:
   - `BUCKET_NAME` - `bsu-famcs-students-application-1`
10. Сохраняем весь проект в отдельном репозитории
11. Деплоим на [Cloud Run](https://console.cloud.google.com/run/create). Для этого:
    - Выбираем опцию `Continuosly Deploy from a repository`
    - Выбираем опцию `Cloud Build`
    - В открывшемся окне выбираем репозиторий и ветку, на которой храниться код, а в качестве пути к Dockerfile указываем `/backend/Dockerfile`
    - Остальные настройки оставляем по умолчанию
    - Нажимаем Create. Google Cloud теперь будет автоматически деплоить новый контейнер при обновлении репозитория
12. Берем URL задеплоенного сервера (например `https://bsu-famcs-students-application.europe-west1.run.app/`) и изменяем конфигурацию фронтенда в файле `./frontend/src/constants/api.ts` (константа `API_BASE_URL`)
13. Деплоим на [Vercel](https://vercel.com/). Для этого:
    - Создаем аккаунт
    - На странице проекта нажимаем кнопку `Add New...` - `Project`
    - Выбираем репозиторий в котором находиться проект
    - На странице конфигурации в качестве директории проекта выбираем `./frontend`
    - Нажимаем кнопку `Deploy`
14. Теперь у вас есть задеплоенный FastAPI сервер и React фронтенд. Для управления данными необходимо локально находясь в корне репозитория запустить команду `python -m backend.cli` и следовать указаниям в консоли
