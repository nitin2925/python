import sys

type = sys.argv[1]

if type == "t2.micro":
    print("ok, we will create the instance for you")
else:
    print("sorry, we can create instance")
