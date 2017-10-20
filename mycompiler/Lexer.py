# -*- coding: utf-8 -*-
import DFA
import re

class Lexer():
    def __init__(self):
        self.dfa = DFA.DFA1()
        self.keywords = None
        keywords_file = "keywords"
        with open(keywords_file, 'r') as k:
            line = k.readline()
            words = line.split(" ")
            self.keywords = words

    def analyze(self, word, line_num=0):
        '''
        analyze every splited word
        :param word:
        :return:
        '''
        def output(s1, t):
            if s1 == 1:
                print("<DEC,", t, ">")
            elif s1 == 2:
                print("<DEC,", 0,">")
            elif s1 == 3:
                print("unfinished HEX")
            elif s1 == 4:
                print("<OCT,", t, ">")
            elif s1 == 5:
                print("<HEX,", t, ">")
            elif s1 == 6:
                if t in self.keywords:
                    print("<" + t, ", _ >")
                else:
                    print("<IDF,", t, ">")
            elif s1 in [11, 12, 13, 14, 15, 16, 17, 22]:
                print("<" + t, ", _ >")
            elif s1 in [25]:
                print("<NOTE,", t, ">")

        def output1(s1, t, line_num):
            ret_token_str = str(line_num) + '\t'
            if s1 == 1:
                ret_token_str += "<DEC,"+ t+ ">"
            elif s1 == 2:
                ret_token_str += "<DEC, 0 >"
            elif s1 == 3:
                ret_token_str += "unfinished HEX"
            elif s1 == 4:
                ret_token_str += "<OCT,"+ t+ ">"
            elif s1 == 5:
                ret_token_str += "<HEX,"+ t+ ">"
            elif s1 == 6:
                if t in self.keywords:
                    ret_token_str += "<" + t+ ", _ >"
                else:
                    ret_token_str += "<IDF,"+ t+ ">"
            elif s1 in [11, 12, 13, 14, 15, 16, 17, 22]:
                ret_token_str += "<" + t+ ", _ >"
            elif s1 in [25, 26]:
                ret_token_str += "<NOTE,"+ t+ ">"
            return ret_token_str

        token = ''
        s = 0
        i = 0
        line_idx = 1
        tokens = []
        while i<len(word):
            c = word[i]
            s = self.dfa.move(s, c)
            if re.match('\n', c):
                line_idx += 1
            if re.match('\s', c) == None:
                token += c
            elif s in [23, 24, 26]:
                if s == 26 and re.match('\n', c) == None:
                    token += c
                else:
                    token += c
            if i < len(word)-1:
                c_next = word[i + 1]
                s_next = self.dfa.move(s, c_next)
                if s != 0 and s_next == 0:
                    tokens.append(output1(s, token, line_idx))
                    token = ''
                    s = 0
            else:
                tokens.append(output1(s, token, line_idx))
            i = i+1
        return tokens

    def lex_splited(self, content):
        lines = content.strip().split('\n')
        tokens = []

        for i in range(len(lines)):
            line_num = i+1
            line = lines[i]
            blank = re.compile("[ \t]+")
            words = blank.split(line.strip())

            for w in words:
                tokens.extend(self.analyze(w, line_num))
        return tokens

    def lex_lines(self, content):
        lines = content.strip().split('\n')
        tokens = []

        for i in range(len(lines)):
            line_num = i+1
            line = lines[i]
            # blank = re.compile("[ \t]+")
            # words = blank.split(line.strip())
            #
            # for w in words:
            tokens.extend(self.analyze(line, line_num))
        return tokens

    def lex(self, content):

        tokens = self.analyze(content)
        return tokens

if __name__=='__main__':
    l = Lexer()
    # str = '<>'
    # print('test1:')
    # l.analize(str)
    # a = re.match("[!<>]", '<>')
    # print(a)
    # print(re.compile("/").split("ss *dsdsdad/ **d/sdsdss*   dsds  sda ".strip()))


    content = ''
    with open("example.txt", 'r', encoding='utf8') as f:
        for line in f:
            content += line
    # print(content)

    tokens = l.lex(content)
    for t in tokens:
        print(t)
    # def xxx():
    #     for i in range(10):
    #         yield i
    # x = xxx()
    # for i in x:
    #     print(i)