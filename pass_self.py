"""Passing self as an arg for shared info.
I want <class Section> to be able to access the <class BSub1> obj.

Passing self is valid, can bsub 2 use it though
"""

class Info:
    def __init__(self, master):
        self.inst_var_BSub1 = BSub1(master)
        self.inst_var_BSub2 = BSub2(master, self)
        return


class Base:
    def __init__(self, master):
        self.master = master
        self.info = Info(self.master)
        return


class BSub1:
    def __init__(self, master):
        self.master = master
        self.lower_lim = 1
        self.upper_lim = 5
        return


class BSub2:
    def __init__(self, master, info):
        self.master = master
        self.info = info  
        for i in range (self.info.inst_var_BSub1.upper_lim):
            print(self.info.inst_var_BSub1.lower_lim)
        return


# class Section:
#     def __init__(self):
#         return

def main():
    master = "master" 
    app = Base(master)

main()