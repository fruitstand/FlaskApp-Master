from flask import Flask, render_template
from flask import jsonify, request
import json
#As far as I know, to use MySQLClient you import MySQLdbß
import MySQLdb #Both modules are manually installed, use Pip if needed
import geopy.distance
from vendorAlgorithm import findVendors

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to FruitStand!"

@app.route("/export")
def export():
    return render_template('flatListData.json')

@app.route('/summary', methods = ['GET','POST'])
def summary():
    d = {
  "placeHolderData": "Does nothing for the time being",
}
    if request.method == 'GET':
      return jsonify(d)

    elif request.method == 'POST':
      dataDict = request.get_json()
      print(dataDict)

      userlat = dataDict['userlat']
      userlong = dataDict['userlong']

      userCoords = (userlat, userlong)
      
      desiredFruit = []
      for key, value in dataDict['fruits'].items():
        if value == True:
          desiredFruit.append(key)
      print(desiredFruit)
      
      flatlistData = findVendors(desiredFruit, userCoords)


      return jsonify(flatlistData)

if __name__ == "__main__":
    """change this code depending on local ip"""
    app.run(debug=True)
    #app.run(host='192.168.1.5')