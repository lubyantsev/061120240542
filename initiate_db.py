from crud_functions import initiate_db, seed_db

if __name__ == '__main__':
    initiate_db()  # Создаем таблицу перед добавлением данных
    seed_db()