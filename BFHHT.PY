import random
num = []
N = int(input('скок'))
for i in range(N):
    ran_num = random.randint(-10, 10)
    num.append(ran_num)

print(num)
zero = 0
seven = 0
minus = 0

for i in range(N):
    if num[i] < 0:
        minus += 1
    if num[i] == 0:
        zero += 1
    if num[i] > 7:
        seven += 1



print(zero, minus, seven)

