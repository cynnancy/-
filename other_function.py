# 個股三大法人買賣超
from bs4 import BeautifulSoup
from linebot.models import*
import pandas as pd
import time as t
import datetime
import requests

#先抓取個股之證券代碼_stock_dic
#上市
res0 = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=&industry_code=&Page=1&chklike=Y")  
#上櫃
res1 = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=&industry_code=&Page=1&chklike=Y")  
def get_security_number(res0,res1):
    df0_value = pd.read_html(res0.text)[0][2][1:]
    df0_key = pd.read_html(res0.text)[0][3][1:]
    df1_value = pd.read_html(res1.text)[0][2][1:]
    df1_key = pd.read_html(res1.text)[0][3][1:]
    # 儲存成字典
    stock_dic = {}
    for i in range(1,len(df0_key)):
        stock_dic[str(df0_key[i])] = str(df0_value[i])  
    for j in range(1,len(df1_key)):
        stock_dic[str(df1_key[j])] = str(df1_value[j])
    return stock_dic
stock_dic = get_security_number(res0,res1)

#前一交易日當沖前五
def top_pawn(event):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    resp = requests.get('https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E5%B9%B3%E5%9D%87%E6%8C%AF%E5%B9%85+%28%E4%BB%8A%E5%B9%B4%29%40%40%E5%B9%B3%E5%9D%87%E6%8C%AF%E5%B9%85%40%40%E4%BB%8A%E5%B9%B4&SHEET=%E6%BC%B2%E8%B7%8C%E5%8F%8A%E6%88%90%E4%BA%A4%E7%B5%B1%E8%A8%88&SHEET2=%E5%90%84%E6%9C%9F%E5%B9%B3%E5%9D%87%E6%8C%AF%E5%B9%85%E7%B5%B1%E8%A8%88', headers = headers)

    #將亂碼轉碼
    resp.encoding = 'utf - 8'
    soup = BeautifulSoup(resp.text, 'lxml')

    #數據被放在txtStockListData裡面
    data = soup.select_one('#txtStockListData')
    dfs = pd.read_html(data.prettify())

    num = list(dfs[2][:5]['代號'])
    name = list(dfs[2][:5]['名稱'])
    data3 = dfs[1][:5]
    amplitude = list(data3.loc[:5]['3日  平均  振幅'])
    
    one = num[0] + " " + name[0]
    two = num[1] + " "+ name[1]
    three = num[2] + " " + name[2]
    four = num[3] + " " + name[3]
    five = num[4] + " " + name[4]
    
    one_ampl = amplitude[0]
    two_ampl = amplitude[1]
    three_ampl = amplitude[2]
    four_ampl = amplitude[3]
    five_ampl = amplitude[4]
 
    contents = {"type": "bubble",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "前一交易日當沖量前五名之個股",
                    "weight": "bold",
                    "size": "xl",
                    "margin": "none"
                    },
                    {
                    "type": "text",
                    "text": "以及平均三日振福",
                    "size": "lg",
                    "color": "#000000",
                    "wrap": True
                    },
                    {
                    "type": "separator",
                    "margin": "xxl"
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": one,
                            "size": "md",
                            "color": "#555555",
                            "flex": 0
                            },
                            {
                            "type": "text",
                            "text": one_ampl,
                            "size": "md",
                            "color": "#111111",
                            "align": "end"
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": two,
                            "size": "md",
                            "color": "#555555",
                            "flex": 0
                            },
                            {
                            "type": "text",
                            "text": two_ampl,
                            "size": "md",
                            "color": "#111111",
                            "align": "end"
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": three,
                            "size": "md",
                            "color": "#555555"
                            },
                            {
                            "type": "text",
                            "text": three_ampl,
                            "size": "md",
                            "color": "#111111",
                            "align": "end"
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": four,
                            "size": "md",
                            "color": "#555555"
                            },
                            {
                            "type": "text",
                            "text": four_ampl,
                            "size": "md",
                            "color": "#111111",
                            "align": "end"
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": five,
                            "size": "md",
                            "color": "#555555"
                            },
                            {
                            "type": "text",
                            "text": five_ampl,
                            "size": "md",
                            "color": "#111111",
                            "align": "end"
                            }
                        ]
                        }
                    ]
                    }
                ]
                },
                "styles": {
                "footer": {
                    "separator": False
                }
                }
            }

    return contents


# 開始爬蟲的時間，為了區別每次爬蟲
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

