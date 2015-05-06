sheet_file = "sheet.data"

with open(sheet_file) as f:
    data = [map(int, line.strip().split()) for line in f.readlines()[1:]]

N = len(data)
M = len(data[0])

# compute integral image of the piece
cum_data = [[0 for j in xrange(M+1)] for i in xrange(N+1)]
for i in xrange(1,N+1):
    for j in xrange(1,M+1):
        cum_data[i][j] = data[i-1][j-1] + cum_data[i-1][j] + cum_data[i][j-1] - cum_data[i-1][j-1]

# Return the total value of a square with upper left corner at (x,y)
# and side length = k
def get_square_value(x, y, k, cum_data):
    return cum_data[y+k][x+k] - cum_data[y+k][x] - cum_data[y][x+k] + cum_data[y][x]

# Return the value of the piece with squares of side k with axis at (x,y)
def get_piece_value(x, y, k, cum_data):
    return get_square_value(x-k, y-k, k, cum_data) + get_square_value(x+1, y+1, k, cum_data)

T = int(raw_input())
for case in xrange(1, T+1):
    y0, x0, y1, x1, k = map(int, raw_input().split())
    max_value = 0
    for x in xrange(x0+k , x1-k+1):
        for y in xrange(y0+k, y1-k+1):
            max_value = max(max_value, get_piece_value(x, y, k, cum_data))
    print "Case {}: {}".format(case, max_value)
