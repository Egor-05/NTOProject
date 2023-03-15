import requests
import pandas as pd
import datetime


def times():
    tim = datetime.datetime.today()-datetime.timedelta(days=1)
    data=tim.strftime("%Y-%m-%d")
    tim= tim.replace(year=tim.year-1).strftime("%Y-%m-%d")
    return [tim, data]


def pars(tim_delt):
    stock_name = {'SBER': '', 'PLZL': '', 'POLY': '', 'GAZP': '', 'LKOH': '', 'TCSG': '', 'MOEX': '', 'TATN': '',
                  'ROSN': '', 'SBERP': '', 'FLOT': '', 'SELG': '', 'MTLRP': '', 'NVTK': '', 'VKCO': '', 'POSI': '',
                  'YNDX': '', 'MTLR': '', 'MAGN': '', 'CBOM': '', 'GMKN': '', 'CHMF': '', 'PHOR': '', 'BSPB': '',
                  'MGNT': ''}
    sl = {}
    for i in stock_name:
        res = requests.get("https://iss.moex.com/iss/engines/stock/markets/shares/securities/{}/candles.json?interval=24&from={}&till={}".format(i, tim_delt[0], tim_delt[1])).json()['candles']['data']
        a = list(map(lambda x: x[2], res))
        if None not in a:
            sl[i] = a
    mi = 366
    for i in sl:
        mi = min(mi, len(sl[i]))
    for i in sl:
        sl[i] = sl[i][:mi]
    return sl


def to_csv(data):
    mi = 366
    pd_data = pd.DataFrame(data)
    pd_data.to_csv("NTO/main/data.csv")


def do_pars():
    res = pars(times())
    to_csv(res)
    return res


do_pars()
