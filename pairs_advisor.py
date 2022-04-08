import pyhdfs

fs = pyhdfs.HdfsClient("localhost:50070", user_name="ark")
print("Connected")
f = fs.open("/user/ark/orders/output/part-00000")
fr = f.read().decode('UTF-8')
inf = {}
for line in fr.split("\n"):
    if line:
        key, value = line.split(":")
        value = value.split("\t")
        if key in inf:
            inf[key].append(value)
        else:
            inf[key] = [value, ]
print(inf)
print("-------")

choice = input("Enter a meal:")
if choice in inf:
    items = sorted(inf[choice], key=lambda x: x[1], reverse=True)[:10]
    for item in items:
        print("{}, {} times".format(*item))