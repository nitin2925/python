import os

folders = input("please provide folder names with spaces in between: ").split()

for folder in folders:

    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        print("Please provide valid input")
        break

    print("---------------------- listing of file------" + folder)
    

    for file in files:
        print(file)
