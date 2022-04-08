import csv
import random

EXAMPLES = ['bread', 'flour', 'cheese', 'rice', 'cereal', 'porridge', 'steak',
            'beef', 'onion', 'sausage', 'egg', 'fish', 'spaghetti', 'beer',
            'burger', 'chicken', 'orange', 'apple', 'pear', 'cucumber']

items = [sorted(random.sample(EXAMPLES, random.randint(2, 5))) for _ in range(1000)]
items.sort()
with open('order_bd.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for item in items:
        writer.writerow(item)
