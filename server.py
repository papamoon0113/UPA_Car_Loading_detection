from flask import Flask, jsonify, request, render_template, make_response, redirect
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import os
import mysql_util
import pandas as pd
import datetime
import info_mgmt, history_mgmt, count_mgmt
import update_xlsx

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
CORS(app)

def timestamp_to_data(timestamp):
    _date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%y/%m/%d')
    return _date

@app.route('/')
def home():
    _count = count_mgmt.Count()
    df = _count.get_all()
    # df = pd.read_excel('table_example.xlsx')
     # 이 윗 부분이 나중에 대체됨
    df_yard = df[df['LOCATION'] == 'YARD']
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

@app.route('/modal/<location>/<model>', methods=['GET'])
def modal(location, model):
    _count = count_mgmt.Count()
    _history = history_mgmt.History()
    history_df = _history.find_model_log(model)
    print(history_df)
    # print(history_df)
    # current_df = pd.read_excel('table_example.xlsx')
    # history_df = pd.read_excel('history.xlsx')
    # 위의 df 수정하면 됨
    # 오류 뜨면 아마 history_df에 날짜가 날짜가 아니라 문자열일 때
    
    tmp = min(len(history_df), 15)
    history_df = history_df.iloc[-tmp:]
    # print(current_df)
    # print(history_df)
    del history_df['MODEL']

    # history_df.columns = ['MOVING_TIME', 'LOCATION', 'PM', 'M_FROM', 'M_TO', 'COUNT', 'RESULT']
    
    yard_count = _count.get_count(model, 'YARD')
    wharf_count = _count.get_count(model, '6wharf')

    # yard_count = current_df[(current_df.MODEL == model) & (current_df.LOCATION == 'YARD')]['COUNT'].iat[0]
    # wharf_count = current_df[(current_df.MODEL == model) & (current_df.LOCATION == '6wharf')]['COUNT'].iat[0]

    result_df = pd.DataFrame(columns=['MOVING_TIME', 'LOCATION', 'PM', 'MOVING', 'BEFORE', 'COUNT', 'RESULT'])
    translate = {'YARD':'야적지', '6wharf':'6부두', 'abroad':'해외', 'factory':'공장'}
    # result_df에 표에 출력해야 하는 
    for i in range(len(history_df)):
        count = history_df.iloc[i]['COUNT']
        tmp1 = []
        tmp2 = []
        if history_df.iloc[i]['M_FROM'] == 'YARD':
            _time = f"{history_df.iloc[i]['MOVING_TIME'].year}. {history_df.iloc[i]['MOVING_TIME'].month}. {history_df.iloc[i]['MOVING_TIME'].day}"
            tmp1.append(_time)
            tmp1.append('YARD')
            tmp1.append('-')
            tmp1.append(f"{translate[history_df.iloc[i]['M_TO']]}으로 나감")
            tmp1.append(f'{yard_count + count}')
            tmp1.append(f'-{count}')
            tmp1.append(yard_count)
            yard_count = yard_count + count
            
        if history_df.iloc[i]['M_FROM'] == '6wharf':
            _time = f"{history_df.iloc[i]['MOVING_TIME'].year}. {history_df.iloc[i]['MOVING_TIME'].month}. {history_df.iloc[i]['MOVING_TIME'].day}"
            tmp2.append(_time)
            tmp2.append('6wharf')
            tmp2.append('-')
            tmp2.append(f"{translate[history_df.iloc[i]['M_TO']]}으로 나감")
            tmp2.append(f'{wharf_count + count}')
            tmp2.append(f'-{count}')
            tmp2.append(wharf_count)
            wharf_count = wharf_count + count

        if history_df.iloc[i]['M_TO'] == 'YARD':
            _time = f"{history_df.iloc[i]['MOVING_TIME'].year}. {history_df.iloc[i]['MOVING_TIME'].month}. {history_df.iloc[i]['MOVING_TIME'].day}"
            tmp1.append(_time)
            tmp1.append('YARD')
            tmp1.append('+')
            tmp1.append(f"{translate[history_df.iloc[i]['M_FROM']]}에서 들어옴")
            tmp1.append(f'{yard_count - count}')
            tmp1.append(f'+{count}')
            tmp1.append(yard_count)
            yard_count = yard_count - count

        if history_df.iloc[i]['M_TO'] == '6wharf':
            _time = f"{history_df.iloc[i]['MOVING_TIME'].year}. {history_df.iloc[i]['MOVING_TIME'].month}. {history_df.iloc[i]['MOVING_TIME'].day}"
            tmp2.append(_time)
            tmp2.append('6wharf')
            tmp2.append('+')
            tmp2.append(f"{translate[history_df.iloc[i]['M_FROM']]}에서 들어옴")
            tmp2.append(f'{wharf_count - count}')
            tmp2.append(f'+{count}')
            tmp2.append(wharf_count)
            wharf_count = wharf_count - count
        
        if len(tmp1)!=0:
            result_df.loc[len(result_df)] = tmp1
        if len(tmp2)!=0:
            result_df.loc[len(result_df)] = tmp2
    
    result_df = result_df[result_df['LOCATION'] == location]
    result_df.reset_index(inplace=True)
    del result_df['index']
    del result_df['LOCATION']

    result = result_df.to_json(orient = 'index')
    # print(result)
    return jsonify({'table_data':result})

