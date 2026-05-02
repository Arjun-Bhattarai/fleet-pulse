# 🚌 Smart Public Transport Signal System

A backend system built with **FastAPI** that allows users to send real-time demand signals for public transport (buses), while drivers and admins can monitor demand and make smarter routing decisions.


### 🔐 Authentication & Security

* JWT-based authentication (Access & Refresh tokens)
* Secure password hashing (bcrypt)
* Token expiration & validation
* Redis-based token blocklisting (logout support)

---

### 👥 Role-Based Access Control (RBAC)

* **User**

  * Create signal
  * View own signals
  * Update/delete own signals

* **Driver**

  * View all signals (demand across city)

* **Admin**

  * Full access (monitor system)

---

### 📍 Signal System

* Users send signals with:

  * Latitude
  * Longitude
  * Passenger count

* Drivers can:

  * See all signals
  * Identify high-demand areas

---

### 🧱 Architecture

* Clean separation of concerns:

  * **Routes (API layer)**
  * **Services (business logic)**
  * **Schemas (validation)**
  * **Models (database)**
  * **Core (auth, dependencies, config)**

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL (Async)
* **ORM:** SQLModel
* **Auth:** JWT
* **Caching / Blocklist:** Redis
* **Validation:** Pydantic

---

## 📁 Project Structure

```
app/
│
├── core/
│   ├── config.py
│   ├── db.py
│   ├── security.py
│   ├── dependency.py
│   └── redis.py
│
├── models/
│   ├── user.py
│   └── signal.py
│
├── schemas/
│   ├── user.py
│   └── signal.py
│
├── services/
│   ├── service.py
│   └── signal.py
│
├── routes/
│   ├── auth.py
│   └── signal.py
│
└── main.py
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/db_name

JWT_SECRET=your_super_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=1800
REFRESH_TOKEN_EXPIRE=86400

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## ▶️ Running the Project

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run server

```
uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

### 🔐 Auth

* `POST /register`
* `POST /login`

---

### 📍 Signals

#### User

* `POST /signals` → Create signal
* `GET /signals/my` → Get own signals
* `PUT /signals/{id}` → Update own signal
* `DELETE /signals/{id}` → Delete own signal

#### Driver/Admin

* `GET /signals` → Get all signals

#### Shared

* `GET /signals/{id}` → Get signal details

---

## 🔒 Security Design

* JWT token required for protected routes
* Role-based access enforced via dependencies
* Ownership checks for update/delete
* Token blocklisting using Redis

---

## 🧠 Future Improvements

* 🔴 Real-time updates using WebSockets
* 🗺️ Map integration (Leaflet / Google Maps)
* 📊 Signal clustering (hotspot detection)
* 🚏 Driver route optimization
* 📱 Mobile app integration

---

## 📌 Project Goal

To build a **smart transport demand system** that helps:

* Users get buses faster
* Drivers optimize routes
* Cities improve public transport efficiency

---

## 👨‍💻 Author

Built as a backend system learning project using FastAPI and modern backend architecture.

---

## ⭐ Status

🚧 In Progress → Core backend completed, moving to real-time features
