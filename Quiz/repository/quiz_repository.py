from pymongo import MongoClient

MONGO_URI = "mongodb+srv://myAtlasDBUser:remus@myatlasclusteredu.mbai5d.mongodb.net/quiz?retryWrites=true&w=majority"
DB_NAME = "quiz"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

print("Mongo conectado XD")
