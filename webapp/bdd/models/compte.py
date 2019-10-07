# coding: utf-8
from datetime import date
from enum import Enum


# Compte courant sans autorisation de découvert
class typeAccount(Enum):
    CURRENT_ACCOUNT = "Compte Courant"
    DEBIT_ACCOUNT = "Comte Autorisation de découvert"
    PAID_ACCOUNT = "Compte Rémunéré"


class Compte:
    __account_threshold = 0.0

    def __init__(self, p_num=None,
                 p_account_type=typeAccount.CURRENT_ACCOUNT,
                 p_creation_date=date.today(),
                 p_iban=None,
                 p_balance=0.0):
        self.__account_number = p_num
        self.__account_type = p_account_type
        self.__creation_date = p_creation_date
        self.__iban = p_iban
        self.__balance = p_balance
        print(f"SUCCESS : Creation du compte {self.__account_number}")

    # Getters
    def get_account_number(self):
        return self.__account_number

    def get_account_type(self):
        return self.__account_type

    def get_creation_date(self):
        return self.__creation_date

    def get_iban(self):
        return self.__iban

    def get_balance(self):
        return self.__balance

    # Setters
    def set_account_number(self, p_num):
        self.__account_number = p_num

    def set_account_type(self, p_account_type):
        if isinstance(p_account_type, typeAccount):
            self.__account_type = p_account_type

    def set_creation_date(self, p_creation_date):
        self.__creation_date = p_creation_date

    def set_iban(self, p_iban):
        self.__iban = p_iban

    def set_balance(self, p_balance):
        try:
            if float(p_balance) >= 0.0:
                self.__balance = float(p_balance)
                # print(f"SUCCESS : Mise à jour du solde du compte {self.__account_number}")
                return self.__balance
            else:
                raise NegativeBalanceException(
                    "FAILED : entrez un montant positif".format(self.get_account_number()))
        except ValueError as e:
            print(e)

    # Methods
    def credit(self, p_count):
        self.set_balance(self.get_balance() + float(p_count))
        return self.get_balance()

    def debit(self, p_count):
        try:
            new_balance = self.get_balance() - float(p_count)
            if new_balance >= 0.0:
                return self.set_balance(new_balance)
            else:
                raise NegativeBalanceException(
                    "FAILED : le solde du compte {} est négatif.".format(self.get_account_number()))
        except ValueError as e:
            print(e)

    def __add__(self, p_count):
        return self.credit(p_count)

    def __sub__(self, p_count):
        return self.debit(p_count)

    def __eq__(self, other):
        return (self.get_account_number() == other.get_account_number()) and (
                    self.get_account_type() == other.get_account_number)

    def __str__(self):
        if self.get_balance() >= 0.0:
            return "Account[{}:{}:{:+.2f}]".format(self.get_account_number(),
                                                   self.get_account_type().value,
                                                   self.get_balance())
        else:
            return "Account[{}:{}:{:-.2f}]".format(self.get_account_number(),
                                                   self.get_account_type().value,
                                                   self.get_balance())


class CompteRemunere(Compte):
    __paid_rate = 18.00
    __bank_threshold = 1000.00

    def __init__(self, p_num=None,
                 p_account_type=typeAccount.PAID_ACCOUNT,
                 p_creation_date=date.today(),
                 p_iban=None,
                 p_balance=0.0):
        super().__init__(p_num, p_account_type, p_creation_date, p_iban, p_balance)
        self.__benefit = 0.0

    # Getters
    def get_benefit(self):
        return self.__benefit

    def get_paid_rate(cls):
        return __class__.__paid_rate

    def get_bank_threshold(cls):
        return __class__.__bank_threshold

    # Setters
    def set_benefit(self, p_benefit):
        self.__benefit = p_benefit

    def set_paid_rate(cls, p_paid_rate):
        __class__.__paid_rate = p_paid_rate

    def set_bank_threshold(cls, p_bank_threshold):
        __class__.__bank_threshold = p_bank_threshold


class CompteDecouvert(Compte):
    __agios_rate = 0.18

    def __init__(self, p_num=None,
                 p_account_type=typeAccount.DEBIT_ACCOUNT,
                 p_creation_date=date.today(),
                 p_iban=None,
                 p_balance=0.0,
                 p_cash_facility=False,
                 p_agios=dict()):
        super().__init__(p_num, p_account_type, p_creation_date, p_iban, p_balance)
        self.__cashier_facility = p_cash_facility
        self.__agios = p_agios

    # Getters
    def get_cashier_facility(self):
        return self.__cashier_facility

    def get_agios(self):
        return self.__agios

    def get_agios_rate(cls):
        return __class__.__agios_rate

    def get_bank_threshold(cls):
        return __class__.__bank_threshold

    # Setters
    def set_cashier_facility(self, p_cashier_facility):
        self.__cashier_facility = p_cashier_facility

    def set_agios(self, p_agios):
        self.__agios = p_agios

    def set_agios_rate(cls, p_agios_rate):
        __class__.__agios_rate = p_agios_rate

    # Methods
    def debit(self, p_count):
        try:

            new_balance = (self.get_balance() + self.get_cashier_facility()) - float(p_count)
            if new_balance >= 0.0:
                return self.set_balance(new_balance - self.get_cashier_facility())
            else:
                raise NegativeBalanceException(
                    "FAILED : le solde du compte {} est négatif.".format(self.get_account_number()))
        except ValueError as e:
            print(e)


class NegativeBalanceException(Exception):
    def __init__(self, p_message):
        self.__message = p_message


if __name__ == "__main__":
    
    print(f"La date du jour : {date.today()}")

    try:
        # Account
        ca1 = Compte()
        ca1.set_account_number("MELOU971")
        print(f"SUCCESS : Mise a jour du numero de compte {ca1.get_account_number()}")
        print("SUCCESS : " + str(ca1))
        print("SUCCESS : Réinitialisation du solde du compte {}: {:+.2f}".format(ca1.get_account_number(), ca1.set_balance(1000)))
        print("SUCCESS : Opération de CREDIT du compte {}: {:+.2f}".format(ca1.get_account_number(), ca1.credit("200")))
        debit = 50.53
        print("SUCCESS : Opération de DEBIT du compte {} de -{}: {:+.2f}".format(ca1.get_account_number(), debit, ca1.debit(debit)))
        ca1.set_balance("5100")
        print("SUCCESS : Réinitialisation du solde du compte \n{}".format(ca1))
        print("SUCCESS : Opération CREDIT(+253.20) du compte {}: {:+.2f}".format(ca1.get_account_number(), ca1 + 253.2))
        print("SUCCESS : Opération DEBIT(-1000) et CREDIT(+100) du compte {}: {:+.2f}".format(
            ca1.get_account_number(), ca1 -1000 + 100))

        print("SUCCESS : le compte {} a été vidé : {:+.2f}".format(ca1.get_account_number(), ca1 - ca1.get_balance()))
        print("SUCCESS : j'essaie encore de retirer : {:+.2f}".format(ca1-50))
        print("SUCCESS : " + str(ca1))

    except NegativeBalanceException as nbe:
        pass
