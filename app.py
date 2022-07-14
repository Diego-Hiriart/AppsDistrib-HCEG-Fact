import json
from flask import Flask, request, json, Response
from hcegInvoiceClasses import *

app = Flask(__name__)#Get currentt module name (what is running now)

@app.route('/api/invoice', methods=['POST'])
def createPost():
    content_type = request.headers.get('Content-Type')
    if(content_type == 'application/json'):
        jsonReq = request.json
        invRequest = InvoiceRequest(int(jsonReq["customerId"]), list(jsonReq["products"]), int(jsonReq["paymentMethodId"]))
        print(invRequest.products)
        #invoice = Invoice(jsonInv["invoiceId"], jsonInv["customerId"], jsonInv["orderId"], jsonInv["subtotal"], jsonInv["tax"], jsonInv["total"], jsonInv["paymentMethodId"])
        return Response(status=200, content_type=('application/json'), response=json.dumps(invRequest.__dict__))
    else:
        return Response('Content-Type not supported', status=415)


if __name__ == '__main__':
    app.run()