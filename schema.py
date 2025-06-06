# core tables
schemas = {
    "apartments": {
        "apartment_id": "PK",
        "building_name": "String",
        "floor_number": "Integer",
        "unit_number": "String",
        "size_sqft": "Integer",
        "year_built": "Integer",
        "status": "Enum(Vacant, Occupied, Maintenance)"
    },
    
    "property_owners": {
        "owner_id": "PK",
        "apartment_id": "FK",
        "name": "String",
        "email": "String",
        "phone": "String",
        "ownership_percentage": "Decimal(5,2)",
        "is_primary": "Boolean",
        "id_type": "String",
        "id_number": "String",
        "bank_account": "String"
    },
    
    "property_registration": {
        "registration_id": "PK",
        "apartment_id": "FK",
        "egarsi_number": "String",
        "registration_date": "Date",
        "contract_amount": "Decimal(12,2)",
        "advance_payment": "Decimal(12,2)",
        "contract_start": "Date",
        "contract_end": "Date",
        "payment_terms": "String",
        "status": "Enum(Active, Expired, Terminated)"
    }
}
# financial tables
schemas.update({
    "cheques": {
        "cheque_id": "PK",
        "apartment_id": "FK",
        "cheque_number": "String",
        "bank_name": "String",
        "account_name": "String",
        "amount": "Decimal(12,2)",
        "issue_date": "Date",
        "due_date": "Date",
        "deposit_date": "Date",
        "status": "Enum(Pending, Cleared, Bounced, Cancelled)",
        "image_url": "String"
    },
    
    "brokerage": {
        "brokerage_id": "PK",
        "apartment_id": "FK",
        "broker_id": "FK",
        "amount": "Decimal(12,2)",
        "payment_date": "Date",
        "payment_method": "String",
        "status": "Enum(Paid, Pending, Overdue)",
        "receipt_url": "String"
    },
    
    "brokers": {
        "broker_id": "PK",
        "name": "String",
        "company": "String",
        "email": "String",
        "phone": "String",
        "license_number": "String",
        "commission_rate": "Decimal(5,2)"
    }
})
# property tables
schemas.update({
    "apartment_furnishing": {
        "id": "PK",
        "apartment_id": "FK",
        "furnishing_id": "FK",
        "item_name": "String",
        "purchase_date": "Date",
        "cost": "Decimal(10,2)",
        "condition": "Enum(New, Good, Fair, Poor)",
        "image_url": "String"
    },
    
    "apartment_attributes": {
        "id": "PK",
        "apartment_id": "FK",
        "attribute_type": "Enum(View, Flooring, Layout)",
        "attribute_value": "String"
    },
    
    "apartment_amenities": {
        "id": "PK",
        "apartment_id": "FK",
        "amenity_name": "String",
        "description": "String",
        "is_chargeable": "Boolean"
    }
})
# operational tables
schemas.update({
    "guests": {
        "guest_id": "PK",
        "apartment_id": "FK",
        "name": "String",
        "email": "String",
        "phone": "String",
        "id_type": "String",
        "id_number": "String",
        "check_in": "Date",
        "check_out": "Date",
        "deposit_amount": "Decimal(10,2)",
        "status": "Enum(Active, Checked-Out)"
    },
    
    "employees": {
        "emp_id": "PK",
        "name": "String",
        "designation": "String",
        "salary": "Decimal(10,2)",
        "bank_details": "String",
        "joining_date": "Date",
        "status": "Enum(Active, Inactive)",
        "contact": "String",
        "visa_info": "String"
    },
    
    "payments": {
        "payment_id": "PK",
        "apartment_id": "FK",
        "type": "String",
        "amount": "Decimal(10,2)",
        "date": "Date",
        "method": "String",
        "status": "String",
        "reference": "String"
    },
    
    "wps": {
        "wps_id": "PK",
        "emp_id": "FK",
        "amount": "Decimal(10,2)",
        "payment_date": "Date",
        "status": "String",
        "transaction_ref": "String"
    },
    
    "rent": {
        "rent_id": "PK",
        "apartment_id": "FK",
        "guest_id": "FK",
        "amount": "Decimal(10,2)",
        "payment_date": "Date",
        "period_start": "Date",
        "period_end": "Date",
        "status": "String"
    }
})

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Helper functions
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_string(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def random_phone():
    return f"05{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

# Generate buildings and apartments
buildings = ['Palm Tower', 'Marina Heights', 'Downtown Residence', 'Hillside Villa']
apartment_types = ['Studio', '1BR', '2BR', '3BR', 'Penthouse']

apartments = []
for i in range(1, 51):
    apartments.append({
        "apartment_id": i,
        "building_name": random.choice(buildings),
        "floor_number": random.randint(1, 30),
        "unit_number": f"{random.randint(1, 20)}{random.choice(['A', 'B', 'C', 'D'])}",
        "size_sqft": random.choice([500, 750, 1000, 1200, 1500, 2000, 2500]),
        "year_built": random.randint(2010, 2023),
        "status": random.choice(["Vacant", "Occupied", "Occupied", "Maintenance"])
    })

# Generate property owners (1-3 owners per apartment)
property_owners = []
owner_id = 1
for apt in apartments:
    num_owners = random.randint(1, 3)
    for n in range(num_owners):
        property_owners.append({
            "owner_id": owner_id,
            "apartment_id": apt["apartment_id"],
            "name": f"Owner {owner_id}",
            "email": f"owner{owner_id}@example.com",
            "phone": random_phone(),
            "ownership_percentage": round(100/num_owners, 2),
            "is_primary": n == 0,
            "id_type": random.choice(["Passport", "Emirates ID", "Driving License"]),
            "id_number": f"{random.randint(1000000, 9999999)}",
            "bank_account": f"AE{random.randint(100000000000000000, 999999999999999999)}"
        })
        owner_id += 1

# Generate property registrations
property_registrations = []
for apt in apartments:
    start_date = random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
    contract_amount = apt["size_sqft"] * random.uniform(80, 150)
    property_registrations.append({
        "registration_id": len(property_registrations) + 1,
        "apartment_id": apt["apartment_id"],
        "egarsi_number": f"EG{random.randint(100000, 999999)}",
        "registration_date": start_date,
        "contract_amount": round(contract_amount, 2),
        "advance_payment": round(contract_amount * random.uniform(0.05, 0.15), 2),
        "contract_start": start_date,
        "contract_end": start_date + timedelta(days=365),
        "payment_terms": random.choice(["Monthly", "Quarterly", "Bi-annually"]),
        "status": "Active" if start_date > datetime(2023, 6, 1) else "Expired"
    })

# Generate brokers
brokers = []
for i in range(1, 11):
    brokers.append({
        "broker_id": i,
        "name": f"Broker {i}",
        "company": random.choice(["Elite Properties", "Bayut", "Property Finder", "Luxury Homes"]),
        "email": f"broker{i}@example.com",
        "phone": random_phone(),
        "license_number": f"RERA-{random.randint(10000, 99999)}",
        "commission_rate": round(random.uniform(0.02, 0.05), 4)
    })

# Generate brokerage records
brokerage_records = []
for reg in property_registrations:
    if random.random() > 0.3:  # 70% chance of having brokerage
        brokerage_records.append({
            "brokerage_id": len(brokerage_records) + 1,
            "apartment_id": reg["apartment_id"],
            "broker_id": random.choice([b["broker_id"] for b in brokers]),
            "amount": round(reg["contract_amount"] * random.uniform(0.02, 0.05), 2),
            "payment_date": reg["registration_date"] + timedelta(days=random.randint(1, 14)),
            "payment_method": random.choice(["Cash", "Cheque", "Bank Transfer"]),
            "status": "Paid",
            "receipt_url": f"https://example.com/receipts/{random_string(16)}.pdf"
        })

# Generate cheques
cheques = []
for reg in property_registrations:
    num_cheques = random.randint(4, 12)
    remaining_amount = reg["contract_amount"] - reg["advance_payment"]
    base_amount = remaining_amount / num_cheques
    
    for i in range(num_cheques):
        due_date = reg["contract_start"] + timedelta(days=30*(i+1))
        status = "Cleared" if due_date < datetime.now() else "Pending"
        cheques.append({
            "cheque_id": len(cheques) + 1,
            "apartment_id": reg["apartment_id"],
            "cheque_number": f"CHQ{random.randint(100000, 999999)}",
            "bank_name": random.choice(["Emirates NBD", "Mashreq", "ADCB", "DIB", "RAK Bank"]),
            "account_name": f"Owner {random.choice([o['owner_id'] for o in property_owners if o['apartment_id'] == reg['apartment_id']])}",
            "amount": round(base_amount * random.uniform(0.9, 1.1), 2),
            "issue_date": reg["contract_start"],
            "due_date": due_date,
            "deposit_date": due_date if status == "Cleared" else None,
            "status": status,
            "image_url": f"https://example.com/cheques/{random_string(16)}.jpg"
        })

# Generate apartment furnishings
furnishing_items = ["Sofa", "Dining Table", "Bed", "Wardrobe", "TV", "Refrigerator", 
                   "Washing Machine", "Oven", "Coffee Table", "Curtains"]

apartment_furnishings = []
for apt in apartments:
    num_items = random.randint(3, 10)
    for _ in range(num_items):
        purchase_date = random_date(datetime(2020, 1, 1), datetime(2023, 12, 31))
        apartment_furnishings.append({
            "id": len(apartment_furnishings) + 1,
            "apartment_id": apt["apartment_id"],
            "furnishing_id": random.randint(1000, 9999),
            "item_name": random.choice(furnishing_items),
            "purchase_date": purchase_date,
            "cost": round(random.uniform(500, 5000), 2),
            "condition": random.choice(["New", "Good", "Fair", "Poor"]),
            "image_url": f"https://example.com/furnishings/{random_string(16)}.jpg"
        })

# Generate apartment attributes
attributes = {
    "View": ["Sea View", "City View", "Garden View", "Pool View", "No View"],
    "Flooring": ["Marble", "Wood", "Tiles", "Carpet"],
    "Layout": ["Open Plan", "Traditional", "Modern", "Classic"]
}

apartment_attributes = []
for apt in apartments:
    for attr_type, values in attributes.items():
        apartment_attributes.append({
            "id": len(apartment_attributes) + 1,
            "apartment_id": apt["apartment_id"],
            "attribute_type": attr_type,
            "attribute_value": random.choice(values)
        })

# Generate apartment amenities
common_amenities = ["Swimming Pool", "Gym", "Parking", "Security", "Concierge", 
                   "Kids Play Area", "BBQ Area", "Laundry", "Elevator", "Balcony"]

apartment_amenities = []
for apt in apartments:
    num_amenities = random.randint(3, 8)
    amenities = random.sample(common_amenities, num_amenities)
    for amenity in amenities:
        apartment_amenities.append({
            "id": len(apartment_amenities) + 1,
            "apartment_id": apt["apartment_id"],
            "amenity_name": amenity,
            "description": f"Building {amenity}",
            "is_chargeable": random.choice([True, False])
        })

# Generate guests
guests = []
for apt in apartments:
    if apt["status"] == "Occupied":
        check_in = random_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
        guests.append({
            "guest_id": len(guests) + 1,
            "apartment_id": apt["apartment_id"],
            "name": f"Guest {len(guests) + 1}",
            "email": f"guest{len(guests) + 1}@example.com",
            "phone": random_phone(),
            "id_type": random.choice(["Passport", "Emirates ID"]),
            "id_number": f"{random.randint(1000000, 9999999)}",
            "check_in": check_in,
            "check_out": check_in + timedelta(days=random.randint(30, 365)),
            "deposit_amount": round(random.uniform(1000, 5000), 2),
            "status": "Active"
        })

# Generate employees
designations = ["Manager", "Supervisor", "Cleaner", "Security", "Maintenance", 
               "Accountant", "Receptionist", "Concierge"]

employees = []
for i in range(1, 21):
    joining_date = random_date(datetime(2018, 1, 1), datetime(2023, 12, 31))
    employees.append({
        "emp_id": i,
        "name": f"Employee {i}",
        "designation": random.choice(designations),
        "salary": round(random.uniform(2000, 15000), 2),
        "bank_details": f"AE{random.randint(100000000000000000, 999999999999999999)}",
        "joining_date": joining_date,
        "status": "Active" if random.random() > 0.2 else "Inactive",
        "contact": random_phone(),
        "visa_info": f"Visa {random.randint(100000, 999999)}"
    })

# Generate payments (DEWA, chiller, etc.)
payment_types = ["DEWA", "Chiller", "Municipality", "Service Charges", "VAT"]

payments = []
for apt in apartments:
    for _ in range(random.randint(2, 6)):
        payments.append({
            "payment_id": len(payments) + 1,
            "apartment_id": apt["apartment_id"],
            "type": random.choice(payment_types),
            "amount": round(random.uniform(200, 2000), 2),
            "date": random_date(datetime(2023, 1, 1), datetime(2023, 12, 31)),
            "method": random.choice(["Cash", "Cheque", "Bank Transfer"]),
            "status": random.choice(["Paid", "Pending", "Overdue"]),
            "reference": f"INV-{random.randint(10000, 99999)}"
        })

# Generate WPS (salary payments)
wps_records = []
for emp in employees:
    if emp["status"] == "Active":
        for _ in range(random.randint(1, 12)):  # 1-12 salary payments
            wps_records.append({
                "wps_id": len(wps_records) + 1,
                "emp_id": emp["emp_id"],
                "amount": emp["salary"],
                "payment_date": random_date(datetime(2023, 1, 1), datetime(2023, 12, 31)),
                "status": "Paid",
                "transaction_ref": f"WPS-{random.randint(100000, 999999)}"
            })

# Generate rent records
rent_records = []

for guest in guests:
    period_start = guest["check_in"]
    while period_start < guest["check_out"]:
        period_end = min(period_start + timedelta(days=30), guest["check_out"])
        rent_amount = random.uniform(3000, 15000)
        rent_records.append({
            "rent_id": len(rent_records) + 1,
            "apartment_id": guest["apartment_id"],
            "guest_id": guest["guest_id"],
            "amount": round(rent_amount, 2),
            "payment_date": period_start + timedelta(days=random.randint(0, 5)),
            "period_start": period_start,
            "period_end": period_end,
            "status": "Paid" if random.random() > 0.1 else "Pending"  # 10% chance of pending
        })
        period_start = period_end

# Save generated data to CSV files
pd.DataFrame(apartments).to_csv("apartments.csv", index=False)
pd.DataFrame(property_owners).to_csv("property_owners.csv", index=False)
pd.DataFrame(property_registrations).to_csv("property_registrations.csv", index=False)
pd.DataFrame(brokers).to_csv("brokers.csv", index=False)
pd.DataFrame(brokerage_records).to_csv("brokerage.csv", index=False)
pd.DataFrame(cheques).to_csv("cheques.csv", index=False)
pd.DataFrame(apartment_furnishings).to_csv("apartment_furnishings.csv", index=False)
pd.DataFrame(apartment_attributes).to_csv("apartment_attributes.csv", index=False)
pd.DataFrame(apartment_amenities).to_csv("apartment_amenities.csv", index=False)
pd.DataFrame(guests).to_csv("guests.csv", index=False)
pd.DataFrame(employees).to_csv("employees.csv", index=False)
pd.DataFrame(payments).to_csv("payments.csv", index=False)
pd.DataFrame(wps_records).to_csv("wps.csv", index=False)
pd.DataFrame(rent_records).to_csv("rent.csv", index=False)