#三大法人
def get_juridical_person(stock):
    stock = stock_dic[stock]
    url = "https://histock.tw/stock/chips.aspx?no="
    url = url + stock
    re = requests.get(url)
    df = pd.read_html(re.text) # list型態
    df = df[0]   # 轉變成 DataFrame 型態

    result_lis = df.loc[0,:'自營(避險)']
    # return  result_lis

    data_col_lis = ["日期","外資","投信","自營(自買)","自營(避險)"]
    data_juridical_person = result_lis
    data_juridical_person_lis =[]
    
    for i in data_juridical_person:
        data_juridical_person_lis.append(i)

    for j in range(len(data_juridical_person_lis)):
        data_juridical_person_lis[j] = str(data_juridical_person_lis[j])  

    three_legal_date = data_juridical_person_lis[0]
    fi = data_juridical_person_lis[1]
    invest_trust = data_juridical_person_lis[2]
    self_employed = data_juridical_person_lis[3]
    self_avoid = data_juridical_person_lis[4]

    contents = {"type": "bubble",
                "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                        "type": "text",
                        "text": "三大法人買賣超",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "none"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "日期",
                                "size": "md",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": three_legal_date,
                                "size": "md",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "外資",
                                "size": "md",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": fi,
                                "size": "md",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "投信",
                                "size": "md",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": invest_trust,
                                "size": "md",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "自營(自買)",
                                "size": "md",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": self_employed,
                                "size": "md",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "自營(避險)",
                                "size": "md",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": self_avoid,
                                "size": "md",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        }
                        ]
                    }
                    ]
                },
                "styles": {
                    "footer": {
                    "separator": False
                    }
                }
            }

    return contents


# 判斷隔日沖券商
def distinguish_broker(data,data_1):        
    broker_lis = ['摩根大通','美林','瑞士信貸','凱基-台北','凱基-松山','凱基-市政','凱基-板橋','凱基-士林'
             ,'凱基-永和','凱基-三重','凱基-三多','凱基-斗六','富邦-建國','富邦-台北','富邦-員林','群益-大安'
             ,'元大-土城永寧'] 
    i_lis = []

    for i in range(len(data)) :
        for j in range(len(broker_lis)) :
            if data[i] == broker_lis[j]:
                i_lis.append(i)                
        data_spli = data[i].split('-')

        if len(data_spli) > 1:
            data_spli = data_spli[1]
            if (data_spli == '虎尾') or (data_spli == '嘉義'):
                i_lis.append(i)

    result_name_lis = []
    result_volume_lis = []

    for k in i_lis:
        result_name_lis.append(data[k])
        result_volume_lis.append(data_1[k])

    if int(data_1[0]) < 0:
        # df_name = pd.DataFrame(result_name_lis, columns=['賣超券商名稱'])
        a = {'賣超券商名稱': result_name_lis,'淨賣超':result_volume_lis}
        df_sell_broker = pd.DataFrame(a)
        return df_sell_broker

    elif int(data_1[0]) > 0:
        b = {'買超券商名稱': result_name_lis,'淨買超':result_volume_lis}
        df_buy_broker = pd.DataFrame(b)
        return df_buy_broker

# 開始爬蟲的時間，為了區別每次爬蟲
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# 定義成函數
def get_broker_data(stock):
    respective_table = []
    stock = stock_dic[stock]
    url = "https://histock.tw/stock/branch.aspx?no="
    url = url + stock
    re = requests.get(url)
    df = pd.read_html(re.text) # list型態
    df = df[0]   # 轉變成 DataFrame 型態
    df.columns = ['券商名稱(賣超)','買張','賣張','淨賣超','均價','券商名稱(買超)','買張','賣張','淨買超','均價']
    
    # 分別抓取常見隔日沖券商名稱、買賣超
    name_lis0 = df.loc[:,'券商名稱(賣超)']
    volume_lis0 = df.loc[:,'淨賣超']
    name_lis1 = df.loc[:,'券商名稱(買超)']
    volume_lis1 = df.loc[:,'淨買超']

    sell_result_table = distinguish_broker(name_lis0,volume_lis0)
    buy_result_table = distinguish_broker(name_lis1,volume_lis1)
    
    # 整合成串列(list)
    respective_table.append(stock)
    def sell_table_process(sell_table):
        if sell_table.empty == True :
            respective_table.append('無券商(賣超)')
        else:
            respective_table.append(sell_table)
    def buy_table_process(buy_table):
        if buy_table.empty == True :
            respective_table.append('無券商(買超)')
        else:
            respective_table.append(buy_table)
    
    sell_table_process(sell_result_table)
    buy_table_process(buy_result_table)
    return respective_table

