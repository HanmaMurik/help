import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)

sql = connection.cursor()


sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER,'
            'name TEXT,'
            'num TEXT,'
            'loc TEXT);')

sql.execute('CREATE TABLE IF NOT EXISTS products'
            '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT,'
            'pr_amount INTEGER,'
            'pr_price REAL,'
            'pr_des TEXT,'
            'pr_photo TEXT);')

sql.execute('CREATE TABLE IF NOT EXISTS cart'
            '(user_id INTEGER,'
            'user_product TEXT,'
            'product_quantity INTEGER,'
            'total REAL);')


def register(id, name, num, loc):

    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, num, loc))
    connection.commit()

def checker(id):

    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))

    if check.fetchone():
        return True
    else:
        return False

def add_product(pr_name, pr_amount, pr_price, pr_des, pr_photo):

    sql.execute('INSERT INTO products'
                '(pr_name,'
                'pr_amount,'
                'pr_price,'
                'pr_des,'
                'pr_photo) VALUES (?,?,?,?,?);',
                (pr_name, pr_amount, pr_price, pr_des, pr_photo))

    connection.commit()

def show_info(pr_id):

    sql.execute('SELECT pr_name, pr_amount, pr_price, pr_des, pr_photo FROM products WHERE id=?;', (pr_id,)).fetchone()

def show_all_products():

    all_products = sql.execute('SELECT * FROM products;')
    return all_products.fetchall()

def get_pr_name_id():

    products = sql.execute('SELECT id, pr_name, pr_amount FROM products;').fetchall()
    return products

def get_pr_id():
    prods = sql.execute('SELECT pr_name, id, pr_amount FROM products;').fetchall()
    sorted_prods = [i[0] for i in prods if i[2] > 0]
    return sorted_prods

def add_to_cart(user_id, pr_name, pr_quantity, user_total=0):
    sql.execute('INSERT INTO cart(user_id, user_product, product_quantity, total) VALUES(?,?,?,?);', (user_id, pr_name, pr_quantity, user_total))

    amount = sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (pr_name,)).fetchone()
    sql.execute(f'UPDATE products SET pr_amount={amount[0] - pr_quantity}' f'WHERE pr_name=?;', (pr_name,))

    connection.commit()

def del_cart(user_id):
    pr_name = sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    amount = sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (pr_name,)).fetchone()
    pr_quantity = sql.execute('SELECT product_quantity FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    sql.execute(f'UPDATE products SET pr_amount={amount[0] + pr_quantity}' f'WHERE pr_name=?;', (pr_name,))

    connection.commit()
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    connection.commit()

def show_cart(user_id):
    cart = sql.execute('SELECT user_product, product_quantity, total FROM cart WHERE user_id=?;', (user_id,))
    return cart.fetchone()

