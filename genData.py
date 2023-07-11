from faker import Faker
import random
import json
import datetime
from pymongo import MongoClient
from pymongo import InsertOne
from tqdm import tqdm

fake = Faker('sv_SE')
fakeStd = Faker()

def generate_fake_data():
    base_date = fake.date_time_this_decade()
    first_name = fake.first_name()
    last_name = fake.last_name()

    data = {
        "partyUId": fake.uuid4(),
        "created": base_date.isoformat(),
        "createdSourceSystemId": fake.random_number(digits=6),
        "customerAccountState": fake.random_element(elements=('Active', 'Inactive', 'Pending')),
        "customerCategory": fake.random_element(elements=('Gold', 'Silver', 'Bronze')),
        "firstName": first_name,
        "genderCode": fake.random_element(elements=('M', 'F')),
        "initialBUCode": fake.random_number(digits=4),
        "initialBUType": fake.random_element(elements=('A', 'B', 'C')),
        "languageCode": fake.language_code(),
        "lastName": last_name,
        "status": fake.random_element(elements=('Active', 'Inactive')),
        "type": fake.random_element(elements=('Type1', 'Type2', 'Type3')),
        "updated": generate_updated_date(base_date).isoformat(),
        "updatedSourceSystemId": fake.random_number(digits=6),
        "addresses": generate_addresses(base_date),
        "contactMethods": generate_contact_methods(base_date, first_name, last_name),
        "integrityCodes": generate_integrity_codes(),
        "customerIdentifiers": generate_customer_identifiers(base_date),
        "loyaltyMemberships": generate_loyalty_memberships(),
        "logins": generate_logins(base_date),
        "cifAccountReferences": generate_cif_account_references(),
        "children": [],
        "contactResidences": [],
        "interestAreas": [],
        "communicationPreferences": [],
        "serviceQuestionnaires": []
    }
    return data

def generate_updated_date(base_date):
    variation = random.randint(1, 7)  # Number of days of variation
    updated_date = base_date + datetime.timedelta(days=variation)
    return updated_date

def generate_addresses(base_date):
    addresses = []
    for i in range(random.randint(1, 3)):
        address_date = base_date + datetime.timedelta(days=i)
        address = {
            "id": fake.random_number(digits=6),
            "careOfName": fake.first_name(),
            "city": fake.city(),
            "contextType": fake.random_element(elements=('Type1', 'Type2', 'Type3')),
            "country": "Sweden",
            "created": address_date.isoformat(),
            "nameSuffix": fake.suffix(),
            "postalCode": fake.postcode(),
            "state": fake.state(),
            "streetAddress1": fake.street_address(),
            "streetAddress2": fake.building_number() + " " + fake.random_element(elements=('A', 'B', 'C')),
            "title": fake.prefix(),
            "updated": address_date.isoformat(),
            "verificationCode": fake.random_number(digits=4)
        }
        addresses.append(address)
    return addresses



def generate_contact_methods(base_date, first_name, last_name):
    contact_methods = []
    for i in range(random.randint(1, 3)):
        contact_date = base_date + datetime.timedelta(days=i)
        contact_type = fake.random_element(elements=('SMS', 'EMAIL', 'PHONE'))
        if contact_type in ('SMS', 'PHONE'):
            value = fake.phone_number()
        else:
            value = generate_email(first_name, last_name)
        contact_method = {
            "id": fake.random_number(digits=6),
            "cMSValue": fake.random_number(digits=8),
            "value": value,
            "contextType": fake.random_element(elements=('Type1', 'Type2', 'Type3')),
            "created": contact_date.isoformat(),
            "type": contact_type,
            "updated": contact_date.isoformat(),
            "verificationBy": fake.first_name(),
            "verificationCode": fake.random_number(digits=4),
            "verificationDate": contact_date.date().isoformat(),
            "verificationExpiryDate": (contact_date + datetime.timedelta(days=30)).date().isoformat(),
            "lastValidatedOn": contact_date.date().isoformat(),
            "lastValidatedBy": fake.first_name(),
            "isValid": fake.boolean()
        }
        contact_methods.append(contact_method)
    return contact_methods

def generate_email(first_name, last_name):
    username = f"{first_name.lower()}.{last_name.lower()}"
    domain = fake.domain_name()
    if random.random() < 0.8:
        domain = fakeStd.domain_name()
    if random.random() < 0.7:
        username = username.replace("'", "").replace(" ", "").replace(".", "")
    else:
        username = username.replace("'", "").replace(" ", "")
    if random.random() < 0.9:
        # Add a random number to the email address
        username += str(random.randint(1, 99999))
    if random.random() < 0.7:
        # Add initials between two dots in the email address
        initials = f"{first_name[0].lower()}{last_name[0].lower()}"
        username = username.replace(".", f".{initials}.")
    if random.random() < 0.8:
        # Add a random word to the email address
        random_word = fakeStd.word().lower()
        position = random.randint(1, len(username) - 1)
        username = username[:position] + random_word + username[position:]

    return f"{username}@{domain}"




