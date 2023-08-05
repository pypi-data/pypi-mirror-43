#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Profane(): 

    @staticmethod
    def find_all(text, substring):
        return [m.start() for m in re.finditer(substring, text)]
    
    @staticmethod
    def compare_scheme(bt, wt, filter_black_list, mode):
        if mode == "ignore":
            filter_black_list.append(bt)
        elif mode == "preserve":
            if wt[0] <= bt[0] and bt[1] <= wt[1]:
                pass
            elif wt[0] <= bt[0] and wt[1] <= bt[1] and bt[0] < wt[1]:
                pass
            elif bt[0] <= wt[0] and bt[1] <= wt[1] and wt[0] < bt[1] :
                pass
            else :
                filter_black_list.append(bt)
        elif mode == "overlap":
            if wt[0] <= bt[0] and bt[1] <= wt[1]:
                pass
            elif wt[0] <= bt[0] and wt[1] <= bt[1] and bt[0] < wt[1]:
                nt = (wt[1], bt[1])
                filter_black_list.append(nt)
            elif bt[0] <= wt[0] and bt[1] <= wt[1] and wt[0] < bt[1] :
                nt = (bt[0],wt[0])
                filter_black_list.append(nt)
            else :
                filter_black_list.append(bt)

    @staticmethod
    def censor(whitelist, blacklist, text, mark = "*", mode= "preserve"):
        white_hit_list = []
        for white_term in whitelist:
            for hit_id in Profane.find_all(text, white_term):
                white_hit_list.append((hit_id, hit_id + len(white_term)))

        black_hit_list = []
        for profane_term in blacklist:
            for hit_id in Profane.find_all(text, profane_term):
                black_hit_list.append((hit_id, hit_id + len(profane_term)))

        filter_black_list = []
        if len(white_hit_list) == 0:
            filter_black_list = black_hit_list
        else:
            for bt in black_hit_list:
                for wt in white_hit_list:
                    Profane.compare_scheme(bt, wt, filter_black_list, mode)

        censor_text = text
        for tobe_censor in filter_black_list:
            a = tobe_censor[0]
            b = tobe_censor[1]
            censor_text = censor_text.replace(censor_text[a:b], mark * ((b-a) / (1 if isinstance(censor_text[a:b], unicode) else 3)) )
        return censor_text

#print Profane.censor([u"น้ำ"], [u"แม่ง", u"ถุยน้ำลาย"], u"แม่งเอ้ย อย่ามาถุยน้ำลายใส่กับข้าวของลูกค้าสิครับ")
#save
#load
#censor
#detect (yes no)

#print filter(["aba"], ["b", "baba"], "b")
#print filter(["aba"], ["b", "baba"], "aba")
#print filter(["aba"], ["b", "baba"], "baba")
#print censor([u"abcde"], [u"a", u"c", u"d", u"fgh"], u"abcdefghijk", mode = "ignore")
#print censor([u"abcde"], [u"a", u"c", u"d", u"fgh"], u"abcdefghijk", mode = "preserve")
#print censor([u"abcde"], [u"a", u"c", u"defgh"], u"abcdefghijk", mode = "preserve")
#print censor([u"abcde"], [u"a", u"c", u"defgh"], u"abcdefghijk", mode = "overlap")
#print censor([u"บ้าง"], [u"ควาย", u"บ้า"], u"สวัสดีครับ คุณควาย เป็นยังไงบ้างครับ", mode = "preserve")
#print censor([u"น้ำ"], [u"แม่ง", u"ถุยน้ำลาย"], u"แม่งเอ้ย อย่ามาถุยน้ำลายใส่กับข้าวของลูกค้าสิครับ" )