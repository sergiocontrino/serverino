import flask
from config import config
import psycopg2
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def connection():
    # read connection parameters
    params = config()
    con: connection = psycopg2.connect(**params)
    con.set_client_encoding('UTF8')
    con.autocommit = True
    return con


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API oops.</p>"


@app.errorhandler(404)
def show_message(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/users', methods=['GET'])
def api_all_users():
    """
    To show all users in the system (GET)
    :return: json list of all users
    """
    cur = connection().cursor()
    cur.execute('SELECT name, surname FROM reader order by 2;')
    all_readers = cur.fetchall()
    return jsonify(all_readers)


@app.route('/api/v1/user', methods=['GET'])
def api_filter_user():
    """
    To show specific user’s details (GET)

    http://127.0.0.1:5000/api/v1/user?id=3
    :return: json user's details
    """
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')
    surname = query_parameters.get('surname')

    query = "SELECT name, surname, address FROM reader WHERE"

    if id:
        query += " reader_id= " + id
    if name:
        query += " name = '" + name + "'"
    if surname:
        query += " surname = '" + surname + "'"

    if not (id or name or surname):
        return page_not_found(404)

    cur = connection().cursor()
    cur.execute(query)
    a_reader = cur.fetchall()

    return jsonify(a_reader)


@app.route('/api/v1/users', methods=['POST'])
def api_add_user():
    """"
    To add a new user (POST)

    curl -v -H "Content-Type: application/json" \
    -d '{"name":"carla","surname":"alba", "address":"capua"}' \
    http://127.0.0.1:5000/api/v1/users
    """

    try:
        _json = request.json
        _name = _json['name']
        _surname = _json['surname']
        _address = _json['address']
        if _name and _surname and _address and request.method == 'POST':
            cur = connection().cursor()
            sql = "INSERT INTO reader (name, surname, address) VALUES(%s, %s, %s);"
            data = (_name, _surname, _address)
            cur.execute(sql, data)
            connection().commit()
            response = jsonify('Reader added successfully')
            response.status_code = 200
            return response
        else:
            return show_message()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/users', methods=['PUT'])
def api_update_user():
    """
    To edit user’s information (PUT)

    curl -v -H "Content-Type: application/json" -X PUT
    -d '{"id":"3","name":"aldo","surname":"quattro", "address":"pula"}'
    http://127.0.0.1:5000/api/v1/users
    """
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _surname = _json['surname']
        _address = _json['address']
        if _name and _surname and _address and _id and request.method == 'PUT':
            sql = "UPDATE reader SET name='" + _name + "', surname='" + _surname + "', address='" +\
                       _address + "' WHERE reader_id=" + _id + ";"
            cur = connection().cursor()
            cur.execute(sql)
            connection().commit()

            response = jsonify('Reader updated successfully.')
            response.status_code = 200
            return response
        else:
            return show_message()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/users', methods=['DELETE'])
def api_delete_user():
    """
    To delete user (DELETE)

    curl -v -H "Content-Type: application/json" -X DELETE -d '{"id":"15"}'
    http://127.0.0.1:5000/api/v1/users

    TODO: add check if still holding books
    :return:
    """
    _json = request.json
    _id = _json['id']
    try:
        cur = connection().cursor()
        cur.execute("delete from reader where reader_id=" + _id + ";")

        connection().commit()
        response = jsonify('User deleted successfully!')
        response.status_code = 200
        return response

    except Exception as e:
        print("Cannot delete user " + _id + ": it holds books!")
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/books', methods=['POST'])
def api_add_book():
    """
    To add a new book to the system (POST)

    curl -v -H "Content-Type: application/json"
    -d '{"title":"Pride and prejudice","year":"1800", "author":"J. Austen"}'
    http://127.0.0.1:5000/api/v1/books
    """
    try:
        _json = request.json
        _title = _json['title']
        _year = _json['year']
        _author = _json['author']
        if _title and _year and _author and request.method == 'POST':
            cur = connection().cursor()
            sql = "INSERT INTO book (title, year, author) VALUES(%s, %s, %s);"
            data = (_title, _year, _author)
            cur.execute(sql, data)
            connection().commit()
            response = jsonify('Book added successfully')
            response.status_code = 200
            return response
        else:
            return show_message()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/books', methods=['GET'])
def api_all_books():
    """
    To get all books in the system (GET)
    :return: json list of all users
    """
    cur = connection().cursor()
    cur.execute('SELECT title, year, author FROM book order by 1;')
    all_readers = cur.fetchall()
    return jsonify(all_readers)


@app.route('/api/v1/book', methods=['GET'])
def api_filter_book():
    """
    To view a specific book detail (GET)

    http://127.0.0.1:5000/api/v1/book?id=3
    :return: json book's details
    """
    query_parameters = request.args

    id = query_parameters.get('id')
    title = query_parameters.get('title')

    query = "SELECT title, year, author FROM book WHERE"

    if id:
        query += " book_id= " + id
    if title:
        query += " title = '" + title + "'"

    if not (id or title):
        return page_not_found(404)

    cur = connection().cursor()
    cur.execute(query)
    a_reader = cur.fetchall()

    return jsonify(a_reader)


@app.route('/api/v1/books', methods=['PUT'])
def api_update_book():
    """
    To update a specific book detail

    curl -v -H "Content-Type: application/json" -X PUT
    -d '{"id":"3","title":"chez swan","year":"1880", "author":"proust"}'
    http://127.0.0.1:5000/api/v1/books
    :return:
    """
    try:
        _json = request.json
        _id = _json['id']
        _title = _json['title']
        _year = _json['year']
        _author = _json['author']
        # TODO: allow update of single field
        if _title and _year and _author and _id and request.method == 'PUT':
            sql = "UPDATE book SET title='" + _title + "', year='" + _year + "', author='" +\
                       _author + "' WHERE bokk_id=" + _id + ";"
            cur = connection().cursor()
            cur.execute(sql)
            connection().commit()

            response = jsonify('Book updated successfully.')
            response.status_code = 200
            return response
        else:
            return show_message()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/books', methods=['DELETE'])
def api_delete_book():
    """
    To delete a book

    curl -v -H "Content-Type: application/json" -X DELETE -d '{"id":"15"}'
    http://127.0.0.1:5000/api/v1/books
    :return:
    """
    _json = request.json
    _id = _json['id']
    try:
        cur = connection().cursor()
        cur.execute("delete from book where book_id=" + _id + ";")

        connection().commit()
        response = jsonify('Book deleted successfully!')
        response.status_code = 200
        return response

    except Exception as e:
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/books/search', methods=['GET'])
def api_search():
    """
    Search books by name (not strict search; Contain(), not Equal())
    Search books by author

    Note: implemented not strict search for both

    http://127.0.0.1:5000/api/v1/books/search?author=man
    :return: json list of books
    """

    query_parameters = request.args

    title = query_parameters.get('title')
    author = query_parameters.get('author')

    query = "SELECT * from book where "

    if title:
        query = query + "title like '%" + title + "%';"
    if author:
        query = query + "author like '%" + author + "%';"
    if not (title or author):
        return page_not_found(404)

    cur = connection().cursor()
    cur.execute(query)
    books = cur.fetchall()

    return jsonify(books)


@app.route('/api/v1/loans', methods=['GET'])
def api_loans():
    """
    See user’s book’s list

    http://127.0.0.1:5000/api/v1/loans?id=2
    :return: json list of books
    """
    query_parameters = request.args

    id = query_parameters.get('id')

    query = "SELECT b.book_id, b.title, b.year, b.author FROM book b, loan l WHERE reader_id ="
    if id:
        query += id + " and b.book_id = l.book_id;"
    else:
        return page_not_found(404)

    cur = connection().cursor()
    cur.execute(query)
    books = cur.fetchall()

    return jsonify(books)


@app.route('/api/v1/returns', methods=['POST'])
def api_del_loan():
    """
    Unassign (remove) book(s) from the user’s book’s list

    curl -v -H "Content-Type: application/json" -d '{"book_id":"2","reader_id":"2"}'
    http://127.0.0.1:5000/api/v1/returns
    :return:
    """
    try:
        _json = request.json
        _reader = _json['reader_id']
        _book = _json['book_id']
        if _reader and _book and request.method == 'POST':
            cur = connection().cursor()
            sql = "DELETE from loan where book_id IN (" + _book \
                  + ") AND reader_id in (" + _reader + ");"
            print("DDD", sql)
            cur.execute(sql)
            connection().commit()
            response = jsonify("Reader " + _reader + ": loan''s list update successfully.")
            response.status_code = 200
            return response
        else:
            return show_message()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/loans', methods=['POST'])
def api_add_loan():
    """
    Assign (add) book(s) to the user’s book’s list

    curl -v -H "Content-Type: application/json"
    -d '{"book_id":"2","reader_id":"2"}'
    http://127.0.0.1:5000/api/v1/loans
    :return:
    """
    try:
        _json = request.json
        _reader = _json['reader_id']
        _book = _json['book_id']
        if _reader and _book and request.method == 'POST':
            cur = connection().cursor()
            sql = "INSERT into loan (book_id, reader_id) VALUES (" + _book + ", " + _reader + ");"
            cur.execute(sql)
            connection().commit()
            response = jsonify('Loan added successfully.')
            response.status_code = 200
            return response
        else:
            return show_message()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        connection().close()


@app.route('/api/v1/holder', methods=['GET'])
def api_towhom_loan():
    """
    See which user is assigned to the specific book

    http://127.0.0.1:5000/api/v1/holder?id=3
    http://127.0.0.1:5000/api/v1/holder?title=
    :return:
    """
    query_parameters = request.args

    # TODO: search by title
    id = query_parameters.get('id')
    title = query_parameters.get('title').lower()

    query = "SELECT r.reader_id, r.name, r.surname, r.address from reader r, loan l where r.reader_id = l.reader_id "
    if id:
        query += "AND book_id=" + id + ";"
    if title:
        query = "SELECT r.reader_id, r.name, r.surname, r.address " \
                "from reader r, loan l, book b " \
                "where r.reader_id = l.reader_id " \
                "and b.book_id = l.book_id " \
                "and lower(b.title)='" + title + "';"
    if not (id or title):
        return page_not_found(404)

    cur = connection().cursor()
    cur.execute(query)
    books = cur.fetchall()

    return jsonify(books)


app.run()
