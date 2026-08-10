# 🚗 Car Rental System using FastAPI

A simple REST API-based **Car Rental System** built using **FastAPI** and **Pydantic**. The application provides APIs for managing cars, searching and sorting vehicles, pagination, and handling the complete car booking workflow.

---

## 🚀 Key Features

- **Car Management**: Create, read, update, and delete car details.
- **Car Search**: Search cars using brand and model.
- **Sorting**: Sort cars based on rental price.
- **Pagination**: Retrieve cars using page and limit parameters.
- **Car Browsing**: Combine filtering, sorting, and pagination.
- **Booking System**: Book an available car and calculate the total rental price.
- **Pickup & Return**: Manage the pickup and return status of booked cars.
- **Pydantic Validation**: Validate car and booking request data.
- **Custom Validation**: Validate customer names using `field_validator`.
- **Exception Handling**: Handle invalid requests and unavailable resources.
- **API Documentation**: Interactive Swagger UI provided by FastAPI.

---

## 🛠️ Technologies Used

- **Python**
- **FastAPI**
- **Pydantic**
- **Uvicorn**

---

## 📂 Project Structure

```text
car-rental-system/
│
├── main.py
└── README.md
```

---

## ⚙️ Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install fastapi uvicorn pydantic
```

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/cars` | Get all cars |
| POST | `/cars` | Add a new car |
| GET | `/cars/{id}` | Get a car by ID |
| PUT | `/cars/{id}` | Update car details |
| DELETE | `/cars/{id}` | Delete a car |
| GET | `/cars/search` | Search cars |
| GET | `/cars/sort` | Sort cars by price |
| GET | `/cars/page` | Paginate car results |
| GET | `/cars/browse` | Filter, sort, and paginate cars |
| POST | `/book` | Book a car |
| PUT | `/pickup/{booking_id}` | Pick up a booked car |
| PUT | `/return/{booking_id}` | Return a rented car |

---

## 🔎 Search

Search cars using brand or model.

```text
/cars/search?brand=Toyota
```

```text
/cars/search?model=Creta
```

---

## ↕️ Sorting

Sort cars based on rental price.

```text
/cars/sort?order=asc
```

```text
/cars/sort?order=desc
```

---

## 📄 Pagination

Use `page` and `limit` query parameters.

```text
/cars/page?page=1&limit=5
```

---

## 🔍 Browse Cars

The browse endpoint combines filtering, sorting, and pagination.

```text
/cars/browse?brand=Toyota&order=asc&page=1&limit=5
```

---

## 📅 Booking Workflow

```text
Available
    ↓
  Booked
    ↓
Picked Up
    ↓
 Returned
    ↓
Available Again
```

When a car is booked, its availability becomes `False`. After the car is returned, its availability becomes `True`.

---

## 💰 Booking Calculation

The total rental price is calculated as:

```text
Total Price = Number of Days × Price Per Day
```

Example:

```text
3 Days × ₹2500 = ₹7500
```

---

## ✅ Validation

Pydantic models are used to validate car and booking data.

The application validates:

- Car ID
- Brand
- Model
- Manufacturing year
- Number of seats
- Rental price
- Customer name
- Booking details

Custom validation is implemented using Pydantic `field_validator`.

---

## ⚠️ Exception Handling

The application handles errors such as:

- Car already exists
- Car not found
- Car already booked
- Booking not found
- Invalid pickup operation
- Invalid return operation

---

## 📝 Example Car Request

```json
{
  "id": 6,
  "brand": "Kia",
  "model": "Seltos",
  "year": 2024,
  "color": "Grey",
  "fuel_type": "Petrol",
  "transmission": "Automatic",
  "seats": 5,
  "price_per_day": 2300,
  "available": true
}
```

---

## 📝 Example Booking Request

```json
{
  "booking_id": 101,
  "car_id": 1,
  "customer_name": "Hruthik",
  "days": 3
}
```

---

## 💾 Data Storage

The application currently uses in-memory Python lists to store cars and bookings. The data will reset when the application is restarted.

---

## 👨‍💻 Author

**Hruthik Reddy Anugu**
