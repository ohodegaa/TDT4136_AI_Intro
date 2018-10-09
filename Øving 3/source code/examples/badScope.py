'''program causing an error with an undefined variable'''

def main():
    x = 3
    f()

def f():
    print(x)  # error: f does not know about the row defined in main

main()
