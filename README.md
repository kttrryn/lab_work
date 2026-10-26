## Beauli
Beauli – сайт магазину косметики. Головною метою є забезпечити зручний перегляд каталогу і надати можливість клієнту складати обрані предмети в кошик.

#### Сторінки:
* Головна сторінка – тут розміщуються актуальні акції/розпродажі. З неї можна швидко перейти до кошика, увійти в акаунт або почати пошук товарів.
* Меню – доступне з будь-якого місця на сайті. Це велике випадаюче меню, де товари логічно згруповані за напрямками (наприклад, категорії очі, губи, обличчя та субкатегорії помади, тіні, консилери)
* Сторінка списку товарів (каталог) – окрема сторінка, куди клієнт потрапляє після вибору категорії у випадаючому меню. Тут відображається перелік товарів із назвами та цінами. Тут має бути присутня панель фільтрації за брендом, кольором тощо та швидка кнопка "додати в кошик" для кожного товару
* Сторінка товару – містить детальну інформацію про конкретний продукт (назву, опис, артикул, ціну, доступні кольори). Звідси можна додати товар у кошик або перейти на сторінку бренду/виробника
* Сторінка бренду – дозволяє переглянути всі товари конкретного виробника. Тут також працюють фільтри за категоріями та кольорами.
* Пошук – доступний на всіх сторінках. (Пізніше можна додати,щоб він шукав не лише за назвою, але й за комбінацією характеристик. Наприклад, "червона помада" = всі помади які червоні)
* Кошик – зберігає обрані товари. Для авторизованих користувачів кошик прив'язаний до акаунту, для гостей працює на базі поточної сесії

#### Ендпоінти
* Отримання структури меню категорій (Меню та Пошук)
    * Використання: викликається при відкритті випадаючого меню для відображення всіх доступних категорій(Губи) та підкатегорій(Помади та блиски)
    * Request Method: GET
    * Endpoint: /api/v1/categories
    * Request Parameters: Немає
    * Response Status: 200 OK
    * Response Body:
      ```
      [
       {
        "id": 10,
        "name": "Губи",
        "subcategories": [{"id": 11, "name": "Помади та блиски"}]
       }
      ]
      ```
* Отримання списку товарів
    * Використання: Використовується на окремій сторінці списку товарів, на сторінці бренду, а також для глобального пошуку
    * Request Method: GET
    * Endpoint: /api/v1/products
    * Request Parameters (Query): ?category_id=11&brand_id=5&color=red&search=помада
    * Response Status: 200 OK
    * Response Body:
      ```
      {
        "total": 45,
        "items": [
          {
            "id": 101,
            "name": "Matte Lipstick",
            "price": 450.00,
            "brand": "MAC",
            "image_url": "/img/mac_red.jpg"
          }
        ]
      }
      ```
* Отримання деталей товару
    * Використання: Для відображення повної інформації на сторінці конкретного товару
    * Request Method: GET
    * Endpoint: /api/v1/products/{id}
    * Request Parameters: Немає
    * Response Status: 200 OK
    * Response Body:
      ```
      {
        "id": 101,
        "sku": "MAC-001",
        "name": "Matte Lipstick",
        "description": "Стійка червона помада...",
        "price": 450.00,
        "brand": {"id": 5, "name": "MAC"},
        "available_colors": ["red", "pink", "nude"]
      }
      ```
* Отримання даних бренду
    * Використання: Для відображення заголовка та інформації на сторінці бренду (список його товарів завантажується через /api/v1/products?brand_id={id})
    * Request Method: GET
    * Endpoint: /api/v1/brands/{id}
    * Request Parameters: Немає
    * Response Status: 200 OK
    * Response Body:
      ```
      {
        "id": 5,
        "name": "MAC",
        "description": "Професійна косметика для макіяжу."
      }
      ```
* Перегляд кошика (для авторизованих клієнтів)
    * Використання: Отримання списку товарів, які клієнт вже додав у кошик, та загальної суми
    * Request Method: GET
    * Endpoint: /api/v1/cart
    * Request Parameters: Немає
    * Response Status: 200 OK
    * Response Body:
      ```
      {
        "total_price": 450.00,
        "items": [
          {
          "cart_item_id": 1,
          "product_id": 101,
          "name": "Matte Lipstick",
          "color": "red",
          "quantity": 1,
          "price": 450.00
          }
        ]
        }
      ```
* Додавання товару в кошик
    * Використання: Клік по кнопці "Додати в кошик" на сторінці списку товарів або на сторінці деталей
    * Request Method: POST
    * Endpoint: /api/v1/cart/items
    * Request Body:
      ```
      {
        "product_id": 101,
        "color": "red",
        "quantity": 1
      }
      ```
#### Структура БД:
<img width="740" height="461" alt="Screenshot 2026-10-13 at 21 32 55" src="https://github.com/user-attachments/assets/61b5bdbb-14ff-40a3-a4c2-da6310b8f414" />

Всі звʼязки one to many. Категорії та субкатегорії зберігаються в межах єдиної таблиці через ідентичну структуру записів(але лише субкатегорії матимуть parent_id, у категорій буде null). Product_variations потрібна як більш детальна версія кожного продукту (помада однієї лінійки має унікальний колір і виносити її як повністю окремий продукт нема сенсу).


Додайте цей блок у кінець розділу ендпоінтів у `README.md`:


### Адміністрування каталогу (CRUD)

#### 1. Бренди (`/api/v1/brands`)

