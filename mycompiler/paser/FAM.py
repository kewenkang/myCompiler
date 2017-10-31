import re


class LR1FA(object):
    def __init__(self):
        prefix = ''
        #  初始化产生式，非终结符，终结符
        profile = prefix + 'productor.txt'
        self.productors = []
        # 解析所有产生式
        with open(profile, 'r', encoding='utf8') as f:
            for line in f.readlines():
                if line.strip() == '' or line.startswith('/'):
                    continue
                pro = line.split("->")
                if len(pro) != 2:
                    continue
                pro_left = pro[0].strip()
                right = pro[1].strip()
                pro_right = right.split('|')
                for p_r in pro_right:
                    p_r = re.split('\s+', p_r.strip())
                    self.productors.append((pro_left, tuple(p_r)))

        # 加载所有终结符和非终结符
        self.terminal_signal = self.load_file(prefix + "terminalSignal.txt")
        self.unterminal_signal = self.load_file(prefix + "unterminalSignal.txt")
        self.all_signal = self.unterminal_signal + self.terminal_signal

        # print(self.productors)
        # print(self.terminal_signal)
        # print(self.unterminal_signal)

        # 设置起始产生式
        self.start_pro = self.productors[0]

        # 计算项目集
        self.load_all_items()

        # 计算所有非终结符的first集
        self.calc_first()

        # 计算非终结符的follow集
        self.follow = {self.start_pro[0]: set("$")}
        for s in self.unterminal_signal:
            self.follow.setdefault(s, set())
        self.calc_follow()

        # 构造项目集
        self.construct_states({(self.start_pro[0], self.start_pro[1], 0)})

        # 构造SLR转换表
        self.construct_conv_table()

    # 加载终结符与非终结符
    def load_file(self, file):
        l = []
        with open(file, 'r') as f:
            for line in f.readlines():
                l.append(line.strip())
        return l

    def load_all_items(self):
        self.items = []
        for (pro_l, pro_r) in self.productors:
            if pro_r == ("empty",):
                self.items.append((pro_l, (), 0))
                continue
            for i in range(len(pro_r) + 1):
                self.items.append((pro_l, pro_r, i))

    def calc_first(self):
        self.first = {}
        for s in self.unterminal_signal:
            sig_first = self.get_sig_first(s)
            self.first[s] = sig_first

    # 计算某个非终结符的first集
    def get_sig_first(self, signal):
        sig_first = set()
        # if (signal, ['empty']) in self.productors:
        #     sig_first.add('empty')
        if signal in self.terminal_signal:
            sig_first.add(signal)
            return sig_first
        elif signal in self.unterminal_signal:
            for (pro_l, pro_r) in self.productors:
                if pro_l == signal:
                    if "empty" in pro_r:
                        sig_first.add("empty")
                    else:
                        i = 0
                        while i < len(pro_r):
                            cur_sig_first = self.get_sig_first(pro_r[i])
                            if "empty" in cur_sig_first:
                                cur_sig_first.remove("empty")
                                sig_first = sig_first | cur_sig_first
                                i = i + 1
                                if i == len(pro_r):
                                    sig_first.add("empty")
                            else:
                                sig_first = sig_first | cur_sig_first
                                break
            return sig_first

    # 计算一个非终结符串的first集
    def get_pro_first(self, pro_list):
        if len(pro_list) == 0:
            return None

        pro_first = set()
        i = 0
        while i < len(pro_list):
            cur_sig_first = self.get_sig_first(pro_list[i])
            # print(cur_sig_first)
            if "empty" in cur_sig_first:
                cur_sig_first.remove("empty")
                pro_first = pro_first | cur_sig_first
                i = i + 1
                if i == len(pro_list):
                    pro_first.add("empty")
            else:
                pro_first = pro_first | cur_sig_first
                break
        return pro_first

    # 更新follow集
    def calc_follow(self):
        old_follow = None

        while old_follow != self.follow:
            old_follow = self.follow
            for s in self.unterminal_signal:
                sig_follow = self.get_sig_follow(s)
                self.follow[s] =  sig_follow

    # 计算某各非终结符的follow集
    def get_sig_follow(self, signal):
        sig_follow = self.follow.get(signal)

        for (pro_l, pro_r) in self.productors:
            i = 0
            while i < len(pro_r):
                if pro_r[i] == signal:
                    if i == len(pro_r) - 1:
                        pro_l_follow = self.follow.get(pro_l)
                        sig_follow = sig_follow | pro_l_follow
                        break
                    else:
                        rightall = pro_r[i+1:]
                        right_all_first = self.get_pro_first(rightall)
                        if "empty" in right_all_first:
                            right_all_first.remove("empty")
                            sig_follow = sig_follow | right_all_first
                            pro_l_follow = self.follow.get(pro_l)
                            sig_follow = sig_follow | pro_l_follow
                        else:
                            sig_follow = sig_follow | right_all_first
                        break
                i += 1
        return sig_follow

    # CLOSURE闭包
    def closure(self, I):
        if I == None:
            return None
        J = None
        K = I.copy()
        while J != K:
            J = K.copy()
            for item in I:
                if item[2] == len(item[1]):
                    continue
                for (pro_l, pro_r, idx) in self.items:
                    if item[1][item[2]] == pro_l and (pro_l, pro_r, 0) not in I:
                        K.add((pro_l, pro_r, 0))
            I = K.copy()
        return I

    def goto(self, I, X):
        J = set()
        for (pro_l, pro_r, idx) in I:
            if idx < len(pro_r) and pro_r[idx] == X:
                J.add((pro_l, pro_r, idx+1))
        if J == set():
            return None
        return self.closure(J)

    def construct_states(self, start_item_set):
        start_set = self.closure(start_item_set)
        self.C = {0: start_set}
        old_C = None
        copy_C = self.C.copy()
        i = 1
        while old_C != copy_C:
            old_C = copy_C.copy()
            for (state, I) in self.C.items():
                for sig in self.all_signal :
                    sig_goto_set = self.goto(I, sig)
                    if sig_goto_set != None and sig_goto_set not in self.C.values():
                        copy_C[i] = sig_goto_set
                        self.C = copy_C.copy()
                        i += 1
            self.C = copy_C.copy()

    def construct_conv_table(self):
        self.conv_table = {}
        for state, I in self.C.items():
            self.conv_table[state] = {}
            for (pro_l, pro_r, idx) in I:
                if idx < len(pro_r):
                    sig = pro_r[idx]
                    I_j = self.goto(I, sig)
                    for state_i, I_i in self.C.items():
                        if I_i == I_j:
                            j = state_i
                            break
                    if sig in self.terminal_signal:
                        action_str = self.conv_table[state].get(sig, '')
                        if action_str != 's'+str(j):
                            self.conv_table[state][sig] = 's'+str(j)
                    elif sig in self.unterminal_signal:
                        self.conv_table[state][sig] = str(j)
                else:
                    if pro_l == self.start_pro[0]:
                        self.conv_table[state]['$'] = 'acc'
                    else:
                        for a in self.follow[pro_l]:  # SLR文法
                        # for a in self.terminal_signal + ["$"]:  # LR(0)文法
                            if pro_r == ():
                                j = self.productors.index((pro_l, ("empty",)))
                            else:
                                j = self.productors.index((pro_l, pro_r))
                            action_str = self.conv_table[state].get(a, '')
                            if action_str != '':
                                print('1111111')
                            action_str += 'r' + str(j)
                            self.conv_table[state][a] = action_str



if __name__ == '__main__':
    fa = LR1FA()
    # sig_first = fa.get_sig_follow('A')
    # print(sig_first)
    # pro_f = fa.get_pro_first(["A"])
    # print(pro_f)

    # print('follow\n-------------------')
    # for (k, v) in fa.follow.items():
    #     print(k+'---->' +str(v))

    # print('first\n-------------------')
    # for (k, v) in fa.first.items():
    #     print(k + '---->' + str(v))

    print("items:----------")
    for i in fa.items:
        print(i)

    # 测试closure函数
    # item_clo = fa.closure({('Program', ('P',), 0)})
    # for i in item_clo:
    #     print(i)
    # print('-'*30)

    # 测试goto函数
    # item_goto = fa.goto(set([("L'", ('[', 'E', ']', "L'"), 0)]), 'E')
    # print(item_goto)

    print('clusters:\n-----------------')
    for k, I in fa.C.items():
        print(k, '---->', I)

    print("productors:\n----------------")
    for i in range(len(fa.productors)):
        print(i, '--->', fa.productors[i])

    print('conv_table:\n-----------------')
    fa.construct_conv_table()
    for s, t in fa.conv_table.items():
        print(s, '-->', t)
    # print(fa.conv_table)

