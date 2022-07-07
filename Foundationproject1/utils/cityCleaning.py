import utils.cityZoneList as cz
import pandas as pd


def cityToZoneMapping(df):

    l = set()

    for cityList in df['Location']:
        for city in cityList.split(','):
            l.add(city.strip())

    cityZonedict = dict()

    for city in l:
        zones = set()
        if any(substring in city.lower().strip() for substring in cz.northList):
            zones.add('north')
            cityZonedict[city] = zones
        if any(substring in city.lower().strip() for substring in cz.southList):
            zones.add('south')
            cityZonedict[city] = zones
        if any(substring in city.lower().strip() for substring in cz.eastList):
            zones.add('east')
            cityZonedict[city] = zones
        if any(substring in city.lower().strip() for substring in cz.westList):
            zones.add('west')
            cityZonedict[city] = zones

    # print(cityZonedict)

    def assignZones(cityList):
        z = set()
        for i in cityList.split(','):
            z.update(cityZonedict[i.strip()])
        return z

    df['Zone'] = df['Location'].map(lambda x: assignZones(x))
    df.drop('Location', axis=1, inplace=True)

    return df
