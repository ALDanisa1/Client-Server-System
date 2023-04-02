def number_of_sequences(filename):
    file = open(filename, "r")
    number = 0
    for i in file:
        if i[0] == ">" :
            number = number +1
    return number

def Read_FastA_Names_And_Sequences(filename):
    file = open(filename, "r")
    number = 0
    previous = 0
    data = ""
    data = ""
    List = []
    List2 = []
    for i in file:
        if i[0] == ">"  :
            number = number +1
            data1 = i[1:]
            substrings = data1.split('\n')
            data1 = ' '.join(substrings)
            List2.append(data1)
            if data != "" :
                List.append(data)
                data = ""
        else :
            data = data + i
            substrings = data.split('\n')
            data = ' '.join(substrings)

    
    return List, List2


if __name__ == "__main__":
    print(number_of_sequences("result.txt"))
    #print(Read_FastA_Names_And_Sequences("result.txt"))
    List1, List2 = Read_FastA_Names_And_Sequences("result.txt")
    print(List1)
    