@app.errorhandler(500)
def internal_error(error):
    return redirect('/')

@app.route('/chart')
def chart():
    # 일단 현재 야적지에 있는 차량들을 전부 불러와야 한다.
    _count = count_mgmt.Count()
    df = _count.get_all()
    # print(df)
    # 그 다음에 차량에 info에 맞게 면적을 곱해준다
    yard_df = df[df.LOCATION == 'YARD']
    wharf_df = df[df.LOCATION == '6wharf']
    yard_df.reset_index(inplace=True)
    wharf_df.reset_index(inplace=True)
    del yard_df['index']
    del wharf_df['index']

    yard_area = 0.0
    wharf_area = 0.0
    _info = info_mgmt.Info()
    info_df = _info.get_all()
    sonata = info_df[info_df.MODEL == 'YFSonata']['AREA'].iat[0]
    for i in range(len(yard_df)):
        model = yard_df.loc[i]['MODEL']
        yard_area += info_df[info_df.MODEL == model]['AREA'].iat[0] * yard_df.loc[i]['COUNT']
    
    for i in range(len(wharf_df)):
        model = wharf_df.loc[i]['MODEL']
        wharf_area += info_df[info_df.MODEL == model]['AREA'].iat[0] * wharf_df.loc[i]['COUNT']
    
    yard_area_rest = info_df[info_df.MODEL == 'YARD']['AREA'].iat[0] - yard_area
    wharf_area_rest = info_df[info_df.MODEL == '6wharf']['AREA'].iat[0] - wharf_area

    yard_data = [['잔여 면적', yard_area_rest], ['야적 면적', yard_area]]
    wharf_data = [['잔여 면적', wharf_area_rest], ['야적 면적', wharf_area]]
    data = [yard_data, wharf_data, int(yard_area_rest//sonata), int(wharf_area_rest//sonata)]
    print(data)
    # 그걸 다 더해서 YARD와 6wharf 면적 값에서 뺀 값을 구하고, 그걸 배열로 넘긴다.
    return render_template('chart.html', data=data)


@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload/xlsx', methods=['GET', 'POST'])
def upload_xlsx():
    if request.method == 'POST':
        f = request.files['file']
        m_from = request.form['from']
        m_to = request.form['to']
        moving_time = request.form['date'] + ' 00:00:00'

        update_xlsx.update_xlsx(f, m_from, m_to, moving_time)
        
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
