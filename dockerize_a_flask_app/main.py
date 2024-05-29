from flask import Flask, render_template
import time
import json
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    # now = time.ctime()
    # response = json.dumps({"response_time": now, "response_id": str(uuid.uuid4())})
    return render_template("home.html")
@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')
