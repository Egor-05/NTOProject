import numpy as np
import random
from .models import ShareInfo


def cov_table(data):
    m = []
    for i in data:
        m.append(data[i])
    table = np.array(m,np.float64)
    table = np.cov(table, bias=True)
    for i in range(5):
        for y in range(5):
            table[i][y] = table[i][y]/10000
    return table

def filter(ob, data):
    fl = {}
    k = 0
    for i in range(len(ob)):
        l = len(data[ob[i]]) // 6 + 1
        m = []
        for y in range(0, 6):
            m.append(round(sum(data[ob[i]][(y * l):((y + 1) * l)]) / l, 2))
        fl[ob[i]] = m
        k+=1
    os = 5- k
    v = []
    for i in data:
        if i not in fl:
            v.append(i)
    v = random.sample(v, os)
    for i in v:
        l = len(data[i]) // 6 + 1
        m = []
        for y in range(0, 6):
            m.append(round(sum(data[i][(y * l):((y + 1) * l)]) / l, 2))
        fl[i] = m
    return fl

def math_o(data):
    o = {}
    for i in data:
        o[i] = round(sum(data[i])/len(data[i]), 2)
    return o

def risk_port(cov, doli):
    risk = 0
    for i in range(5):
        for y in range(5):
            risk += doli[i]*doli[y]*cov[i][y]
    return risk

def port_risk(cov, mat_o, max_risk):
    value = [i for i in mat_o]
    ma_dox=0
    max_doli = [0,0,0,0,0]
    risk = 0
    for d1 in range(0, 100):
        for d2 in range(0, 100-d1):
            for d3 in range(0, 100-d1-d2):
                for d4 in range(0, 100 - d1-d2-d3):
                    if d1+d2+d3+d4<=100:
                        dox = d1*mat_o[value[0]]+d2*mat_o[value[1]]+d3*mat_o[value[2]]\
                              +d4*mat_o[value[3]]+ (100- d1-d2-d3-d4)*mat_o[value[3]]
                        dox= dox/100
                        if ma_dox < dox:
                            doli = [d1/100,d2/100,d3/100,d4/100,(100- d1-d2-d3-d4)/100]
                            r = risk_port(cov, doli)
                            if r<max_risk:
                                ma_dox = dox
                                max_doli =doli
                                risk = r
    if ma_dox == 0:
        return [-1, -1, -1]
    doli = {}
    a = []
    for i in mat_o:
        a.append(i)
    for i in range(5):
        doli[a[i]] = max_doli[i]
    return [round(ma_dox, 5), round(risk, 5), doli]

def port_sum(cov, mat_o, su):
    value = [i for i in mat_o]
    ma_dox = 0
    max_doli = [0, 0, 0, 0, 0]
    risk = 1
    for d1 in range(0, 100):
        for d2 in range(0, 100 - d1):
            for d3 in range(0, 100 - d1 - d2):
                for d4 in range(0, 100 - d1 - d2 - d3):
                    if d1 + d2 + d3 + d4 <= 100:
                        dox = d1 * mat_o[value[0]] + d2 * mat_o[value[1]] + d3 * mat_o[value[2]] \
                              + d4 * mat_o[value[3]] + (100 - d1 - d2 - d3 - d4) * mat_o[value[3]]
                        dox = dox / 100
                        if su <= dox:
                            doli = [d1 / 100, d2 / 100, d3 / 100, d4 / 100, (100 - d1 - d2 - d3 - d4) / 100]
                            r = risk_port(cov, doli)
                            if r < risk:
                                ma_dox = dox
                                max_doli = doli
                                risk = r
    if ma_dox == 0:
        return [-1, -1, -1]
    doli = {}
    a = []
    for i in mat_o:
        a.append(i)
    for i in range(5):
        doli[a[i]] = max_doli[i]
    return [round(ma_dox, 5), round(risk, 5), doli]
    pass


def Markov(res_pars, risk=-1,min_sum=-1):
    m_o = math_o(res_pars)
    cov = cov_table(res_pars)
    if risk != - 1:
        return port_risk(cov, m_o, risk)
    else:
        return port_sum(cov, m_o, min_sum)
print()

def get_min_profit(max_risk, companies):
    rez = {}
    for i in ShareInfo.objects.filter(name__in=companies).all():
        rez[i.name] = i.info
    return Markov(res_pars=rez, risk=max_risk)


def get_max_risk(min_profit, companies):
    rez = {}
    for i in ShareInfo.objects.filter(name__in=companies).all():
        rez[i.name] = i.info
    return Markov(res_pars=rez, min_sum=min_profit)