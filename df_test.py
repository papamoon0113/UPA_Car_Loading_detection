import history_mgmt, count_mgmt, info_mgmt
from datetime import datetime
import pandas as pd

history_df = pd.read_excel('history.xlsx')

_history = history_mgmt.History()

for i in range(0, len(history_df)):
    time = f"{history_df.loc[i]['MOVING_TIME'].year}-{history_df.loc[i]['MOVING_TIME'].month}-{history_df.loc[i]['MOVING_TIME'].day} {history_df.loc[i]['MOVING_TIME'].hour}:{history_df.loc[i]['MOVING_TIME'].minute}:{history_df.loc[i]['MOVING_TIME'].second}"
    _history.create(history_df.loc[i]['MODEL'], history_df.loc[i]['M_FROM'], history_df.loc[i]['M_TO'], history_df.loc[i]['COUNT'], time)

# count_df = pd.read_excel('table_example.xlsx')
# _count = count_mgmt.Count()

# for i in range(0, len(count_df)):
#     _count.create(count_df.loc[i]['MODEL'], count_df.loc[i]['COUNT'], count_df.loc[i]['LOCATION'])

# logs = _history.find_log('2021-08-01', '2021-08-27')
# print(logs)

# info_df = pd.read_excel('model_info.xlsx')
# _info = info_mgmt.Info()
# print(info_df)
# for i in range(len(info_df)):
#     _info.create(info_df.loc[i]['MODEL'], info_df.loc[i]['AREA'])