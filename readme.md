💳 Payment with Django + Zarinpal (AzBankGateways)
=================================================

A full-stack Django project to demonstrate user registration, login, credit purchase, and payment via **Zarinpal** using the `azbankgateways` library. It includes a simple **React (in-browser JSX)** frontend and **JWT authentication**.

🚀 Features
-----------

- 🔐 JWT-based authentication with Ninja JWT
- 👤 User registration with credit tracking (`UserProfile`)
- 💸 Purchase credits via Zarinpal sandbox
- ✅ Automatic payment verification on return
- 🌐 Simple frontend with React & Babel, served via `index.html`

🧱 Project Structure
--------------------

```
armemami2001-payment_with_django/
│
├── dargahpardkht/               # Django project root
│   ├── manage.py                # Entry point
│   ├── requirements.txt         # Python dependencies
│   ├── creditpurchase/          # Core app
│   │   ├── models.py            # UserProfile model
│   │   ├── controller.py        # NinjaExtra API controllers
│   │   ├── schema.py            # Request/response schemas
│   └── dargahpardkht/
│       ├── api.py               # Controller registration
│       ├── settings.py
│       ├── urls.py
│
└── Frontend/
    └── index.html               # Self-contained frontend (React + Babel)
```

🔧 Setup Instructions
---------------------

### 1. 📦 Install Requirements

```bash
cd dargahpardkht
python -m venv venv
Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 🔧 Configure Zarinpal

In `settings.py`, configure:

```python
AZ_IRANIAN_BANK_GATEWAYS = {
  "GATEWAYS": {
    "ZARINPAL": {
      "MERCHANT_CODE": "YOUR-ZARINPAL-CODE-HERE",
      "SANDBOX": 1,
      "IS_ENABLED": True,
    },
  },
  "DEFAULT": "ZARINPAL",
  "CURRENCY": "IRR",
  "TRACKING_CODE_QUERY_PARAM": "tc",
}
```

### 3. 🧬 Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 🔐 Create Superuser (optional)

```bash
python manage.py createsuperuser
```

### 5. ▶️ Run Django Server

```bash
python manage.py runserver
```

### 6. 🌐 Start Frontend

```bash
cd Frontend
python -m http.server 5500
```

> Then open `http://localhost:5500` in your browser.

📦 API Overview
----------------

| Endpoint                                 | Description             |
|------------------------------------------|--------------------------|
| `POST /api/register/create_user`         | Create a new user        |
| `POST /api/token/pair`                   | Get JWT token            |
| `GET /api/profile/`                      | Get user profile         |
| `GET /api/shop/purchase-credits?amount=` | Initiate payment         |
| `GET /api/shop/verify-payment?tc=...`    | Verify payment           |

🧠 How It Works
----------------

- User logs in/registers
- User clicks *"Purchase Credits"*
- Backend generates payment request via Zarinpal
- User is redirected to Zarinpal sandbox
- After payment, Zarinpal redirects user back to `/index.html?tc=...`
- Frontend auto-detects `tc` and verifies payment
- On success, user credits are increased

🎨 Frontend Tech
----------------

- React 18 via UMD + Babel (no bundler needed)
- JSX inside `<script type="text/babel">`
- JWT is saved in `localStorage`
- Payment auto-verification is triggered if `tc` is present in the URL

🔒 Auth Flow (JWT)
------------------

- Auth via `ninja_jwt`
- JWT is sent as `Authorization: Bearer <token>`
- Session is restored on reload if token is valid

🧪 Example Test Flow
---------------------

1. Run backend + frontend
2. Register or login a user
3. Press "Purchase Credits"
4. Complete payment on Zarinpal sandbox
5. Get redirected back with `?tc=...`
6. Credits update automatically

📦 API Endpoint Explanations
----------------------
### 🔐 `POST /api/token/pair`
Authenticate a user using their username and password and return a **JWT access + refresh token pair**.

**Request Body**
```json
{
  "username": "john",
  "password": "1234"
}
```

**Response**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5..."
}
```

---

### 👤 `GET /api/profile/`
Returns the authenticated user’s basic profile including current credit balance.

**Headers**
```
Authorization: Bearer <access_token>
```

**Response**
```json
{
  "username": "john",
  "credits": 100000
}
```

---

### 🧾 `POST /api/register/create_user`
Registers a new user account with a username and password.

**Request Body**
```json
{
  "username": "john",
  "password": "1234"
}
```

**Response**
```json
{
  "message": "User created successfully."
}
```

---

### 💸 `GET /api/shop/purchase-credits?amount=10000`
Initiates a payment via Zarinpal and returns a `redirect_url` to the payment gateway.

**Query Parameters**
```
amount (int): Amount in IRR (e.g., 10000)
```

**Headers**
```
Authorization: Bearer <access_token>
```

**Response**
```json
{
  "redirect_url": "https://sandbox.zarinpal.com/pg/StartPay/..."
}
```

---

### ✅ `GET /api/shop/verify-payment?tc=<tracking_code>`
Verifies the payment via AzBankGateways and, if successful, updates the user's credit balance.

**Query Parameters**
```
tc: tracking code provided by AzBankGateways (e.g., ?tc=2381329348539292)
```

**Headers**
```
Authorization: Bearer <access_token>
```

**Response (Success)**
```json
{
  "message": "Payment verified and credits added.",
  "credits_added": 10000,
  "new_balance": 110000
}
```

**Response (Failure)**
```json
{
  "message": "Payment failed or already verified."
}
```

---

## 🔒 Authentication Summary

All `/api/shop/...` and `/api/profile/` endpoints require:

```
Authorization: Bearer <JWT Access Token>
```

Use `/api/token/pair` to obtain this after logging in.