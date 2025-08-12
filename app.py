from flask import Flask, render_template, send_file, jsonify
from pymongo import MongoClient
import pandas as pd
import os

app = Flask(__name__)

# MongoDB Atlas connection URI
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI environment variable not set")

DB_NAME = "test"          # Your database name
COLLECTION_NAME = "songs" # Your collection name
CSV_FILE = "mongodb_export.csv"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Function to get data from MongoDB (excluding password)
def get_data():
    data = list(collection.find({}, {"_id": 0, "password": 0}))
    return data

# Route to render the table
@app.route("/")
def index():
    data = get_data()
    return render_template("index.html", data=data)

# Route to get refreshed data in JSON
@app.route("/refresh")
def refresh():
    data = get_data()
    return jsonify(data)

# Route to download CSV
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
