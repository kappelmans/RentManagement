from google.appengine.ext import ndb
 
class Address(ndb.Model):
    street = ndb.StringProperty()
    postalCode = ndb.StringProperty()
    locality = ndb.StringProperty()
    def __str__( self ):
        return self.street + ', ' + self.postalCode + ' ' + self.locality

class Property(ndb.Model):
    shortName = ndb.StringProperty()
    propertyType = ndb.IntegerProperty()
    address = ndb.Referencendb.KeyProperty(kind=Address)
    ki = ndb.FloatProperty()
    propertyOwner = ndb.IntegerProperty()
    def __str__( self ):
        return self.shortName

    @staticmethod
    def getProperty(property_url_key = None, property_key = None):
        if not property_key is None:
            return property_key.get()
        elif not property_url_key is None:
            property_key = ndb.Key(urlsafe=property_url_key)
            return property_key.get()
        else:
            return None
    
class Person(ndb.Model):
    name = ndb.StringProperty()
    language = ndb.StringProperty()
    aanspreekTittel = ndb.StringProperty()
    phone = ndb.PhoneNumberProperty()
    email = ndb.EmailProperty()
    address = ndb.Referencendb.KeyProperty(kind=Address)
        
class Contract(ndb.Model):
    tenant = ndb.Referencendb.KeyProperty(kind=Person)
    property = ndb.Referencendb.KeyProperty(kind=Property)
    useTenantAddress = ndb.BooleanProperty();
    contractDate = ndb.DateTimeProperty()
    startDate = ndb.DateTimeProperty()
    endDate = ndb.DateTimeProperty()
    baseIndex = ndb.FloatProperty()
    baseIndexType = ndb.IntegerProperty()
    baseRent = ndb.FloatProperty()
    currentRent = ndb.FloatProperty()
    provision = ndb.FloatProperty()
    tenantGaranty = ndb.FloatProperty()
    indexMonth = ndb.IntegerProperty()  

    @staticmethod
    def getContract(contract_url_key = None, contract_key = None):
        if not contract_key is None:
            return contract_key.get()
        elif not contract_url_key is None:
            contract_key = ndb.Key(urlsafe=contract_url_key)
            return contract_key.get()
        else:
            return None
      
    def delete(self):
        _contract_delete(self)

def _contract_delete(self):
    tenant = self.tenant
    db.Model.delete(self)
    Person.delete(tenant)
    
    
    
    
    
    
class User(ndb.Model):
    email = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    status = ndb.IntegerProperty()
    
    @staticmethod
    def getUser(email=None, user_url_key = None):
        if not user_url_key is None:
            user_key = ndb.Key(urlsafe=user_url_key)
            return user_key.get()
        else:
            user_key = ndb.Key("User", email)
            user = user_key.get()
            if user is None:
                user = User(parent = user_key, email=email, status=0)
                user.gatewayList = {'gateway_url_keys':[]}
                user.key = user_key
                user.put()
            return user
        
class Location(ndb.Model):
    geolocation = ndb.GeoPtProperty()
    geolocation_proximity = ndb.StringProperty()
    description = ndb.StringProperty()
    
    @staticmethod
    def getLocation(geolocation_proximity = None, description=None, geolocation=None, location_url_key = None):
        if not location_url_key is None:
            location_key = ndb.Key(urlsafe=location_url_key)
            return location_key.get()
        else:
            location_key = ndb.Key("Location", geolocation_proximity)
            location = location_key.get()
            if location is None:
                location = Location(geolocation_proximity = geolocation_proximity, geolocation=geolocation, description=description)
                location.key = location_key
                location.put()
            return location

class Container(ndb.Model):
    container_id = ndb.StringProperty()
    exact_location = ndb.GeoPtProperty()
    current_location = ndb.KeyProperty(kind=Location) 
    description = ndb.StringProperty()
    status = ndb.IntegerProperty()

    @staticmethod
    def getContainer(container_id = None, container_url_key = None, container_key = None):
        if not container_key is None:
            return container_key.get()
        elif not container_url_key is None:
            container_key = ndb.Key(urlsafe=container_url_key)
            return container_key.get()
        else:
            container_key = ndb.Key("Container", container_id)
            container = container_key.get()
            if container is None:
                container = Container(parent = container_key, container_id=container_id)
                container.key = container_key
                container.status = -1
                container.put()
            return container

class LockerType(ndb.Model):
    type = ndb.StringProperty()
    description = ndb.StringProperty()
   
    @staticmethod
    def getAllLockerTypes():
        allTypes = LockerType.query().fetch()
        if len(allTypes) == 0:
            LockerType(type='Type A').put()
            LockerType(type='Type B').put()
            LockerType(type='Type C').put()
            allTypes = LockerType.query().fetch()
        result=[]
        for locker in allTypes:
            result.append({'locker_type':locker.type, 'locker_url_key':locker.key.urlsafe(), 'locker_description':locker.description})
        return result
    
    @staticmethod
    def getLockerType(lockertype_url_key = None, lockertype_key = None):
        if not lockertype_key is None:
            return lockertype_key.get()
        elif not lockertype_url_key is None:
            lockertype_key = ndb.Key(urlsafe=lockertype_url_key)
            return lockertype_key.get()
    