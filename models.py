
from sqlobject import *
import os

db_filename = os.path.abspath('ccp_dump.db')
connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection


class agtAgents(SQLObject):
    class sqlmeta:
        #table = 'tablename'
        idName = 'agentID'
        style = MixedCaseStyle()
    division = ForeignKey('crpNPCDivisions')
    corporation = ForeignKey('crpNPCCorporations')
    location = ForeignKey('staStations')
    level = IntCol()
    quality = IntCol()
    agentType = ForeignKey('agtAgentTypes')


class agtAgentTypes(SQLObject):
    class sqlmeta:
        idName = 'agentTypeID'
        style = MixedCaseStyle()
    agentType = StringCol()
    agents = MultipleJoin('agtAgents')


#class agtConfig(SQLObject):
    #    class sqlmeta:
        #        idName = 'agentID'
        #        style = MixedCaseStyle()
        #    k = StringCol()
        #    v = StringCol()


class crpActivities(SQLObject):
    class sqlmeta:
        idName = 'activityID'
        style = MixedCaseStyle()
    activityName = StringCol()
    description = StringCol()


class crpNPCCorporations(SQLObject):
    class sqlmeta:
        idName = 'corprationID'
        style = MixedCaseStyle()
        fromDatabase = True
    size = StringCol(length=1, varchar=False)
    extent = StringCol(length=1, varchar=False)
    solarSystem = ForeignKey('mapSolarSystems')
    friend = ForeignKey('crpNPCCorporations')
    enemy = ForeignKey('crpNPCCorporations')
    scattered = BoolCol()
    fringe = IntCol()
    corridor = IntCol()
    hub = IntCol()
    border = IntCol()
    faction = ForeignKey('chrFactions')
    stationCount = IntCol()
    stationSystemCount = IntCol()
    description = StringCol()
    agents = MultipleJoin('agtAgents')
    stations = MultipleJoin('staStations')


class crpNPCDivisions(SQLObject):
    class sqlmeta:
        idName = 'divisionID'
        style = MixedCaseStyle()
    divisionName = StringCol()
    description = StringCol()
    leaderType = StringCol()
    agents = MultipleJoin('agtAgents')
    #TODO: do a multiplejoin for stations?


class eveNames(SQLObject):
    class sqlmeta:
        idName = 'itemID'
        style = MixedCaseStyle()
    itemName = StringCol()
    category = ForeignKey('invCategories')
    group = ForeignKey('invGroups')
    type = ForeignKey('invTypes')


class invCategories(SQLObject):
    class sqlmeta:
        idName = 'categoryID'
        style = MixedCaseStyle()
        fromDatabase = True
    categoryName = StringCol()
    description = StringCol()


class invGroups(SQLObject):
    class sqlmeta:
        idName = 'groupID'
        style = MixedCaseStyle()
        fromDatabase = True
    category = ForeignKey('invCategories')
    groupName = StringCol()
    description = StringCol()

class invTypes(SQLObject):
    class sqlmeta:
        idName = 'typeID'
        style = MixedCaseStyle()
        fromDatabase = True
    group = ForeignKey('invGroups')



class mapSolarSystems(SQLObject):
    class sqlmeta:
        idName = 'solarSystemID'
        style = MixedCaseStyle()
        fromDatabase = True
    region = ForeignKey('mapRegions')
    constellation = ForeignKey('mapConstellations')
    faction = ForeignKey('chrFaction')
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
    corporations = MultipleJoin('crpNPCCorporations')
    stations = MultipleJoin('staStations')


class mapSolarSystemJumps(SQLObject):
    class sqlmeta:
        idName = 'ROWID'
        style = MixedCaseStyle()
    fromSolarSystem = ForeignKey('mapSolarSystems', notNull=True, cascade=True)
    fromRegion = ForeignKey('mapRegions')
    fromConstellation = ForeignKey('mapConstellations')
    toSolarSystem = ForeignKey('mapSolarSystems', notNull=True, cascade=True)
    toRegion = ForeignKey('mapRegions')
    toConstellation = ForeignKey('mapConstellations')
    unique = index.DatabaseIndex('fromSolarSystem', 'toSolarSystem',
                                 unique=True)


