import pyhdfs

fs = pyhdfs.HdfsClient("localhost:50070", user_name="ark")
print("Connected")
f = fs.open("/user/ark/orders/output/part-00000")
fr = f.read().decode('UTF-8')
inf = {}
with open("info", "r") as f:
    inf = {}
    for line in f.read().split("\n"):
        line = line.split(':')
        if line == ['']:
            continue
        inf[line[0]] = {i.split('=')[0]: i.split('=')[1] for i in line[1].split(';')[:-1]}
choice = input("Enter a meal:")
if choice in inf:
    items = sorted_x = sorted(inf[choice].items(), key=lambda kv: kv[1], reverse=True)
    for item in items:
        print("{}, {} times".format(*item))

