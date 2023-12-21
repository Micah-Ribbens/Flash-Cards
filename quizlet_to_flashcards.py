# NOTE Make sure that there aren't two empty lines in a row because that's gonna mess up the code
terms = """"""
number_of_enters = 0
enter = """
"""
is_reading_term = True
new = ""
for ch in terms:
    if ch == enter:
        number_of_enters += 1

    if number_of_enters % 4 == 1 and ch == enter:
        new += "}"
        continue

    if number_of_enters % 4 == 2 and ch == enter:
        continue
    if number_of_enters % 4 == 3 and ch == enter:
        continue

    new += ch

# NOTE Make sure to have a file called l.txt
f = open("l.txt", "w+")
f.write(new)