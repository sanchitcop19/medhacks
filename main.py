import collections
import googlemaps
from flask import Flask, request, render_template, Response, make_response, url_for
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

@app.route("/home", methods = ["GET"])
def home():
    return render_template("home.html")

@app.route("/", methods = ["GET", "POST", "OPTIONS"])
def home_page():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Max-Age"] = 86400
        response.headers["Content-Type"] = "application/json"
        return response
    import json

    data = json.loads(str(request.data).replace('\\n', '')[2:-1])
    lat = data['latitude']
    lon = data['longitude']
    client = googlemaps.Client(key= 'AIzaSyB2ekBwXRcw-dI5afMnf4Nck7JwXpNEDXI')
    geocode = client.reverse_geocode((lat, lon))
    data['location'] = geocode[0]['formatted_address']
    store = collections.defaultdict(list)
    try:
        with open("store.json") as file:
            store = json.load(file)
    except FileNotFoundError:
        pass
    with open("store.json", "w") as file:
        if data:
            store['data'].append(data)
        json.dump(store, file)
    return Response(status=200)

@app.route('/info')
def info():
    store = None
    try:
        with open("store.json") as file:
            store = json.load(file)
    except FileNotFoundError:
        pass
    if not store:
        return Response(status=404)
    return render_template('list.html', info = store)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
