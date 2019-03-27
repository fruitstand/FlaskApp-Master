#As far as I know, to use MySQLClient you import MySQLdbß
import MySQLdb #Both modules are manually installed, use Pip if needed
import geopy.distance

def findVendors(FruitList, Coordinates):

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                        user="root",         # your username
                        passwd="1Light8Candles!",  # your password
                        db="FruitStand")        # name of the data base
    cur = db.cursor()

    MYSQLstring = "WHERE "
    for x in FruitList:
        MYSQLstring = MYSQLstring + "Fruit = '" + x + "'"

        if x != FruitList[-1]:
            MYSQLstring = MYSQLstring + " OR "


    cur.execute("SELECT VendorName, Latitude, Longitude FROM Vendors " 
                "WHERE Vendor_id " 
                "IN (SELECT Vendor_id " 
                "FROM VmapF JOIN Fruits "
                "ON Fruits.Fruit_id = VmapF.Fruit_id " +
                MYSQLstring +
                ")")
    db.close()


    VendorDict = {}
    for row in cur.fetchall():
        VendorDistance = geopy.distance.geodesic([row[1],row[2]], Coordinates).mi
        VendorDict.update({row[0]: [round(VendorDistance,2),row[1],row[2]]})

    GoodList = sorted(VendorDict.items(), key=lambda x: x[1]) #Sorts the dictionary and returns a list of tuples
    SRcount = len(GoodList) #How many matching Vendors were found

    searchData = {"SearchResults": 
        {          
        "searchCount": str(SRcount) + " matches found",
        "userCoordinates":  {"ULat":Coordinates[0], "ULong": Coordinates[1]}
    },
        "vendors": []
    }

    for y in GoodList:
        
        searchData["vendors"].append(
            {
            "distance": str(y[1][0]) + " mi away",               
            "vendorName": y[0],
            "vendorAddress": {"Lat":y[1][1], "Long": y[1][2]}
        })
        
    print(searchData)
    return(searchData)

"""For testing
fruit = ["Apples","Oranges","Grapes"]
cors = (38.7105, -121.35634)

findVendors(fruit, cors)
"""