import re
currency_list = ['usd','aud','euro','eur']
def is_amount(text):
#    if ' ' in text:
#        [currency,amt] = text.split(' ')
#        re_amount = r'^\S?\S?\S?\$?\d*[.,-,(]?\s?\d*[.,-,)]?\d*[.]?$'
#        return currency.lower() in currency_list and bool(re.match(re_amount, amt)) and bool(re.match( r'.*[0-9].*',amt))
#    else:
        re_amount = r'^\S?\S?\S?\$?\d*[.,-,(]?\s?\d*[.,-,)]?\d*[.]?$'
        return bool(re.match(re_amount, text)) and bool(re.match( r'.*[0-9].*',text))
#    re_amount = r'^\d*[.,]?\d*$'

#    re_amount = r'^\S?\$?\d*[.,-]?\d*[.]?\d*[.]?$'

    
    
    
    
if __name__ == "__main__":
    text = "(102)"
    res = is_amount(text)
    print(res)