class Eve:
    def __init__(self, db):
        self.db = db

    def get_moon_by_id(self, moon_id):
        self.db.execute("SELECT * FROM mapDenormalize WHERE itemID=?", (moon_id,))
        location = self.db.fetchone()
        return {
            'id': location['itemID'],
            'name': location['itemName'],
        }

    def get_planet_by_id(self, planet_id):
        self.db.execute("SELECT itemID, itemName, solarSystemID FROM mapDenormalize WHERE itemID=?", (planet_id,))
        location = self.db.fetchone()
        return {
            'id': location['itemID'],
            'name': location['itemName'],
            'system_id': location['solarSystemID'],
        }

    def get_system_by_id(self, system_id):
        self.db.execute("SELECT itemID, itemName FROM mapDenormalize WHERE itemID=?", (system_id,))
        location = self.db.fetchone()
        return {
            'id': location['itemID'],
            'name': location['itemName'],
        }

    def get_item_by_id(self, item_id):
        self.db.execute("SELECT typeID, typeName FROM invTypes WHERE typeID=?", (item_id,))
        item = self.db.fetchone()
        return {
            'id': item['typeID'],
            'name': item['typeName'],
        }
