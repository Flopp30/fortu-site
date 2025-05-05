### Запуск

#### Docker
1. Запустить сервисы 
   ```sh
   docker compose up -d
   ```
   
#### Локально
1. Переменные окружения (создание файлы)
    ```sh 
    cp .env.sample .env
    ```
2. Загрузка переменных
    ```sh
   source load_env.sh
   ```
3. Установка зависимостей
   ```sh
    poetry install
    ```
4. Поднять БД
    ```sh
   docker compose up db
   ```
5. Провести миграции
    ```sh
   make migrate
   ```
6. Линтер
    ```sh
   make lint
   ```
7. Запустить сервер
    ```sh
   make run
   ```