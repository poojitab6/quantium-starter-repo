import csv
from pathlib import Path

data_files = [Path('.\data\daily_sales_data_0.csv'), 
              Path('.\data\daily_sales_data_1.csv'),
              Path('.\data\daily_sales_data_2.csv')]

output_path = Path('.\data\output.csv')

with open(output_path, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['sales', 'date', 'region']) # HEADER

    for file_path in data_files:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['product'] == 'pink morsel':
                    price = float(row['price'].replace('$',''))
                    quantity = int(row['quantity'])
                    sales = price * quantity
                    writer.writerow([sales, row['date'], row['region']])