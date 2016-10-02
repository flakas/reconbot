class Eve:
    def __init__(self, db, eve_api):
        self.db = db
        self.eve_api = eve_api

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

    def get_alliance_name_by_id(self, alliance_id):
        return self.eve_api.character_names_from_ids(alliance_id).result[alliance_id]

    def get_corporation_name_by_id(self, corporation_id):
        return self.eve_api.character_names_from_ids(corporation_id).result[corporation_id]

    def get_character_by_id(self, character_id):
        return self.eve_api.affiliations_for_character(character_id).result
