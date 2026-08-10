from fastapi import FastAPI, Path, Query, HTTPException,status
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional
from fastapi.responses import JSONResponse

app = FastAPI()
cars = [
    {
        "id": 1,
        "brand": "Toyota",
        "model": "Innova Crysta",
        "year": 2023,
        "color": "White",
        "fuel_type": "Diesel",
        "transmission": "Manual",
        "seats": 7,
        "price_per_day": 2500,
        "available": True
    },
    {
        "id": 2,
        "brand": "Hyundai",
        "model": "Creta",
        "year": 2022,
        "color": "Black",
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 5,
        "price_per_day": 2200,
        "available": True
    },
    {
        "id": 3,
        "brand": "Mahindra",
        "model": "Thar",
        "year": 2024,
        "color": "Red",
        "fuel_type": "Diesel",
        "transmission": "Manual",
        "seats": 4,
        "price_per_day": 3000,
        "available": False
    },
    {
        "id": 4,
        "brand": "Tata",
        "model": "Nexon",
        "year": 2023,
        "color": "Blue",
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "seats": 5,
        "price_per_day": 2000,
        "available": True
    },
    {
        "id": 5,
        "brand": "Honda",
        "model": "City",
        "year": 2021,
        "color": "Silver",
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "seats": 5,
        "price_per_day": 1800,
        "available": True
    }
]

bookings = []

class Car(BaseModel):
    id: Annotated[int, Field(...,description="id of the car", example=1)]
    brand: Annotated[str, Field(..., description="brand of the car")]
    model: Annotated[str, Field(..., description='model of the car')]
    year: Annotated[int,Field(...,ge=2000,le=2035,description="Manufacturing year")]
    color: Annotated[str, Field(..., description='color of the car')]
    fuel_type: Annotated[str, Field(..., description='fuel type of the car')]
    transmission: Annotated[str, Field(..., description='transmission of the car')]
    seats:Annotated[int, Field(..., ge=2,le=10,description='seats of the car')]
    price_per_day: Annotated[float, Field(..., gt=0,description='price per day of the car')]
    available: Annotated[bool, Field(..., description='avaliable of the car', examples=[True])]

class UpdateCar(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    seats: Optional[int] = None
    price_per_day: Optional[float] = None
    available: Optional[bool] = None

class Booking(BaseModel):
    booking_id: Annotated[int, Field(...,description="booking id for the car")]
    car_id: Annotated[int, Field(...,description="id of the car")]
    customer_name: Annotated[str, Field(...,description="name of the customer")]
    days:  Annotated[int, Field(...,description="no.of day require")]
    @field_validator("customer_name")
    @classmethod
    def validate_name(cls, value):

        if len(value.strip()) < 3:
            raise ValueError("Customer name must contain at least 3 characters")

        return value

@app.get('/')
def home():
    return {"home": "welcome to the car service"}

@app.get('/cars', response_model=list[Car])
def get_all_cars():
    return cars

@app.post("/cars",status_code=status.HTTP_201_CREATED,response_model=Car)
def add_car(car: Car):
    for existing_car in cars:
        if existing_car["id"] == car.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Car already exists")
    cars.append(car.model_dump())

    return car

@app.put("/cars/{id}")
def updated_car(id: int, updated_car: UpdateCar):
    for index, car in enumerate(cars):
        if car["id"]==id:
            updated_data = updated_car.model_dump(exclude_unset=True)
            cars[index].update(updated_data)
            return {"message":"car updated successfully", 
                    "car": cars[index]}
    raise HTTPException(status_code=404, detail="car not found")


@app.delete('/cars/{id}')
def delete_car(id: int):
    for index, car in enumerate(cars):
        if car['id'] == id:
            del cars[index]
            return {"message":"car deleted successfully"}
    raise HTTPException(status_code=404, detail="car not found")
    
        
@app.post("/book")
def book_car(booking: Booking):
    for car in cars:
        if car['id'] == booking.car_id:
            if not car['available']:
                raise HTTPException(status_code=400, detail="car is already booked")
            total_price = booking.days * car['price_per_day']

            new_booking = {
                "booking_id":booking.booking_id,
                "car_id": booking.car_id,
                'customer_name':booking.customer_name,
                "days":booking.days,
                "total_price":total_price,
                'status':"Booked"
            }
            bookings.append(new_booking)
            car['available'] = False

            return {"message": "car booked successfully",
                    "booking": new_booking}
    raise HTTPException(status_code=404, detail="car not found")

@app.put("/pickup/{booking_id}")
def pickup_car(booking_id: int):
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking["status"]!="Booked":
                raise HTTPException(status_code=400, detail="car has already booked")
            booking["status"] = "picked up"
            return {"message": "car picked up successfully",
                    "booking": booking}
    raise HTTPException(status_code=400, detail="booking not found")

@app.put("/return/{booking_id}")
def return_car(booking_id:int):
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking['status'] != "picked up":
                raise HTTPException(status_code=400, detail="car has not been picked up yet")
            booking['status'] = "Returned"

            for car in cars:
                if car['id'] == booking["car_id"]:
                    car["available"] = True
                    break
            return {"message":"car returned successfully",
                    "booking":booking}
    raise HTTPException(status_code=404, detail="Booking not found")


@app.get("/cars/search")
def search_cars(brand: str| None = Query(None), model: str| None=Query(None)):
    res = cars

    if brand:
        res = [car for car in res if car["brand"].lower() == brand.lower()]
    if model:
        res = [car for car in res if car["model"].lower() == model.lower()]
    return res

@app.get("/cars/sort")
def sort_cars(order: str= Query("asc")):
    if order.lower() == "desc":
        return sorted(cars, key=lambda car: car["price_per_day"], reverse=True)
    return sorted(cars,key=lambda car: car["price_per_day"])

@app.get("/cars/page")
def paginate_cars(page: int=Query(1,ge=1), limit: int=Query(5,ge=1)):
    start = (page-1)*limit
    end = start + limit

    return {"page": page, "limit": limit, "total": len(cars), "cars": cars[start:end]}

@app.get("/cars/browse")
def browse_cars(
    brand: str | None = Query(None),
    model: str | None = Query(None),
    order: str = Query("asc"),
    page: int = Query(1,ge=1),
    limit: int = Query(5,ge=1)):
    res = cars

    if brand: 
        res = [car for car in res if car["brand"].lower() == brand.lower()]
    if model:
        res = sorted(res, key=lambda car: car["price_per_day"],reverse=(order.lower()=="desc"))
    res = sorted(res, key=lambda car:car['price_per_day'],reverse=(order.lower() == "desc"))

    start = (page - 1)*limit
    end = start + limit

    return {"page": page,"limit": limit, "total":len(res), "cars": res[start:end]}
    

@app.get("/cars/{id}", response_model=Car)
def get_car(id: int = Path(..., description="ID of the car")):
    for car in cars:
        if car["id"] == id:
            return car
    raise HTTPException(status_code=404, detail="car not found")         



for route in app.routes:
    print(route.path)