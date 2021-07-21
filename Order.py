from abc import ABC, abstractmethod

# S: Single responsibility, a class should handle one thing and One thing only 
# O: Open-closed, Once a class has been made, it should be open to inherit, but not to alter
# L: Liskov substitution principle, Inherited classes should not have to hack or break the superclass just to work
# I: Interface Segregation, Make Interfaces specific to the jobs required, create extra abstract classes when needed
# D: Dependency Inversion, Classes should depend on abstract classes, this allows to create different interfaces from a superclass instead of 
#    individual, seperate interfaces 

# The stages of change
# All classes below started as a single order class with the add_order, total_price and payment methods, this was then seperated into a seperate payment class
# from here the payment was now seperated into a superclass with different payment types represented as child classes,
# The authorization method was altered to remove the neccessity of having multiple abstract methods that not all classes implement directly by creating a authorizor class used through composition
# The SMSAuth interface was then created as a more specific interface definition, that could handle the authorization seperate to the payment
# The Authorizor interface wasd then created for more than one authorization type not_a_robot and SMS_auth and the potential for further authorizations to inherit from it.

class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class Authorizor(ABC):
    @abstractmethod
    def is_authorized(self)-> bool:
        pass

class SMSAuth(Authorizor):

    authorized = False

    def verify_code(self, code):
        print(f"Verifying code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class NotARobot(Authorizor):

    authorized = False

    def not_a_robot(self):
        print("You are not a robot")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizor: Authorizor):
        self.security_code = security_code
        self.authorizor = authorizor

    def auth_sms(self, code):
        print(f"Verifying SMS code: {code}")
        self.verified = True

    def pay(self, order):
        if not self.authorizor.is_authorized():
            raise Exception("Not Authorised") 
        print("Processing debit payment")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address, authorizor: Authorizor):
        self.authorizor = authorizor
        self.email_address = email_address

    def pay(self, order):
        if not self.authorizor.is_authorized():
            raise Exception("Not Authorised") 
        print("Processing paypal payment")
        print(f"Verifying email: {self.email_address}")
        order.status = "paid"
    

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 10)

print(order.total_price())

authorizor = NotARobot()

paypal = PaypalPaymentProcessor("test@email.com", authorizor)
authorizor.not_a_robot()

paypal.pay(order)