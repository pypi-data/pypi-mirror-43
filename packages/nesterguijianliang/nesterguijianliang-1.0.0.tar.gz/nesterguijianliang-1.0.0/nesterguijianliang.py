# -*- coding: utf-8 -*-
# @Author: guijianliang
# @Date:   2019-03-08 15:09:32


def lol_list(l):
    for i in l:
        if isinstance(i, list):
            lol_list(i)
        else:
            print(i)
