# -*- coding: utf-8 -*-

import math
import pandas as pd
import os
import re
import numpy as np
import networkx as nx

strl_dict = {}
log_dict = {}


def getlog(n):
    res = 0.0
    # if n in log_dict:
    if log_dict.has_key(n):
        return log_dict[n]
    if n == 0:
        return math.log(1.0)
    if len(log_dict) != 0:
        res = log_dict[len(log_dict)]
    for i in range(len(log_dict), n):
        res = res + math.log(1.0 * (i + 1))
        log_dict[i + 1] = res
    return res


def getpvalue(cc_dict, v_dict, M, N):
    edgs = N * (N - 1) / 2
    fenmu = getlog(edgs) - getlog(M) - getlog(edgs - M)
    min1 = N - 1
    if M < min1:
        min1 = M
    min1 += 1
    f1 = N - 1
    f2 = edgs - f1
    p_list = []
    for k in cc_dict.keys():  # cc <- cluster coefficient
        c = cc_dict[k]
        d = v_dict[k]
        ori = 0.0
        for i in range(d, min1):
            f3 = i * (i - 1) / 2
            j = int(math.ceil(c * f3))
            min2 = M - i
            if j <= min2 and j <= f3:
                p = getlog(f1) - getlog(i) - getlog(f1 - i) + getlog(f3) - getlog(j) - getlog(f3 - j) + getlog(f2 - j) - getlog(M - i - j) - getlog(f2 - j - (M - i - j)) - fenmu
                ori += math.exp(p)
        pvalue = ori
        p_list.append(pvalue)
    print("------------p值列表--------------")
    print(p_list)
    print(len(p_list))
    return p_list


def getfdr(p_list, alpha):
    d = {}
    i = 0
    for p in p_list:
        d[i] = p
        i += 1
    sorted_dict = sorted(d.items(), key=lambda x: x[1], reverse=False)
    print("--------ranked p_list---------")
    print (sorted_dict)
    print(len(sorted_dict))
    index = 0
    maxindex = 0
    m = len(p_list)
    print(m)
    for index, p in sorted_dict:
        index += 1
        if p < index * 1.0 * alpha / m:
            maxindex = index
        #print(maxindex)
    print(maxindex)
    aftercontrol = []
    for i in range(0, maxindex):
        aftercontrol.append(sorted_dict[i][0])
    print("---------aftercontrol------------")
    print(aftercontrol)
    print(len(aftercontrol))
    return aftercontrol


def process(filename):
    g = pd.read_csv("F:/Peggy/Python/vertex centrality/sample.txt", sep = ' ', header=None)
    print(g)
    g1 = np.mat(g)
    print(g1)

    G = nx.from_numpy_matrix(g1)
    #G = nx.Graph(g1_list)
    nodes = list(G)
    #print(nodes)
    #print(nodes[3])
    #print(G[nodes[3]])
    #nbrs = list(G[nodes[3]])
    print("\n")
    print("--------clustering coeffcient of each node--------")
    cc_dict = nx.clustering(G)
    print(cc_dict)
    print(type(cc_dict))

    M = len(G.edges())
    print(M)
    print("********")

    N = len(cc_dict)  # vertices
    #print(N)

    print(G.degree())
    print(type(G.degree()))
    v_dict = {}
    for n,d in G.degree():
       v_dict[n] = d
    print(v_dict)

    print("********")

    N = len(v_dict)  # vertices
    print(N)
    """a = []
    for k in v_dict:
        a.append(v_dict[k])
    print(a)
    degrees = a  # degrees"""

    p_list = getpvalue(cc_dict, v_dict, M, N)
    print("--------pvalue--------")
    print(p_list)
    p_list = [x * N for x in p_list]
    cc_node_list = []
    cc_node_list = list(cc_dict.keys())
    print(cc_node_list)
    node_p = dict(zip(cc_node_list, p_list))
    print(node_p)
    print(len(node_p))
    node_p_sorted = sorted(node_p.items(), key = lambda x: x[1])
    print(node_p_sorted)
    print(type(node_p_sorted))

    adjust_p = []
    for i in range(len(p_list)):
        adjust = (i+1) * 1.0 * 0.01 / len(p_list)
        adjust_p.append(adjust)
    print(adjust_p)
    line = 0
    for k,v in node_p_sorted:
        line += 1
       # writeline = str(p_sorted[i]) + " : " + str(adjust_p[i]) + "\n"
        if v < adjust_p[line-1]:
            print(str(line) + " " + str(k) + " : " + str(v) + " : " + str(adjust_p[line-1]) + "\n")
    #print(writeline)



if __name__ == "__main__":
    filename = "sample.txt"
    process(filename)




