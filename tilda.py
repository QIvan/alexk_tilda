import csv
import re
import sys


class Person:
    def __init__(self, phone, utm_source, utm_medium, utm_campaign, utm_content, utm_term):
        self.phone = phone
        self.utm_source = utm_source
        self.utm_medium = utm_medium
        self.utm_campaign = utm_campaign
        self.utm_content = utm_content
        self.utm_term = utm_term
        self.purchaseList = []

    def addPurchase(self, purchase):
        self.purchaseList.append(purchase)


def convertPhone(param: str):
    return re.sub('[^0-9]', '', param)


def parse_and_enrich_purchases(purchase_csv, people):
    global csvfile, reader, row, phone, person
    with open(purchase_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            phone = row['Телефон']
            person = people.get(phone, None)
            if person is not None:
                person.addPurchase(
                    [row['Дата продажи'], row['Название услуги'], row['Стоимость номенклатуры']]
                )


people_csv = sys.argv[1]
if people_csv is None:
    sys.exit('Дай csv с людями')

if len(sys.argv) < 3:
    sys.exit('Дай csv[\'шки] с продажами')

people = {}
print('Парсим людей из ' + people_csv)
with open(people_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        phone = convertPhone(row['Phone'])
        person = Person(phone,
                        row['utm_source'],
                        row['utm_medium'],
                        row['utm_campaign'],
                        row['utm_content'],
                        row['utm_term'])
        people[phone] = person

for i in range(2, len(sys.argv)):
    purchase_csv = sys.argv[i]
    print('парсим  ̶б̶л̶я̶д̶е̶й̶ покупки из ' + purchase_csv)
    parse_and_enrich_purchases(purchase_csv, people)


with open('tilda.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['phone', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'])
    for key in people:
        person = people[key]
        writer.writerow(
            [person.phone,
             person.utm_source,
             person.utm_medium,
             person.utm_campaign,
             person.utm_content,
             person.utm_term
             ]
            +
            [item for sublist in person.purchaseList for item in sublist]
        )


with open('tilda.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print(row)
