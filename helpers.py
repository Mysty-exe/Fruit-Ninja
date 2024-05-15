from decimal import Decimal

def add_decimal(numToAdd, num):
    after_comma = Decimal(num).as_tuple()[-1]*-1
    add = Decimal(numToAdd) / Decimal(10**after_comma)
    return Decimal(num) + add
    
def sub_decimal(numToSub, num):
    after_comma = Decimal(num).as_tuple()[-1]*-1
    sub = Decimal(numToSub) / Decimal(10**after_comma)
    return Decimal(num) - sub
