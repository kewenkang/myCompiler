# -*- coding: utf-8 -*-
import re

class DFA():

    d0_9 = ['0','1','2','3','4','5','6','7','8','9']
    d1_9 = ['1','2','3','4','5','6','7','8','9']
    d0_7 = ['0','1','2','3','4','5','6','7']
    d0_9a_f = ['0','1','2','3','4','5','6','7','8','9', 'a', 'b', 'c', 'd', 'e', 'f']

    def __init__(self):
        self.conv_table = {
            0: {'0': 2, '1': 1, '2': 1,'3': 1,'4': 1,'5': 1,'6': 1,'7': 1,'8': 1,'9': 1},
            1: {'0': 1, '1': 1, '2': 1,'3': 1,'4': 1,'5': 1,'6': 1,'7': 1,'8': 1,'9': 1},
            2: {'x': 3, '0': 4, '1': 4, '2': 4,'3': 4,'4': 4,'5': 4,'6': 4,'7': 4},
            3: {'0': 5, '1': 5, '2': 5,'3': 5,'4': 5,'5': 5,'6': 5,'7': 5,'8': 5,'9': 5, 'a': 5, 'b': 5, 'c': 5, 'd': 5, 'e': 5, 'f': 5},
            4: {'0': 4, '1': 4, '2': 4,'3': 4,'4': 4,'5': 4,'6': 4,'7': 4},
            5: {'0': 5, '1': 5, '2': 5,'3': 5,'4': 5,'5': 5,'6': 5,'7': 5,'8': 5,'9': 5, 'a': 5, 'b': 5, 'c': 5, 'd': 5, 'e': 5, 'f': 5}
        }

    def move(self, s, c):
        if s in self.conv_table :
            table = self.conv_table[s]
        if c in table:
            return table[c]
        else:
            return 0

class DFA1():
    d0_9 = "[0-9]"
    d1_9 = "[1-9]"
    d0_7 = "[0-7]"
    d0_9a_f = "[0-9a-f]"

    def __init__(self):
        self.conv_table = {
            0: {'0': 2, '[1-9]': 1, "[a-zA-Z_]": 6, "[=!<>\*\+-]": 12,
                "[\(\)\[\];,:{}]": 11, "/": 22, "&": 16, "\|": 14},
            # NUM tokens
            1: {'[0-9]': 1},
            2: {'x': 3, '[0-7]': 4},
            3: {'[0-9a-f]': 5},
            4: {'[0-7]': 4},
            5: {'[0-9a-f]': 5},
            # IDF tokens
            6: {"[a-zA-Z_0-9]": 6},
            # boundary
            11: {},
            # operation
            12: {"=": 13},
            13: {},
            14: {"\|": 15},
            15: {},
            16: {"&": 17},
            17: {},
            # note
            22: {"\*": 23, "/": 26},
            23: {"[^\*]": 23, "\*": 24},
            24: {"[^\*/]": 23, "\*": 24, "/": 25},
            25: {},
            26: {"[\s\S]": 26}


        }
        self.end_status = [1, 2, 4, 5, 6, 12, 13, 14, 15, 16, 17, 22, 25, 26]

    def get_table(self):
        states = [str(s) for s in list(self.conv_table.keys())]
        chars = set()
        for s, v in self.conv_table.items():
            for k, vv in v.items():
                chars.add(k)

        chars = list(chars)
        t_content = [['']*len(chars) for i in range(len(states))]

        for s, v in self.conv_table.items():
            for k, vv in v.items():
                x = states.index(str(s))
                y = chars.index(k)
                if vv in self.end_status:
                    vv = str(vv) + '(end state)'
                    t_content[x][y] = vv
                else:
                    t_content[x][y] = str(vv)


        # for l in t_content:
        #     print(l)
        return states, chars, t_content

    def move(self, s, c):
        if s in self.conv_table :
            table = self.conv_table[s]
            for p, s_to in table.items():
                if re.match(p, c) != None:
                    return s_to
            return 0

if __name__ == '__main__':
    dfa = DFA1()
    a, b, c = dfa.get_table()