#隔日沖買超
def next_day_over_buy(stock):
    data_broker = get_broker_data(stock)
    data_1 = data_broker[1]
    data_2 = data_broker[2]
    boo_1 = type(data_1)==str
    boo_2 = type(data_2)==str
    
    broker_data_name1 = []
    broker_data_volume1 = []

    if boo_1 !=True:
        data0 = data_1.loc[:,'賣超券商名稱']
        
        for i in data0:
            broker_data_name1.append(i)
            broker_data_name1.insert(0,'賣超券商名稱')
            data1 = data_1.loc[:,'淨賣超']
        for j in data1:
            broker_data_volume1.append(j)
            broker_data_volume1.insert(0,'淨賣超')
    elif boo_1 == True:
        broker_data_name1.append('無券商(賣超)')
        broker_data_volume1.append('無淨賣超')

    broker_data_name2 = []
    broker_data_volume2 = []

    if boo_2 !=True:
        data2 = data_2.loc[:,'買超券商名稱']

        for i in data2:
            broker_data_name2.append(i)
            broker_data_name2.insert(0,'買超券商名稱')
            data3 = data_2.loc[:,'淨買超']

        for j in data3:
            broker_data_volume2.append(j)
            broker_data_volume2.insert(0,'淨買超')

    elif boo_2 == True:
        broker_data_name2.append('無券商(買超)')
        broker_data_volume2.append('無淨買超')
    
    while  len(broker_data_name1) < 5:  
        broker_data_name1.append('.')
    while  len(broker_data_volume1) < 5:  
        broker_data_volume1.append('.')
    while  len(broker_data_name2) < 5:  
        broker_data_name2.append('.')
    while  len(broker_data_volume2) < 5:  
        broker_data_volume2.append('.')

  # 轉成字串型態
    for j in range(len(broker_data_volume1)):
        broker_data_volume1[j] = str(broker_data_volume1[j]) 
    for j in range(len(broker_data_volume2)):
        broker_data_volume2[j] = str(broker_data_volume2[j])

    broker1 = broker_data_name2[1]
    broker1_volume = broker_data_volume2[1]
    broker2 = broker_data_name2[2]
    broker2_volume = broker_data_volume2[2]
    broker3 = broker_data_name2[3]
    broker3_volume = broker_data_volume2[3]
    broker4 = broker_data_name2[4]
    broker4_volume = broker_data_volume2[4]

    contents = {"type": "bubble",
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "(隔日沖)買超券商名稱及其淨買超",
                "weight": "bold",
                "size": "xl",
                "margin": "none"
              },
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "text",
                        "text": "買超券商名稱",
                        "size": "lg",
                        "color": "#2A2A2A",
                        "align": "end",
                        "margin": "xxl"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "淨買超",
                            "size": "lg",
                            "align": "end",
                            "color": "#2A2A2A"
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "text",
                        "text": "1",
                        "align": "start",
                        "size": "md"
                      },
                      {
                        "type": "text",
                        "text": broker1,
                        "size": "md",
                        "color": "#555555"
                      },
                      {
                        "type": "text",
                        "text": broker1_volume,
                        "size": "md",
                        "color": "#555555",
                        "align": "end"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "text",
                        "text": "2",
                        "align": "start",
                        "size": "md"
                      },
                      {
                        "type": "text",
                        "text": broker2,
                        "size": "md",
                        "color": "#555555"
                      },
                      {
                        "type": "text",
                        "text": broker2_volume,
                        "size": "md",
                        "color": "#555555",
                        "align": "end"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "text",
                        "text": "3",
                        "align": "start",
                        "size": "md"
                      },
                      {
                        "type": "text",
                        "text": broker3,
                        "size": "md",
                        "color": "#555555"
                      },
                      {
                        "type": "text",
                        "text": broker3_volume,
                        "size": "md",
                        "color": "#555555",
                        "align": "end"
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "text",
                        "text": "4",
                        "align": "start",
                        "size": "md"
                      },
                      {
                        "type": "text",
                        "text": broker4,
                        "size": "md",
                        "color": "#555555"
                      },
                      {
                        "type": "text",
                        "text": broker4_volume,
                        "size": "md",
                        "color": "#555555",
                        "align": "end"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        }
    return contents

