from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/disasters")
def get_disasters():
    return jsonify([
        {
            "title": "Flood in Assam",
            "description": "Heavy rainfall has caused major flooding in the Assam region.",
            "url": "https://example.com/flood-assam"
        },
        {
            "title": "Earthquake in Nepal",
            "description": "5.2 magnitude earthquake hit western Nepal this morning.",
            "url": "https://example.com/earthquake-nepal"
        }
    ])

if __name__ == "__main__":
    app.run(debug=True)
