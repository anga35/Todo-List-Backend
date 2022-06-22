# from urllib import response
from urllib import response
import requests
# from django.conf import settings
# import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
# from pathlib import Path
# mPath=Path(__file__).resolve()

# endpoint='http://127.0.0.1:8000/user/profile-pic/'

'''
token_endpoint='http://127.0.0.1:8000/user/get-token/'
response=requests.post(token_endpoint,data={'email':'dayodele89@gmail.com','password':'heso123yam'})
token=response.json()['token']

'''


# pic=open('C:/Dev/Django_Projects/todo_project/temp.jpg','rb')
# upload={'profile_pic':pic}
# response=requests.post(endpoint,files=upload,headers={'Authorization':f'Token {token}'})
# print(response.json())


response=requests.post("https://datobi-todolist-app.herokuapp.com/user/reset-password-email/",data={'email':'dayodele289@gmail.com'})
print(response)