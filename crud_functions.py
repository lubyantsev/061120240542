import sqlite3


# Инициализация базы данных
def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        image_url TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# Получение всех продуктов
def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, description, price, image_url FROM products')
    products = cursor.fetchall()

    conn.close()
    return products


# Заполнение базы данных примерными данными
def seed_db():
    products = [
        ('Витамин A', 'Витамин A помогает поддерживать здоровье глаз и кожи.', 100, 'https://i.pinimg.com/736x/e5/de/94/e5de9481f54df4a712525431338c3497.jpg'),
        ('Витамин C', 'Витамин C помогает укреплять иммунную систему.', 150, 'https://images.squarespace-cdn.com/content/v1/607773ecd359161f2364e7c9/1622838803922-WEOBACY2T9I8AHFQPDGJ/vitaminC.png'),
        ('Витамин D', 'Витамин D важен для здоровья костей и зубов.', 200, 'https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_728,h_389/https://www.medicynanaroda.ru/wp-content/uploads/2017/11/v-kakix-produktax-soderzhitsya-vitamin-d.jpg'),
        ('Витамин E', 'Витамин E является мощным антиоксидантом.', 250, 'https://avatars.mds.yandex.net/i?id=cf694584172248a40c4d1bc3fdb4832e_l-10355200-images-thumbs&n=13'),
    ]

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Очистка таблицы перед заполнением, если это необходимо
    cursor.execute('DELETE FROM products')

    cursor.executemany('''
        INSERT INTO products (name, description, price, image_url)
        VALUES (?, ?, ?, ?)
        ''', products)

    conn.commit()
    conn.close()


# Пример использования функций
if __name__ == "__main__":
    initiate_db()
    seed_db()
    all_products = get_all_products()
    for product in all_products:
        print(product)