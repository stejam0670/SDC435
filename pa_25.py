# Stephen James
# 2026-06-27
# Performance Assessment 2.5
# Purpose: Create a menu-driven Python program that uses CRUD operations
# with PyMongo and the ReviewData collection in a MongoDB database.

import json
import pymongo

# Store the connection information in variables so it is easy to change.
CONNECTION_STRING = "mongodb://localhost:27017/"
DATABASE_NAME = "Amazon"
COLLECTION_NAME = "ReviewData"
DATA_FILE = "dataset_en_dev.json"


# Print a document without the MongoDB _id field so the output is cleaner.
def print_document(document):
    if document is None:
        print("No document was found.")
    else:
        if "_id" in document:
            document.pop("_id")
        print(document)


# Import sample review documents from the JSON file if the collection is empty.
def import_data_if_needed(collection):
    if collection.count_documents({}) == 0:
        print("Importing data from file...")
        for line in open(DATA_FILE, "r"):
            data_set = json.loads(line)
            collection.insert_one(data_set)
        print("Data imported successfully!")


# *Create a new document in the ReviewData collection.
def add_document(collection):
    print("\nAdd a new review document")
    review_id = input("Enter review_id: ")
    product_id = input("Enter product_id: ")
    reviewer_id = input("Enter reviewer_id: ")
    stars = input("Enter number of stars: ")
    review_body = input("Enter review body: ")
    review_title = input("Enter review title: ")
    language = input("Enter language: ")
    product_category = input("Enter product category: ")

    new_document = {
        "review_id": review_id,
        "product_id": product_id,
        "reviewer_id": reviewer_id,
        "stars": stars,
        "review_body": review_body,
        "review_title": review_title,
        "language": language,
        "product_category": product_category,
    }

    collection.insert_one(new_document)
    print("New document inserted.")


# *Retrieve one document from the ReviewData collection using find_one().
def find_one_document(collection):
    review_id = input("\nEnter the review_id to find: ")
    query = {"review_id": review_id}
    document = collection.find_one(query)
    print_document(document)


# *Retrieve documents using find() and filter for greater than or equal stars.
def find_stars_greater_equal(collection):
    stars = input("\nEnter the minimum number of stars: ")
    query = {"stars": {"$gte": stars}}
    show_fields = {"_id": False, "review_id": True, "stars": True, "review_title": True}
    data = collection.find(query, show_fields).limit(10)

    for document in data:
        print(document)


# *Retrieve documents using find() and filter for less than stars.
def find_stars_less_than(collection):
    stars = input("\nEnter the number of stars to search below: ")
    query = {"stars": {"$lt": stars}}
    show_fields = {"_id": False, "review_id": True, "stars": True, "review_title": True}
    data = collection.find(query, show_fields).limit(10)

    for document in data:
        print(document)


# *Retrieve documents using find() and filter for a word in the review_title.
def find_word_in_title(collection):
    word = input("\nSearch the title for: ")
    query = {"review_title": {"$regex": word, "$options": "i"}}
    show_fields = {
        "_id": False,
        "stars": True,
        "review_title": True,
        "review_body": True,
    }
    data = collection.find(query, show_fields).limit(10)

    for document in data:
        print(document)


# *Retrieve documents using find() and filter for a word in the review_body.
def find_word_in_body(collection):
    word = input("\nSearch the review body for: ")
    query = {"review_body": {"$regex": word, "$options": "i"}}
    show_fields = {
        "_id": False,
        "stars": True,
        "review_title": True,
        "review_body": True,
    }
    data = collection.find(query, show_fields).limit(10)

    for document in data:
        print(document)


# Show a query menu for all required read operations.
def query_menu(collection):
    print("\nPlease type in a number and press enter to execute the menu option")
    print("1. Query by reviewID")
    print("2. Filter for a number of stars and greater")
    print("3. Filter for less than a number of stars")
    print("4. Filter for a word in the title")
    print("5. Filter for a word in the review body content")

    choice = input()

    if choice == "1":
        find_one_document(collection)
    elif choice == "2":
        find_stars_greater_equal(collection)
    elif choice == "3":
        find_stars_less_than(collection)
    elif choice == "4":
        find_word_in_title(collection)
    elif choice == "5":
        find_word_in_body(collection)
    else:
        print("That is not a valid query option.")


# *Allow the user to enter a field and update a value in a document.
def update_document(collection):
    review_id = input("\nEnter the review_id of the document to update: ")
    field_name = input("Enter the field name to update: ")
    new_value = input("Enter the new value: ")

    query = {"review_id": review_id}
    update_data = {"$set": {field_name: new_value}}
    result = collection.update_one(query, update_data)

    if result.modified_count > 0:
        print("Document updated to:")
        print_document(collection.find_one(query))
    else:
        print("No document was updated.")


# *Allow the user to enter a document ID and delete that document.
def delete_document(collection):
    review_id = input("\nEnter the review_id of the document to delete: ")
    query = {"review_id": review_id}
    result = collection.delete_one(query)

    print("Number of documents deleted: " + str(result.deleted_count))


# *Menu option to remove all documents in the ReviewData collection.
def delete_all_documents(collection):
    answer = input("\nType YES to delete all documents from the collection: ")

    if answer == "YES":
        result = collection.delete_many({})
        print("Number of documents deleted: " + str(result.deleted_count))
    else:
        print("No documents were deleted.")


# *Menu option to delete the ReviewData collection from the Amazon database.
def delete_collection(collection):
    answer = input("\nType YES to delete the collection: ")

    if answer == "YES":
        collection.drop()
        print("Collection removed!")
    else:
        print("Collection was not removed.")


# Display the main CRUD menu.
def display_menu():
    print("\nType in a number and press enter to execute the menu option.")
    print("1. Query for documents")
    print("2. Add a new document")
    print("3. Update fields of a document")
    print("4. Delete a document")
    print("5. Delete all documents from the collection")
    print("6. Delete a collection")
    print("7. Exit the program")


# Main program section connects to MongoDB and keeps the menu running.
print("Connecting to Amazon Mongo database...")
myClient = pymongo.MongoClient(CONNECTION_STRING)
db = myClient[DATABASE_NAME]
myCollection = db[COLLECTION_NAME]

import_data_if_needed(myCollection)

menu_choice = ""

while menu_choice != "7":
    display_menu()
    menu_choice = input()

    if menu_choice == "1":
        query_menu(myCollection)
    elif menu_choice == "2":
        add_document(myCollection)
    elif menu_choice == "3":
        update_document(myCollection)
    elif menu_choice == "4":
        delete_document(myCollection)
    elif menu_choice == "5":
        delete_all_documents(myCollection)
    elif menu_choice == "6":
        delete_collection(myCollection)
    elif menu_choice == "7":
        print("Program has ended!")
    else:
        print("That is not a valid menu option.")
