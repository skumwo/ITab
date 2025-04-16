class CardPaymentHandler:
    def process(self, payment):
        print(f"[💳] Card payment for ${payment.amount}")

class PayPalPaymentHandler:
    def process(self, payment):
        print(f"[🅿️] PayPal payment for ${payment.amount}")

class CryptoPaymentHandler:
    def process(self, payment):
        print(f"[₿] Crypto payment for ${payment.amount}")

def payment_handler_factory(payment_type):
    if payment_type == 'card':
        return CardPaymentHandler()
    elif payment_type == 'paypal':
        return PayPalPaymentHandler()
    elif payment_type == 'crypto':
        return CryptoPaymentHandler()
    raise ValueError(f"Unknown payment type: {payment_type}")
