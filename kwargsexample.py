class Foo:
    def set_attr_with_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def main():
    


if __name__ == "__main__":
    main()