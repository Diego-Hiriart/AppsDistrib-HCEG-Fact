from flask import Flask, request, json, jsonify, Response
from flask_cors import CORS
from hcegInvoiceClasses import *
from datetime import datetime
import requests

app = Flask(__name__)#Get currentt module name (what is running now)
CORS(app, resources={r"/api/invoice": {"origins": ["http://localhost:3001", "https://hceg-gui.azurewebsites.net", "127.0.0.1"]}})

iva = 0.12

@app.route('/api/invoice', methods=['POST'])
def createPost():
    try:
        content_type = request.headers.get('Content-Type')
        if(content_type == 'application/json'):
            jsonReq = request.json # Get the request's content
            invRequest = InvoiceRequest(int(jsonReq["customerId"]), list(jsonReq["products"]), int(jsonReq["paymentMethodId"]))
            if len(invRequest.products) == 0:#Check if products were sent
                return Response("Products list cannot be empty", status=400)
            order = Order(0, datetime.now())
            orderPostReq = requests.post("https://hceg-dbapi.azurewebsites.net/api/orders", data=jsonify(order.serialize()).data, headers={'Content-type': 'application/json'})#Send order to be created
            #If order creation was successful, now read the latest order and send an invoice to be created
            if(orderPostReq.status_code == 200):
                latestOrderReq = requests.get("https://hceg-dbapi.azurewebsites.net/api/orders/latest")
                latestOrder = latestOrderReq.json()
                #Generate Order items
                itemsPostSuccess = True
                for product in list(jsonReq["products"]):
                    orderItem = OrderItem(latestOrder["orderId"], product)
                    orderItemPostReq = requests.post("https://hceg-dbapi.azurewebsites.net/api/order-items", data=jsonify(orderItem.serialize()).data, headers={'Content-type': 'application/json'})
                    if orderItemPostReq.status_code != 200:
                        itemsPostSuccess = False
                #Get each of the product's price to caculate subtotal, tax, and total
                if itemsPostSuccess:
                    subtotal = 0
                    for pId in list(jsonReq["products"]):
                        productReq = requests.get("https://hceg-dbapi.azurewebsites.net/api/products/search?id={0}".format(pId))
                        subtotal += productReq.json()["price"]
                    tax = subtotal*iva
                    total = subtotal+tax
                    #Create an invoice object and send it to the DB API
                    invoice = Invoice(0, invRequest.customerId, latestOrder["orderId"], subtotal, tax, total, invRequest.paymentMehtodId)
                    invPostRequest = requests.post("https://hceg-dbapi.azurewebsites.net/api/invoices", data=jsonify(invoice.serialize()).data, headers={'Content-type': 'application/json'})
                    if invPostRequest.status_code == 200:
                        return Response(status=200, content_type='application/json', response=str(invPostRequest.json()))
                    else:
                        return Response("Invoice could not be created {0}".format(str(invPostRequest.content)), status=500)
            else:
                return Response("Order could not be created {0}".format(str(orderPostReq.content)), status=500,)
        else:
            return Response('Content-Type not supported', status=415)
    except Exception as excp:
        return Response(str(excp), status=500)

if __name__ == '__main__':
    app.run()