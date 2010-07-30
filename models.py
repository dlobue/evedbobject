
from sqlobject import *
import os

db_filename = os.path.abspath('ccp_dump.db')
connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string, debug=True, debugOutput=True,
                             autoCommit=False)
#connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

#__connection__ = connection_string
#__connection__.style = MixedCaseStyle(longID=True)


class agtAgents(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        #table = 'tablename'
        idName = 'agentID'
    division = ForeignKey('crpNPCDivisions', dbName='divisionID')
    corporation = ForeignKey('crpNPCCorporations', dbName='corporationID')
    location = ForeignKey('staStations', dbName='locationID')
    level = IntCol()
    quality = IntCol()
    agentType = ForeignKey('agtAgentTypes', dbName='agentTypeID')


class agtAgentTypes(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'agentTypeID'
    agentType = StringCol()
    agents = MultipleJoin('agtAgents', joinColumn='agentTypeID')


class crpActivities(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'activityID'
    activityName = StringCol()
    description = StringCol()


class crpNPCCorporations(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'corporationID'
        fromDatabase = True
    size = StringCol(length=1, varchar=False)
    extent = StringCol(length=1, varchar=False)
    solarSystem = ForeignKey('mapSolarSystems', dbName='solarSystemID')
    friend = ForeignKey('crpNPCCorporations', dbName='friendID')
    enemy = ForeignKey('crpNPCCorporations', dbName='enemyID')
    scattered = BoolCol()
    fringe = IntCol()
    corridor = IntCol()
    hub = IntCol()
    border = IntCol()
    faction = ForeignKey('chrFactions', dbName='factionID')
    stationCount = IntCol()
    stationSystemCount = IntCol()
    description = StringCol()
    agents = MultipleJoin('agtAgents', joinColumn='corporationID')
    stations = MultipleJoin('staStations', joinColumn='corporationID')


class crpNPCDivisions(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'divisionID'
    divisionName = StringCol()
    description = StringCol()
    leaderType = StringCol()
    agents = MultipleJoin('agtAgents', joinColumn='divisionID')
    #TODO: do a multiplejoin for stations?


'''
class eveNames(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'itemID'
    itemName = StringCol()
    category = ForeignKey('invCategories', dbName='categoryID')
    group = ForeignKey('invGroups', dbName='groupID')
    type = ForeignKey('invTypes', dbName='typeID')


class invCategories(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'categoryID'
        fromDatabase = True
    categoryName = StringCol()
    description = StringCol()


class invGroups(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'groupID'
        fromDatabase = True
    category = ForeignKey('invCategories', dbName='categoryID')
    groupName = StringCol()
    description = StringCol()

class invTypes(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'typeID'
        fromDatabase = True
    group = ForeignKey('invGroups', dbName='groupID')
'''


class mapSolarSystems(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'solarSystemID'
        fromDatabase = True
    region = ForeignKey('mapRegions', dbName='regionID')
    constellation = ForeignKey('mapConstellations', dbName='constellationID')
    faction = ForeignKey('chrFaction', dbName='factionID')
    solarSystemName = StringCol()
    border = BoolCol()
    fringe = BoolCol()
    corridor = BoolCol()
    hub = BoolCol()
    international = BoolCol()
    regional = BoolCol()
    interconstellation = BoolCol(dbName='constellation')
    security = FloatCol()
    jumps = MultipleJoin('mapSolarSystemJumps', joinColumn='fromSolarSystem')
    corporations = MultipleJoin('crpNPCCorporations',
                                joinColumn='solarSystemID')
    stations = MultipleJoin('staStations', joinColumn='solarSystemID')


class mapSolarSystemJumps(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'ROWID'
    fromSolarSystem = ForeignKey('mapSolarSystems', notNone=True,
                                 cascade=True, dbName='fromSolarSystemID')
    fromRegion = ForeignKey('mapRegions', dbName='fromRegionID')
    fromConstellation = ForeignKey('mapConstellations',
                                   dbName='fromConstellationID')
    toSolarSystem = ForeignKey('mapSolarSystems', notNone=True, cascade=True,
                              dbName='toSolarSystemID')
    toRegion = ForeignKey('mapRegions', dbName='toRegionID')
    toConstellation = ForeignKey('mapConstellations', dbName='toRegionID')
    #unique = index.DatabaseIndex('fromSolarSystem', 'toSolarSystem',
    #                             unique=True)


class mapConstellations(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'constellationID'
        fromDatabase = True
    constellationName = StringCol()
    region = ForeignKey('mapRegions', dbName='regionID')
    faction = ForeignKey('chrFactions', dbName='factionID')
    jumps = MultipleJoin('mapConstellationJumps',
                         joinColumn='fromConstellation')
    solarSystems = MultipleJoin('mapSolarSystems', joinColumn='constellationID')
    stations = MultipleJoin('staStations', joinColumn='constellationID')
    #TODO: multiplejoin for corporations & agents
    #no wait, that's a RELATED join!


class mapConstellationJumps(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'ROWID'
    fromRegion = ForeignKey('mapRegions', dbName='fromRegionID')
    fromConstellation = ForeignKey('mapConstellations', notNone=True,
                                   cascade=True, dbName='fromConstellationID')
    toRegion = ForeignKey('mapRegions', dbName='toRegionID')
    toConstellation = ForeignKey('mapConstellations', notNone=True,
                                 cascade=True, dbName='toConstellationID')
    #unique = index.DatabaseIndex('fromConstellation', 'toConstellation',
    #                             unique=True)


class mapRegions(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'regionID'
        fromDatabase = True
    regionName = StringCol()
    faction = ForeignKey('chrFactions', dbName='factionID')
    jumps = MultipleJoin('mapRegionJumps', joinColumn='fromRegion')
    solarSystems = MultipleJoin('mapSolarSystems', joinColumn='regionID')
    stations = MultipleJoin('staStations', joinColumn='regionID')
    constellations = MultipleJoin('mapConstellations', joinColumn='regionID')
    #TODO: agents, corps, etc


class mapRegionJumps(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'ROWID'
    fromRegion = ForeignKey('mapRegions', notNone=True, cascade=True,
                            dbName='fromRegionID')
    toRegion = ForeignKey('mapRegions', notNone=True, cascade=True,
                          dbName='toRegionID')
    #unique = index.DatabaseIndex('fromRegion', 'toRegion',
    #                             unique=True)


class chrFactions(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'factionID'
        fromDatabase = True
    factionName = StringCol()
    description = StringCol()
    solarSystem = ForeignKey('mapSolarSystems', dbName='solarSystemID')
    corporation = ForeignKey('crpNPCCorporations', dbName='corporationID')
    militiaCorporation = ForeignKey('crpNPCCorporations',
                                    dbName='militiaCorporationID')
    corporations = MultipleJoin('crpNPCCorporations', joinColumn='factionID')
    solarSystems = MultipleJoin('mapSolarSystems', joinColumn='factionID')
    constellations = MultipleJoin('mapConstellations', joinColumn='factionID')
    regions = MultipleJoin('mapRegions', joinColumn='factionID')
    #TODO: agents, stations


class staStations(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'stationID'
        fromDatabase = True
    security = IntCol()
    stationType = ForeignKey('staStationTypes', dbName='stationTypeID')
    operation = ForeignKey('staOperations', dbName='operationID')
    corporation = ForeignKey('chrNPCCorporations', dbName='corporationID')
    solarSystem = ForeignKey('mapSolarSystems', dbName='solarSystemID')
    constellation = ForeignKey('mapConstellations', dbName='constellationID')
    region = ForeignKey('mapRegions', dbName='regionID')
    stationName = StringCol()
    agents = MultipleJoin('agtAgents', joinColumn='locationID')


class staOperations(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'operationID'
        fromDatabase = True
    operationName = StringCol()
    description = StringCol()
    services = RelatedJoin('staServices',
                           intermediateTable='staOperationServices',
                           createRelatedTable=False, joinColumn='operationID',
                           otherColumn='serviceID')

class staServices(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'serviceID'
    serviceName = StringCol()
    description = StringCol()
    operations = RelatedJoin('staOperations',
                           intermediateTable='staOperationServices',
                           createRelatedTable=False, otherColumn='operationID',
                           joinColumn='serviceID')



class staStationTypes(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
        idName = 'stationTypeID'
        fromDatabase = True
    operation = ForeignKey('staOperations', dbName='operationID')
    conquerable = BoolCol()




if __name__ == '__main__':
    #print(chrFactions.get(1))
    print(chrFactions.get(500001))


