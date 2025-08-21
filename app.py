from flask import Flask, render_template, send_file, jsonify
from pymongo import MongoClient
import pandas as pd
import os

app = Flask(__name__)

# Get Mongo URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI environment variable not set")

DB_NAME = "production"          # Your DB name
COLLECTION_NAME = "leads" # Your collection name
CSV_FILE = "mongodb_export.csv"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_data():
    # Find all, exclude password, sort by _id ascending
    data = list(collection.find({}, {"password": 0}).sort("_id", 1))
    # Remove _id from each dict for clean output
    for d in data:
        d.pop("_id", None)
    return data

@app.route("/")
def index():
    data = get_data()
    return render_template("index.html", data=data)

@app.route("/download")
def download():
    data = get_data()
    if data:
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False)
        return send_file(CSV_FILE, as_attachment=True)
    else:
        return "No data to export."

if __name__ == "__main__":
    app.run(debug=True)
