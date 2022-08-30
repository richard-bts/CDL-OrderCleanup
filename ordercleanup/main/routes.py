from flask import render_template, request, Blueprint
from datetime import date, datetime
from sqlalchemy import Date
from ordercleanup.api_func.cleanup import (
    add_orders_to_route,
    add_status_code_and_change_log, 
    update_driver_id, 
    get_test_scans,
    get_master_list
)
from ordercleanup import mail
from ordercleanup.config import config
from flask_mail import Message

import xlsxwriter
import os

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/report", methods=["GET", "POST"])
def get_report():
    total_order_routes = add_orders_to_route()
    total_order_driver, total_new_orders_to_driver = update_driver_id()
    total_orders_shipment_status_codes, total_change_logs = add_status_code_and_change_log()
    today = date.today()
    today = today.strftime("%m_%d_%y")
    file_name = 'Cleanup_Report-' + today + '.xlsx'
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0
    worksheet.write(row, col,'Order Routes TrackingID')

    # Iterate over the data and write it out row by row.
    for order in total_order_routes:
        worksheet.write(row+1, col, order)
        row += 1
    
    row = 0
    col = 1
    worksheet.write(row, col,'Updated Driver ID')
    for order in total_order_driver:
        worksheet.write(row+1, col, order)
        row += 1

    row = 0
    col = 2
    worksheet.write(row, col,'New Order Driver ID')
    for order in total_new_orders_to_driver:
        worksheet.write(row+1, col, order)
        row += 1

    row = 0
    col = 3
    worksheet.write(row, col,'Shipment Status Code')
    for order in total_orders_shipment_status_codes:
        worksheet.write(row+1, col, order)
        row += 1

    row = 0
    col = 4
    worksheet.write(row, col,'Change Logs')
    for order in total_change_logs:
        worksheet.write(row+1, col, order)
        row += 1

    workbook.close()

    subject = 'Order Cleanup Report - ' + today
    msg = Message(
                    sender=str(config.MAIL_DEFAULT_SENDER),
                    subject=subject,
                    recipients = config.RECIPIENTS
                )
    msg.body = 'Find attached the order cleanup report in the email'
    file = open(file_name, 'rb')

    
    msg.attach(file_name, '	application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', file.read())
    mail.send(msg)

    return render_template('success.html')


@main.route("/test")
def test_route():
    return {'TestEnv':config.TESTING, 'Scans': get_test_scans()}

