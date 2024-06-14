with open("InstructionSet.py", "r") as inp:
    with open("temp.txt", "w") as out:
        lines = inp.readlines()
        for line in lines:
            if line[0] != "#" and line != "\n":
                line = line.replace("=", " :")
                s = line.split(" ", maxsplit=1)
                w = '"' + s[0][4:] + '"' + s[1][:-1] + ",\n"
                print(w)
                out.write(w)
            else:
                out.write(line)
