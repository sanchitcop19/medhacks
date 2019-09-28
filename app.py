import collections
from flask import Flask, request, render_template, Response
import json

app = Flask(__name__)
'''
app.config['MONGODB_SETTINGS'] = {
    'db': 'medhacks',
    'host': ''
}
'''
#client = pymongo.MongoClient("mongodb+srv://admin:<password>@medhacks-s3dxi.gcp.mongodb.net/test?retryWrites=true&w=majority")
#db = client.test

#mydoc = db.medhacks.find()
#for x in mydoc:
#  print(x)
@app.route("/", methods = ["GET", "POST"])
def home_page():
    data = request.form
    store = collections.defaultdict(list)
    try:
        with open("store.json") as file:
            store = json.load(file)
    except FileNotFoundError:
        pass
    with open("store.json", "w") as file:
        store['data'].append(data)
        json.dump(store, file)
    return Response(status=200)

@app.route('/info')
def info():
    store = None
    with open("store.json") as file:
        store = json.load(file)
    return render_template('list.html', info = store)

if __name__ == '__main__':
    app.run(debug=True)
