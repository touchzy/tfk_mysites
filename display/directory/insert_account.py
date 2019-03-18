import json

user = {'id': '8798yfidhisa90v', 'username': 'user', 'password': '1235'}
with open('account.txt', 'a', encoding='utf-8') as account:
    account.write(json.dumps(user))