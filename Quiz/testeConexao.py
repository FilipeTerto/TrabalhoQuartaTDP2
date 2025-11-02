from repository.quiz_repository import db, client

print("Bancos disponíveis:", client.list_database_names())
print(db.list_collection_names())