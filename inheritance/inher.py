"""Play with inheritance in Python.
See if children get existing attr of parent class for reorganization
purposes.
"""

class BaseClass:
    def __init__(self, window=None):
        self.window = window
        self.subsection = DerivedClass1()
        self.new_win = DerivedClass2()
        self.var = self.new_win.get_dc1_var()


class DerivedClass1(BaseClass):
    def __init__(self):
        self.dc1_var = "Some new variable"


class DerivedClass2(BaseClass):
    def __init__(self):
        """Can this function access a child var of main window """
        self.var = self.get_dc1_var(self.dc1_var)

    def get_dc1_var(self):
        return self.var


def main():
    win = BaseClass()

if __name__ == "__main__":
    main()


