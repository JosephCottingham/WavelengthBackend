from Teebox_Api import app, db
from stripe import stripe

stripe = app.config['STRIPE_SECRET_KEY']

@staticmethod
def make_payment(user, price, payment_meathod):