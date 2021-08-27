from flask import Flask, jsonify, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import os
import mysql_util
import pandas as pd

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
CORS(app)

@app.route('/')
def home():
    df = pd.read_excel('table_example.xlsx')
     # 이 윗 부분이 나중에 대체됨
    df_yard = df[df['LOCATION'] == 'yard']
    df_6wharf = df[df['LOCATION'] == '6wharf']

    data = []
    list_ = []

    df_ = df_yard
    if len(df_)%2 == 0:
        list_.append(int(len(df_)/2))
        list_.append(int(len(df_)/2))

    else:
        list_.append(int(len(df_)//2 + 1))
        list_.append(int(len(df_)//2))

    for i in range(len(df_)):
        list_.append([df_.iloc[i]['MODEL'], df_.iloc[i]['COUNT']])
    data.append(list_)

    list_ = []
    df_ = df_6wharf
    if len(df_)%2 == 0:
        list_.append(int(len(df_)/2))
        list_.append(int(len(df_)/2))

    else:
        list_.append(int(len(df_)//2 + 1))
        list_.append(int(len(df_)//2))

    for i in range(len(df_)):
        list_.append([df_.iloc[i]['MODEL'], df_.iloc[i]['COUNT']])
    data.append(list_)
    data.append(df.MODEL.unique().tolist())
    return render_template('home.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
