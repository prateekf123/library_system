from itertools import combinations
count = []
for x in range(int(input())):
    n = int(input())
    for y in range(1,n+1):
        count.extend(list(combinations(range(1,n+1),y)))
        print(count)
    print(len(count)-1)
    count = []