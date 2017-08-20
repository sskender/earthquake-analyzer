class Quake():
    def __init__(self,feature):
        self.code      = feature["properties"]["code"]
        self.place     = feature["properties"]["place"]
        self.magnitude = feature["properties"]["mag"]
        self.longitude = feature['geometry']['coordinates'][0]
        self.latitude  = feature['geometry']['coordinates'][1]
        self.depth     = feature['geometry']['coordinates'][2]
        self.tsunami   = feature["properties"]["tsunami"]
        self.alert     = feature["properties"]["alert"]
        self.felt      = feature["properties"]["felt"]