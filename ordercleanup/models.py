from ordercleanup import db


class Orders(db.Model):
    __tablename__ = "Orders"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    PickupTargetFrom = db.Column(db.DateTime)
    Status = db.Column(db.String(1))
    ServiceID = db.Column(db.Integer)
    RouteID = db.Column(db.Integer, nullable=False)
    

class OrderScans(db.Model):
    __tablename__ = "OrderScans"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
 

class OrderPackageItems(db.Model):
    __tablename__ = "OrderPackageItems"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    PackageItemID = db.Column(db.Integer)

class OrderDrivers(db.Model):
    __tablename__ = "OrderDrivers"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    ArchiveLevel = db.Column(db.Integer, primary_key=True)
    DriverID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(1))
    isDefaultDriver = db.Column(db.Integer)
    Pickup = db.Column(db.Integer)
    Delivery = db.Column(db.Integer)
    UserID = db.Column(db.Integer)

   
    def to_json(self):
        return {
            'OrderTrackingID': self.OrderTrackingID,
            'ArchiveLevel': self.ArchiveLevel,
            'DriverID': self.DriverID,
            'Status':self.Status,
            'isDefaultDriver':self.isDefaultDriver,
            'Pickup':self.Pickup,
            'Delivery':self.Delivery,
            'UserID':self.UserID
        }

class OrderChangeLog(db.Model):
    __tablename__ = "OrderChangeLog"
    OrderChangeLogID = db.Column(db.Integer, primary_key=True)
    OrderTrackingID = db.Column(db.DECIMAL)
    EmployeeID = db.Column(db.Integer)
    userCategory = db.Column(db.Integer)
    changeCode = db.Column(db.Integer)
    aTimeStamp = db.Column(db.DateTime, nullable=False)
    FieldName = db.Column(db.String(50))
    ChangeDetails = db.Column(db.String(700))

class OrderShipmentStatusCodes(db.Model):
    __tablename__ = "OrderShipmentStatusCodes"
    __table_args__ = {'implicit_returning':False}
    
    ID = db.Column(db.Integer, primary_key=True)
    OrderTrackingID = db.Column(db.DECIMAL)
    PackageItemID = db.Column(db.Integer)
    ShipmentStatusCodeID = db.Column(db.Integer)
    EmployeeID = db.Column(db.Integer)
    aTimeStamp = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.String(1), nullable=False)