* POST `/api/v1/brands` — створити бренд
* Тіло: `{"name": "Dior", "description": "Французький дім моди."}`
* Відповідь: `201 Created`


* PUT `/api/v1/brands/{id}` — оновити бренд
* Тіло: `{"name": "Dior Beauty", "description": "Оновлений опис."}`
* Відповідь: `200 OK`


* DELETE `/api/v1/brands/{id}` — видалити бренд
* Відповідь: `204 No Content` (якщо є прив'язані товари то повертає `409 Conflict`)



#### 2. Категорії (`/api/v1/categories`)

* POST `/api/v1/categories` — створити категорію/підкатегорію
* Тіло: `{"name": "Блиски", "parent": 10}` (`parent` опціональний)
* Відповідь: `201 Created`


* GET `/api/v1/categories/{id}` — отримати дані окремої категорії
* Відповідь: `200 OK`


* PUT `/api/v1/categories/{id}` — оновити категорію
* Тіло: `{"name": "Помади та олівці", "parent": 10}`
* Відповідь: `200 OK`


* DELETE `/api/v1/categories/{id}` — видалити категорію
* Відповідь: `204 No Content` (якщо містить підкатегорії чи товари то `409 Conflict`)



#### 3. Товари (`/api/v1/products`)

* POST `/api/v1/products` — створити товар
* Тіло:
```json
{
  "sku": "DIOR-001",
  "name": "Lip Glow Oil",
  "description": "Олія-блиск для губ",
  "price": "1450.00",
  "brand_id": 1,
  "category_id": 2
}

```

* Відповідь: `201 Created`


* PUT `/api/v1/products/{id}` — оновити товар
* Тіло: оновлені поля товару
* Відповідь: `200 OK`


* DELETE `/api/v1/products/{id}` — видалити товар
* Відповідь: `204 No Content`


### Формат обробки помилок

Усі помилки мають єдину структуру відповіді:

```json
{
  "error": {
    "message": "Опис причини помилки"
  }
}
```

* `400 Bad Request` — невалідні вхідні дані або відсутні обов'язкові поля
* `404 Not Found` — запитуваний бренд, категорію чи товар не знайдено
* `409 Conflict` — конфлікт бізнес-правил (спроба видалити бренд або категорію, до яких прив'язані існуючі товари чи підкатегорії)


# web-programming-2026-template

A reusable Django project with no bundled application, SQLite, and Django's
standard admin, authentication, sessions, messages, and staticfiles support.

## Local setup

Requires the latest patch release of Python 3.12, 3.13, or 3.14. Run these commands from the project directory containing
`manage.py`.

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   
   # for linux/macos
   source .venv/bin/activate
   # for Windows:
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements-dev.txt
   ```


3. Apply migrations to create the local SQLite database:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Endpoints

With the server running at `http://127.0.0.1:8000`:

| URL | Behavior |
| --- | --- |
| http://127.0.0.1:8000/ | No application homepage; may show Django's development welcome page while `DEBUG = True` |
| http://127.0.0.1:8000/admin/ | Django admin, available after applying migrations |

With `DEBUG = False`, unmatched URLs such as `/` return HTTP 404.

To create an account for admin login, run this after applying migrations:

```bash
python manage.py createsuperuser
```

## Add your first application

1. Create an app from the directory containing `manage.py` (replace `myapp`
   with your application name):

   ```bash
   python manage.py startapp myapp
   ```

2. Add its generated configuration class, `myapp.apps.MyappConfig`, to
   `INSTALLED_APPS` in `config/settings.py`.
3. Define your views and create `myapp/urls.py` with their URL patterns.
4. Register that URLconf in `config/urls.py` using `path()` and `include()`,
   choosing a URL prefix for the app and retaining the admin route.

See the official Django 6.1 tutorial for
[views and URL registration](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
and [app registration and models](https://docs.djangoproject.com/en/6.1/intro/tutorial02/).

## Start a REST API

Django REST framework and `django-cors-headers` are included and configured.
Install the project dependencies with `python -m pip install -r requirements-dev.txt`.
Create your own app, serializers, views, and URL patterns; no API app or
authentication scheme is supplied.

## Git attributes

Git detects text files automatically and normalizes them to LF. Checkouts use
LF on Linux and Windows, while `.bat` and `.cmd` files use CRLF. Binary files
are auto-detected and left unchanged, helping avoid newline-only diffs.


## Code style and submission verification

All submissions are required to adhere to PEP-8, Django best practices, and standard HTML/CSS/JS formatting. A deterministic cross-platform utility is provided to help you check and format your code.

### 1. Verification (Check Mode)
Before submitting, verify that all files adhere to the required standards:

```bash
python check_submission.py
```

Passing these checks confirms code style, not functional API behavior. Before submitting an API, also write and run functional tests for its endpoints. If style checks fail, review the error output or run the auto-formatter below.

### 2. Auto-Formatting
To automatically format Python files, fix safe PEP-8 rules, format Django HTML templates, and format CSS/JS static files:

```bash
python check_submission.py --format
```

### 3. PyCharm Integration
If you use PyCharm:
- **One-Click Run:** In the top-right toolbar run configurations dropdown, select **"Verify Submission"** or **"Format Project"** and click the green **Play** button.

## Development only

The included settings use `DEBUG = True`, a development secret key, and a local
SQLite database. The default mailer uses the console backend: email is printed
to the process's console instead of being delivered.

This configuration and Django's development server are not suitable for
production deployment.