class mapConstellations(SQLObject):
    class sqlmeta:
        idName = 'constellationID'
        style = MixedCaseStyle()
        fromDatabase = True
    constellationName = StringCol()
    region = ForeignKey('mapRegions')
    faction = ForeignKey('chrFactions')
    jumps = MultipleJoin('mapConstellationJumps',
                         joinColumn='fromConstellation')
    solarSystems = MultipleJoin('mapSolarSystems')
    stations = MultipleJoin('staStations')
    #TODO: multiplejoin for corporations & agents
    #no wait, that's a RELATED join!


class mapConstellationJumps(SQLObject):
    class sqlmeta:
        idName = 'ROWID'
        style = MixedCaseStyle()
    fromRegion = ForeignKey('mapRegions')
    fromConstellation = ForeignKey('mapConstellations', notNull=True, cascade=True)
    toRegion = ForeignKey('mapRegions')
    toConstellation = ForeignKey('mapConstellations', notNull=True, cascade=True)
    unique = index.DatabaseIndex('fromConstellation', 'toConstellation',
                                 unique=True)


class mapRegions(SQLObject):
    class sqlmeta:
        idName = 'regionID'
        style = MixedCaseStyle()
        fromDatabase = True
    regionName = StringCol()
    faction = ForeignKey('chrFactions')
    jumps = MultipleJoin('mapRegionJumps', joinColumn='fromRegion')
    solarSystems = MultipleJoin('mapSolarSystems')
    stations = MultipleJoin('staStations')
    constellations = MultipleJoin('mapConstellations')
    #TODO: agents, corps, etc


class mapRegionJumps(SQLObject):
    class sqlmeta:
        idName = 'ROWID'
        style = MixedCaseStyle()
    fromRegion = ForeignKey('mapRegions', notNull=True, cascade=True)
    toRegion = ForeignKey('mapRegions', notNull=True, cascade=True)
    unique = index.DatabaseIndex('fromRegion', 'toRegion',
                                 unique=True)


class chrFactions(SQLObject):
    class sqlmeta:
        idName = 'factionID'
        style = MixedCaseStyle()
        fromDatabase = True
    factionName = StringCol()
    description = StringCol()
    solarSystem = ForeignKey('mapSolarSystems')
    corporation = ForeignKey('crpNPCCorporations')
    militiaCorporation = ForeignKey('crpNPCCorporations')
    corporations = MultipleJoin('crpNPCCorporations')
    solarSystems = MultipleJoin('mapSolarSystems')
    constellations = MultipleJoin('mapConstellations')
    regions = MultipleJoin('mapRegions')
    #TODO: agents, stations


class staStations(SQLObject):
    class sqlmeta:
        idName = 'stationID'
        style = MixedCaseStyle()
        fromDatabase = True
    security = IntCol()
    stationType = ForeignKey('staStationTypes')
    operation = ForeignKey('staOperations')
    corporation = ForeignKey('chrNPCCorporations')
    solarSystem = ForeignKey('mapSolarSystems')
    constellation = ForeignKey('mapConstellations')
    region = ForeignKey('mapRegions')
    stationName = StringCol()
    agents = MultipleJoin('agtAgents')


class staOperations(SQLObject):
    class sqlmeta:
        idName = 'operationID'
        style = MixedCaseStyle()
        fromDatabase = True
    operationName = StringCol()
    description = StringCol()
    services = RelatedJoin('staServices',
                           intermediateTable='staOperationServices',
                           createRelatedTable=False, joinColumn='operationID',
                          otherColumn='serviceID')

class staServices(SQLObject):
    class sqlmeta:
        idName = 'serviceID'
        style = MixedCaseStyle()
    serviceName = StringCol()
    description = StringCol()
    operations = RelatedJoin('staOperations',
                           intermediateTable='staOperationServices',
                           createRelatedTable=False, otherColumn='operationID',
                          joinColumn='serviceID')



class staStationTypes(SQLObject):
    class sqlmeta:
        idName = 'stationTypeID'
        style = MixedCaseStyle()
        fromDatabase = True
    operation = ForeignKey('staOperations')
    conquerable = BoolCol()
