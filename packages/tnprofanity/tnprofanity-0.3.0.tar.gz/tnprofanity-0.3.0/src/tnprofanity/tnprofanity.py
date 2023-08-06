#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os, sys

class Profane(): 

    @staticmethod
    def find_all(text, substring):
        return [m.start() for m in re.finditer(substring, text)]
    
    @staticmethod
    def compare_scheme(bt, wt, filter_black_list, mode):
        if mode == "ignore":
            filter_black_list.add(bt)
        elif mode == "preserve":
            if wt[0] <= bt[0] and bt[1] <= wt[1]:
                pass
            elif wt[0] <= bt[0] and wt[1] <= bt[1] and bt[0] < wt[1]:
                pass
            elif bt[0] <= wt[0] and bt[1] <= wt[1] and wt[0] < bt[1]:
                pass
            else :
                filter_black_list.add(bt)
        elif mode == "overlap":
            if wt[0] <= bt[0] and bt[1] <= wt[1]:
                pass
            elif wt[0] <= bt[0] and wt[1] <= bt[1] and bt[0] < wt[1]:
                nt = (wt[1], bt[1])
                filter_black_list.add(nt)
            elif bt[0] <= wt[0] and bt[1] <= wt[1] and wt[0] < bt[1]:
                nt = (bt[0],wt[0])
                filter_black_list.add(nt)
            else :
                filter_black_list.add(bt)

    @staticmethod
    def _censorProfane(filter_black_list, text, mark):
        censor_text = text
        for tobe_censor in filter_black_list:
            a = tobe_censor[0]
            b = tobe_censor[1]
            censor_part = mark * ((b-a) / (1 if isinstance(censor_text[a:b], unicode) else 3))
            censor_text = censor_text[:a] + censor_part + censor_text[b:]
        return censor_text

    @staticmethod
    def _screenProfane(whitelist, blacklist, text, mode):
        white_hit_list = []
        for white_term in whitelist:
            for hit_id in Profane.find_all(text, white_term):
                white_hit_list.append((hit_id, hit_id + len(white_term)))

        black_hit_list = []
        for profane_term in blacklist:
            for hit_id in Profane.find_all(text, profane_term):
                black_hit_list.append((hit_id, hit_id + len(profane_term)))

        filter_black_list = set([])
        if len(white_hit_list) == 0:
            filter_black_list = set(black_hit_list)
        else:
            for bt in black_hit_list:
                for wt in white_hit_list:
                    Profane.compare_scheme(bt, wt, filter_black_list, mode)
        return filter_black_list

    @staticmethod
    def _verifyParam(text, whitelist, blacklist, mode):
        assert isinstance(text, unicode), "text must be unicode {}".format(type(text))
        for term in whitelist:
            assert isinstance(term, unicode), "whitelist term must be unicode : {}".format(term)
        for term in blacklist:
            assert isinstance(term, unicode), "blacklist term must be unicode : {}".format(term)
        
        assert mode in ["ignore", "preserve", "overlap"], "mode must be 'ignore', 'preserve', 'overlap'"

    @staticmethod
    def censor(text, whitelist = [], blacklist = [],mark = "*", mode = "preserve"):
        Profane._verifyParam(text, whitelist, blacklist, mode)

        whitelist_default = []
        with open(os.path.dirname(os.path.abspath(__file__))+"/thai_white_wordlist.txt") as file:
            whitelist_default = [l.strip().decode("utf-8") for l in file]
        whitelist += whitelist_default

        blacklist_default = []
        with open(os.path.dirname(os.path.abspath(__file__))+"/thai_profane_wordlist.txt") as file:
            blacklist_default = [l.strip().decode("utf-8") for l in file]
        blacklist += blacklist_default
        
        filter_black_list = Profane._screenProfane(whitelist, blacklist, text, mode)
        censored_text = Profane._censorProfane(filter_black_list, text, mark)
        return censored_text
    
    @staticmethod
    def check(text, whitelist = [], blacklist = [], mode = "preserve"):
        Profane._verifyParam(text, whitelist, blacklist, mode)

        whitelist_default = []
        with open(os.path.dirname(os.path.abspath(__file__))+"/thai_white_wordlist.txt") as file:
            whitelist_default = [l.strip().decode("utf-8") for l in file]
        whitelist += whitelist_default

        blacklist_default = []
        with open(os.path.dirname(os.path.abspath(__file__))+"/thai_profane_wordlist.txt") as file:
            blacklist_default = [l.strip().decode("utf-8") for l in file]
        blacklist += blacklist_default
        
        filter_black_list = Profane._screenProfane(whitelist, blacklist, text, mode)

        ProfaneFound = []
        for tobe_censor in filter_black_list:
            fid = tobe_censor[0]
            lid = tobe_censor[1]
            ProfaneFound.append((text[fid:lid],fid,lid))
        return ProfaneFound

#save
#load
#censor
#detect (yes no)