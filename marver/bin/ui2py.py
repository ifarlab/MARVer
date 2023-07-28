import os

if __name__ == "__main__":

    # get the latest file name from ./ui/..
    files = [_ for _ in sorted(os.listdir("ui/")) if _.endswith("ui")]
    filename = files[-1]
    #filename="rv_tool_v4_3.ui"

    # get absolute path of pyuic5.exe
    pyuic5Path = os.path.abspath("venv/Scripts/pyuic5.exe")
    guiFilePath = os.path.abspath("ui/" + filename)

    # output file name
    outputFileName = "UI_MARVer.py"

    try:
        print(f"'{filename}' is going to be converted !!")

        # designer.exe output file (filename.ui) is converting to python file (filename.ui).

        # for windows
        # usage => pyuic5.exe -x guiFilename -o targetFilename

        # for ubuntu
        os.system(f"pyuic5 -x {guiFilePath} -o bin/{outputFileName}")

        print(f"'{filename}' is SUCCESSFULY converted !!")

    except:
        print(f"An error occurred while converting '{filename}' !!")