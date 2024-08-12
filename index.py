import pandas as pd
import psycopg2

# Step 1: Convert Excel to CSV
file_path = 'C3 upload.xlsx'
excel_data = pd.read_excel(file_path)
csv_file_path = 'C3_upload.csv'
excel_data.to_csv(csv_file_path, index=False)

# Read the CSV file
data = pd.read_csv(csv_file_path)

print(data.head())

# Step 2: Load CSV into PostgreSQL
# Database connection parameters
db_params = {
    'dbname': '******',
    'user': '*******',
    'password': '*********',
    'host': '********',
    'port': '5432'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Read the CSV file
data = pd.read_csv(csv_file_path)

# Insert data into the database
for index, row in data.iterrows():
    insert_query = """
    INSERT INTO digiports.part (part_number, description, signal_code, weight, length, width, height)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    weight = row['weight']
    length = row['length']
    width = row['width']
    height = row['height']
    print(insert_query, weight, length, width, height)
    cur.execute(insert_query, (
        row['part_number'],
        row['description'],
        row['signal_code'],
        round(weight, 2),
        round(length, 2),
        round(width, 2),
        round(height, 2)
    )
                )

# Commit the transaction
conn.commit()

# Close the database connection
cur.close()
conn.close()
