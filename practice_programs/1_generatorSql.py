import mysql.connector
from tabulate import tabulate

def fetch_employees(batch_size=1000, limit=10):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # our database password
        database="employees"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM employees LIMIT {limit};")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row  # generator yields row one at a time

    cursor.close()
    conn.close()


# Example usage
limit = int(input("Enter the no. of records you want to see: "))
batch_size = int(input("Enter the no. of records you want to batch together: "))
rows = list(fetch_employees(batch_size, limit))
batch = []

for i, row in enumerate(rows, start=1):
    batch.append(row)
    
    # If we reach batch size or last row, print table
    if i % batch_size == 0 or i == limit:
        headers = batch[0].keys()
        table = [r.values() for r in batch]
        print(f"\nBatch {((i-1)//batch_size)+1}:\n")
        print(tabulate(table, headers=headers, tablefmt="grid"))
        batch = []  # reset for next batch