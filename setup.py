# setup.py
# by Preston Hager

import os

def main():
    if os.path.exists(".git"):
        print("Attempting to update git")
        os.system("git pull")
    else:
        print("Cloning repository from github")
        os.system("git clone https://github.com/PrestonHager/KBB.git")
        print("Moving all files to main level")
        os.system("cp -n -a KBB/. . && rm -r KBB")
        print("Please add the bot key and AWS keys and restart.")
        quit()
    os.system("python3 main.py")

if __name__ == '__main__':
    main()
