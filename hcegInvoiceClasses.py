class InvoiceRequest:
    def __init__(self, customerId, products, paymentMehtodId):
        self.customerId = customerId
        self.products = products
        self.paymentMehtodId = paymentMehtodId

class Invoice:
    def __init__(self, invoiceId, customerId, orderId, subtotal, tax, total, paymentMethodId):
        self.invoiceId = invoiceId
        self.customerId = customerId
        self.orderId = orderId
        self.subtotal = subtotal
        self.tax = tax
        self.total = total
        self.paymentMethodId = paymentMethodId

class Product:
    def __init__(self, productId, name, price):
        self.productId = productId
        self.name = name
        self.price = price

class Order:
    def __init__(self, orderId, date):
        self.orderId = orderId
        self.date = date

class OrderItem:
    def __init__(self, orderId, productId):
        self.orderId = orderId
        self.productId = productId

