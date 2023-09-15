import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import os  # Import the os module

# Create a Faker instance
fake = Faker()

# Define the header for your CSV file
header = [
    "cityname",
    "Discount",
    "product_description",
    "ticket_value",
    "region",
    "week_day",
    "transaction_datetime",
    "location_description",
    "payment_type",
    "locationname",
    "location_id",
    "companyname",
    "transaction_amount",
    "transaction_type",
    "brandname",
    "sale_number",
    "bussiness_datatime",
    "hour",
]

# Define relevant values for specific fields
regions = ["East", "West", "Midwest", "South"]
product_descriptions = ["Product A", "Product B", "Product C", "Product D"]
location_descriptions = ["Store", "Shop", "Mall"]
location_names = ["Location 1", "Location 2", "Location 3", "Location 4"]
brand_names = ["Brand X", "Brand Y", "Brand Z", "Brand W"]

# Generate random data for 1 million records
num_records = 10
data = []

# Define the start and end datetime for the year 2023
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

print(f"Generating {num_records} records...")

for record_num in range(num_records):
    print(f"Generating record {record_num + 1}/{num_records}")
    
    row = [
        fake.city(),
        random.uniform(0.1, 50.0),  # Random discount between 0.1 and 50.0
        random.choice(product_descriptions),  # Random product description
        random.randint(1, 100),  # Random ticket value between 1 and 100
        random.choice(regions),  # Random region
        fake.day_of_week(),  # Random weekday
        fake.date_time_between_dates(datetime_start=start_date, datetime_end=end_date),  # Random transaction datetime in 2023
        f"{random.choice(location_descriptions)} {random.randint(1, 100)}",  # Random location description
        random.choice(["Credit Card", "Cash", "Debit Card"]),  # Random payment type
        f"{random.choice(location_names)} {random.randint(1, 100)}",  # Random location name
        random.randint(1, 1000),  # Random location ID
        fake.company(),  # Random company name
        random.uniform(1.0, 100.0),  # Random transaction amount between 1.0 and 100.0
        random.choice(["Sale", "Return"]),  # Random transaction type
        random.choice(brand_names),  # Random brand name
        random.randint(1001, 2000),  # Random sale number between 1001 and 2000
        fake.date_time_between_dates(datetime_start=start_date, datetime_end=end_date).strftime("%Y-%m-%d %H:%M:%S"),  # Random business datetime
        fake.time(pattern="%H:%M"),  # Random hour
    ]
    data.append(row)

# Write the data to a CSV file
output_file = "data2.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)

# Print the full path of the generated CSV file
output_file_path = os.path.abspath(output_file)
print(f"{num_records} records generated and saved to: {output_file_path}")
