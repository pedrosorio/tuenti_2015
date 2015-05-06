from collections import Counter

book = []
with open("book.data") as file:
    book = [line.strip().split() for line in file.readlines()]

IDX = 0
GOLD = 1
SOURCES = 2

M = len(book)
name_to_id = {}
base_to_compound = [[] for i in xrange(M)]
# convert names to position in the list
# and compile list of compounds that can be
# formed using each element
for i in xrange(M):
    name_to_id[book[i][0]] = i
    book[i][0] = i
    book[i][1] = int(book[i][1])
    for j in xrange(2, len(book[i])):
        # this works because the book is sorted topologically
        book[i][j] = name_to_id[book[i][j]]
        base_to_compound[book[i][j]].append(i)
    # replace the list of sources with a single Counter object
    if len(book[i]) > 2:
        book[i][2] = Counter(book[i][2:])
    else:
        book[i].append(Counter([]))

def gold_in_inventory(book, inventory):
    return sum([count * book[i][GOLD] for i, count in inventory.items()])

# whether the inventory has the necessary items to cook the compound
def can_cook(inventory, compound):
    if compound[SOURCES] - inventory:
        return False
    return True

# returns counter of elements left after cooking compound with inventory
# only makes sense if can_cook(book, inventory, compound) == True
def left_after_cook(inventory, compound):
    return inventory - compound[SOURCES] + Counter([compound[IDX]])

def solve(book, inventory):
    max_gold = gold_in_inventory(book, inventory)
    visited = set([tuple(inventory.items())])
    stack = [inventory]
    while stack:
        inventory = stack.pop()
        for el_idx, count in inventory.items():
            for c_idx in base_to_compound[el_idx]:
                if can_cook(inventory, book[c_idx]):
                    next_inventory = left_after_cook(inventory, book[c_idx])
                    items = tuple(next_inventory.items())
                    if items not in visited:
                        visited.add(items)
                        stack.append(next_inventory)
                        max_gold = max(max_gold, gold_in_inventory(book, next_inventory))
    return max_gold

N = int(raw_input())
for case in xrange(N):
    # get a count of each element
    example = Counter([name_to_id[element] for element in raw_input().split()])
    print solve(book, example)





