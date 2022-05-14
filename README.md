# PARKING LOT Api Docs

Step 1:
```
pip install virtualenv

venv\Scripts\Activate 
```
Step 2:
```
pip install -r requirements.txt
```

Step 3:
```
cd carpark
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
 
```
Step 4:
```
You will get those links
{
    "Park": "http://127.0.0.1:8000/cars/",
    "Info": "http://127.0.0.1:8000/info/"
}
```

# CHANGE EVERYTHING FROM dashboard/config file

# CASE 1: Park a Car
```
    ## Just input car_no. I assume that  car number is Car Licence Plate Number. It will automatically pick a slot from parking lot also save your IP address. You can't park other car by your IP or you can do it after Unpark your car from parking lot. Example For: Car Number 'BMX12341234'
    {
        "car_no": "BMX12341234",
        "slot_no": 1,
    }
```

# CASE 2: Unpark a Car
```
    ## Unpark a car means you remove your car from parking lot. The endpoint will take slot number where you parked your car. EXAMPLE : http://127.0.0.1:8000/unpark/1 , 1 is your slot_no. You cant unpark others because ip is unique.
    {
        "message": "Slot Open"
    }
    Now this slot is reuseable. If anyone want to park here, they can
```
# CASE 3: GET SLOT/CAR NUMBER information
```
    ## If you put your slot number EXAMPLE: 1 return both car number and slot number
    {
        "car_no": "BMX12341234",
        "slot_no": 1
    }

    ## If you put your car number EXAMPLE: 'BMX12341234' return both car number and slot number
    {
        "car_no": "BMX12341234",
        "slot_no": 1
    }
    
    ## If you put incorrect car number or slot number
    {
        "message": "Your Car is not parked or type correct Car No"
    }
```

# CASE 4: Rate-limit 
```
    ## If client sent more than 10 GET request
    {
        "message": "You were blocked for 5 seconds"
    }
```
