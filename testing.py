import itertools

x = {"andrei": {"score": 20, "varsta": 153},
     "andre": {"score": 19, "varsta": 15},
     "andr": {"score": 100, "varsta": 7},
     "drei": {"score": 2, "varsta": 100}}
# x = [{"score": 20, "varsta": 153},
#      {"score": 19, "varsta": 15},
#      {"score": 100, "varsta": 7},
#      {"score": 2, "varsta": 100}]
# new_d = sorted(x.items(), key=lambda x: x[1]['score'])
# print(new_d)

print((list(x.items())[-1]))
