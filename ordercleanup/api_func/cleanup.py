from flask import session, request
from ordercleanup import db
from ordercleanup.models import( 
    Orders, 
    OrderDrivers, 
    OrderChangeLog, 
    OrderScans,
    OrderPackageItems,
    OrderShipmentStatusCodes)


from sqlalchemy import Date
from ordercleanup.config import config
from datetime import datetime


# #config variables 
# config = config['development']
threshold =  config.THRESHOLD
status = config.STATUS
route_id = config.ROUTE_ID
driver_id = config.DRIVER_ID
archive_level = config.ARCHIVE_LEVEL
is_default_driver =config.IS_DEFAULT_DRIVER
pickup = config.PICKUP
delivery = config.DELIVERY
user_id = config.USER_ID
employee_id = config.EMPLOYEE_ID
shipment_status_code_id = config.SHIPMENT_STATUS_CODE_ID
user_category = config.USER_CATEGORY
change_details = config.CHANGE_DETAILS
service_list = config.SERVICE_LIST


#shared variables 
total_order_driver = []
total_new_orders_to_driver = []
total_order_routes =[]
total_orders_shipment_status_codes = []
total_change_logs = []


def get_orderscans():
    order_scans = db.session.query(OrderScans.OrderTrackingID)
    return order_scans.all()

def get_master_list():
    master_order_list = []
    try:
        dbquery = db.session.query(Orders.OrderTrackingID, OrderPackageItems.PackageItemID)
        dbquery = dbquery.join(OrderPackageItems, Orders.OrderTrackingID == OrderPackageItems.OrderTrackingID)
        dbquery = dbquery.filter(
            Orders.PickupTargetFrom.cast(Date) <= threshold,
            Orders.ServiceID.in_(service_list), 
            Orders.Status == status,
            ~Orders.OrderTrackingID.in_(get_orderscans()), 
        )

        res = [r._asdict() for r in dbquery.all()]
        done = set()

        for d in res:
            if d['OrderTrackingID'] not in done:
                done.add(d['OrderTrackingID'])  # to avoid duplicated orders
                master_order_list.append(d)
    except Exception as e: 
        print(e)
    return master_order_list


def add_orders_to_route():
    try:
        master_list = get_master_list()
        if len(master_list) > 0:
        
            for order in master_list: 
                dbquery = db.session.query(Orders.RouteID, Orders.OrderTrackingID).filter(Orders.OrderTrackingID == order['OrderTrackingID'])
                if dbquery is not None:
                    dbquery = dbquery.update({'RouteID': route_id}, synchronize_session=False)
                    total_order_routes.append(order['OrderTrackingID'])
            db.session.commit()
        print('ORDERS TO ROUTE: ', len(total_order_routes))
    except Exception as e: 
        print(e)
    return total_order_routes


def update_driver_id():
    try:
        master_list = get_master_list()
        if len(master_list) > 0:
            new_order_drivers = []
            for order in master_list: 
                dbquery = db.session.query(OrderDrivers.DriverID,).filter(OrderDrivers.OrderTrackingID == order['OrderTrackingID'])
                if len(dbquery.all()) > 0: 
                    dbquery = db.session.query(OrderDrivers.DriverID).filter(OrderDrivers.OrderTrackingID == order['OrderTrackingID'])
                    dbquery = dbquery.update({'DriverID': driver_id}, synchronize_session=False)
                    total_order_driver.append(order['OrderTrackingID'])
                else: 
                    """ If order not assigned, assign to driver """
                    new_order = {}
                    new_order['OrderTrackingID'] = order['OrderTrackingID']
                    new_order['ArchiveLevel'] = archive_level 
                    new_order['DriverID'] = driver_id
                    new_order['Status'] = status
                    new_order['isDefaultDriver'] = is_default_driver
                    new_order['Pickup'] = pickup 
                    new_order['Delivery'] = delivery
                    new_order['UserID'] = user_id
                    new_order_drivers.append(new_order)
                    total_new_orders_to_driver.append(order['OrderTrackingID'])
            if len(new_order_drivers) > 0:
                db.session.bulk_insert_mappings(OrderDrivers, new_order_drivers)
            db.session.commit()
            print('NEW DRIVER: ',len(total_new_orders_to_driver))
            print('UPDATED DRIVER: ', len(total_order_driver))
    except Exception as e: 
        print(e)
    return total_order_driver, total_new_orders_to_driver


def add_status_code_and_change_log():
    try:
        master_list = get_master_list()
        for code in master_list: 
            dbfil = db.session.query(OrderShipmentStatusCodes.OrderTrackingID)
            dbfil = dbfil.filter(OrderShipmentStatusCodes.OrderTrackingID == code['OrderTrackingID'])
            if dbfil.first() is None:
                isInline = True
                new_order_shipment = OrderShipmentStatusCodes()
                setattr(new_order_shipment, 'OrderTrackingID', code['OrderTrackingID'])
                setattr(new_order_shipment, 'PackageItemID', code['PackageItemID'])
                setattr(new_order_shipment, 'ShipmentStatusCodeID', shipment_status_code_id)
                setattr(new_order_shipment, 'EmployeeID', employee_id)
                setattr(new_order_shipment, 'aTimeStamp', datetime.now())
                setattr(new_order_shipment, 'Status','A')
                total_orders_shipment_status_codes.append(code['OrderTrackingID'])
                db.session.add(new_order_shipment)

                new_order = OrderChangeLog()
                setattr(new_order, 'OrderTrackingID', code['OrderTrackingID'])
                setattr(new_order, 'userCategory', user_category)
                setattr(new_order, 'EmployeeID', employee_id)
                setattr(new_order, 'changeCode', 0)
                setattr(new_order, 'FieldName', '')
                setattr(new_order, 'aTimeStamp', datetime.now())
                setattr(new_order, 'ChangeDetails', change_details)
                db.session.add(new_order)
                total_change_logs.append(code['OrderTrackingID'])
        db.session.commit()
        print('SHIPMENT STATUS CODES: ', len(total_orders_shipment_status_codes))
    except Exception as e: 
        print(e)
    return total_orders_shipment_status_codes, total_change_logs