def generate_integrity_codes():
    integrity_codes = []
    for _ in range(random.randint(1, 3)):
        integrity_code = {
            "id": fake.random_number(digits=6),
            "consentCode": fake.random_element(elements=('Code1', 'Code2', 'Code3')),
            "created": fake.date_time_this_decade().isoformat(),
            "integrityType": fake.random_element(elements=('Type1', 'Type2', 'Type3')),
            "updated": fake.date_time_this_month().isoformat()
        }
        integrity_codes.append(integrity_code)
    return integrity_codes

def generate_customer_identifiers(base_date):
    customer_identifiers = []
    num_identifiers = random.randint(1, 5)
    for i in range(num_identifiers):
        identifier_date = base_date + datetime.timedelta(days=random.randint(1, 7))
        identifier = {
            "id": fake.random_number(digits=6),
            "created": identifier_date.isoformat(),
            "validFrom": identifier_date.isoformat(),
            "validUntil": (identifier_date + datetime.timedelta(days=random.randint(1, 365))).isoformat(),
            "customerId": fake.random_number(digits=8),
            "customerIdSource": fake.random_element(elements=('Source1', 'Source2', 'Source3')),
            "customerIdType": fake.random_element(elements=('Type1', 'Type2', 'Type3')),
            "updated": identifier_date.isoformat()
        }
        customer_identifiers.append(identifier)
    return customer_identifiers


def generate_loyalty_memberships():
    loyalty_memberships = []
    for _ in range(random.randint(1, 3)):
        loyalty_membership = {
            "id": fake.random_number(digits=6),
            "created": fake.date_time_this_decade().isoformat(),
            "programCode": fake.random_element(elements=('Program1', 'Program2', 'Program3')),
            "status": fake.random_element(elements=('Active', 'Inactive', 'Pending')),
            "updated": fake.date_time_this_month().isoformat(),
            "membershipCards": generate_membership_cards()
        }
        loyalty_memberships.append(loyalty_membership)
    return loyalty_memberships

def generate_membership_cards():
    membership_cards = []
    for _ in range(random.randint(1, 3)):
        membership_card = {
            "id": fake.random_number(digits=6),
            "cardCreator": fake.first_name(),
            "cardNumber": fake.credit_card_number(),
            "cardStatus": fake.random_element(elements=('Active', 'Inactive')),
            "cardType": fake.random_element(elements=('Type1', 'Type2', 'Type3')),
            "created": fake.date_time_this_decade().isoformat(),
            "updated": fake.date_time_this_month().isoformat()
        }
        membership_cards.append(membership_card)
    return membership_cards

def generate_logins(base_date):
    logins = []
    num_logins = random.randint(1, 5)
    for i in range(num_logins):
        login_date = base_date + datetime.timedelta(days=random.randint(1, 7))
        login = {
            "id": fake.random_number(digits=6),
            "loginType": fake.random_element(elements=('Type1', 'Type2', 'Type3')),
            "updated": login_date.isoformat(),
            "created": login_date.isoformat()
        }
        logins.append(login)
    return logins

def generate_cif_account_references():
    cif_account_references = []
    for _ in range(random.randint(1, 3)):
        cif_account_reference = {
            "customerNumber": fake.random_number(digits=6),
            "externalId": fake.random_number(digits=6),
            "partyUId": fake.uuid4(),
            "subscriptionStatus": fake.random_element(elements=('Active', 'Inactive')),
            "systemNumber": fake.random_number(digits=6)
        }
        cif_account_references.append(cif_account_reference)
    return cif_account_references

def convert_dates_to_datetime(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                convert_dates_to_datetime(value)
            elif isinstance(value, str) and is_iso_date(value):
                data[key] = datetime.datetime.fromisoformat(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            convert_dates_to_datetime(data[i])

def is_iso_date(date_string):
    try:
        datetime.datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False

# MongoDB connection settings
mongo_uri = ""
database_name = ""
collection_name = "profiles"

# Number of documents to insert
num_documents = 3000000


# Number of documents to insert in each bulk write operation
batch_size = 500

# Establish MongoDB connection
client = MongoClient(mongo_uri)
database = client[database_name]
collection = database[collection_name]

# Calculate the number of batches
num_batches = num_documents // batch_size


# Generate and insert documents in bulk write operations
with tqdm(total=num_documents, ncols=80) as pbar:
    for _ in range(num_batches):
        bulk_operations = []
        for _ in range(batch_size):
            document = generate_fake_data()
            convert_dates_to_datetime(document)
            bulk_operations.append(InsertOne(document))
        collection.bulk_write(bulk_operations)
        pbar.update(batch_size)

    # Insert the remaining documents
    remaining_documents = num_documents % batch_size
    if remaining_documents > 0:
        bulk_operations = []
        for _ in range(remaining_documents):
            document = generate_fake_data()
            bulk_operations.append(InsertOne(document))
        collection.bulk_write(bulk_operations)
        pbar.update(remaining_documents)

# Close MongoDB connection
client.close()