#隔日沖賣超
def next_day_over_sell(stock):
    data_broker = get_broker_data(stock)
    data_1 = data_broker[1]
    data_2 = data_broker[2]
    boo_1 = type(data_1)==str
    boo_2 = type(data_2)==str
    
    broker_data_name1 = []
    broker_data_volume1 = []

    if boo_1 !=True:
        data0 = data_1.loc[:,'賣超券商名稱']

        for i in data0:
            broker_data_name1.append(i)
            broker_data_name1.insert(0,'賣超券商名稱')
            data1 = data_1.loc[:,'淨賣超']

        for j in data1:
            broker_data_volume1.append(j)
            broker_data_volume1.insert(0,'淨賣超')
    elif boo_1 == True:
        broker_data_name1.append('無券商(賣超)')
        broker_data_volume1.append('無淨賣超')

    broker_data_name2 = []
    broker_data_volume2 = []

    if boo_2 !=True:
        data2 = data_2.loc[:,'買超券商名稱']

        for i in data2:
            broker_data_name2.append(i)
            broker_data_name2.insert(0,'買超券商名稱')
            data3 = data_2.loc[:,'淨買超']

        for j in data3:
            broker_data_volume2.append(j)
            broker_data_volume2.insert(0,'淨買超')

    elif boo_2 == True:
        broker_data_name2.append('無券商(買超)')
        broker_data_volume2.append('無淨買超')
    
    while  len(broker_data_name1) < 5:  
        broker_data_name1.append('.')
    while  len(broker_data_volume1) < 5:  
        broker_data_volume1.append('.')
    while  len(broker_data_name2) < 5:  
        broker_data_name2.append('.')
    while  len(broker_data_volume2) < 5:  
        broker_data_volume2.append('.')

  # 轉成字串型態
    for j in range(len(broker_data_volume1)):
        broker_data_volume1[j] = str(broker_data_volume1[j]) 

    for j in range(len(broker_data_volume2)):
        broker_data_volume2[j] = str(broker_data_volume2[j])

    broker1 = broker_data_name1[1]
    broker1_volume = broker_data_volume1[1]
    broker2 = broker_data_name1[2]
    broker2_volume = broker_data_volume1[2]
    broker3 = broker_data_name1[3]
    broker3_volume = broker_data_volume1[3]
    broker4 = broker_data_name1[4]
    broker4_volume = broker_data_volume1[4]

    contents = {"type": "bubble",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
            "type": "text",
            "text": "(隔日沖)賣超券商名稱及其淨賣超",
            "weight": "bold",
            "size": "xl",
            "margin": "none"
            },
            {
            "type": "separator",
            "margin": "xxl"
            },
            {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "賣超券商名稱",
                    "size": "lg",
                    "color": "#2A2A2A",
                    "align": "end",
                    "margin": "xxl"
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "淨賣超",
                        "size": "lg",
                        "align": "end",
                        "color": "#2A2A2A"
                        }
                    ]
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "1",
                    "align": "start",
                    "size": "md"
                    },
                    {
                    "type": "text",
                    "text": broker1,
                    "size": "md",
                    "color": "#555555"
                    },
                    {
                    "type": "text",
                    "text": broker1_volume,
                    "size": "md",
                    "color": "#555555",
                    "align": "end"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "2",
                    "align": "start",
                    "size": "md"
                    },
                    {
                    "type": "text",
                    "text": broker2,
                    "size": "md",
                    "color": "#555555"
                    },
                    {
                    "type": "text",
                    "text": broker2_volume,
                    "size": "md",
                    "color": "#555555",
                    "align": "end"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "3",
                    "align": "start",
                    "size": "md"
                    },
                    {
                    "type": "text",
                    "text": broker3,
                    "size": "md",
                    "color": "#555555"
                    },
                    {
                    "type": "text",
                    "text": broker3_volume,
                    "size": "md",
                    "color": "#555555",
                    "align": "end"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "4",
                    "align": "start",
                    "size": "md"
                    },
                    {
                    "type": "text",
                    "text": broker4,
                    "size": "md",
                    "color": "#555555"
                    },
                    {
                    "type": "text",
                    "text": broker4_volume,
                    "size": "md",
                    "color": "#555555",
                    "align": "end"
                    }
                ]
                }
            ]
            }
        ]
        },
        "styles": {
        "footer": {
            "separator": False
        }
        }
    }
    return contents