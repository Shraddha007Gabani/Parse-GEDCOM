from prettytable import PrettyTable


def familyList():
    """Creates a list that stores the in for of families"""
    flist = [0 for _ in range(6)]
    flist[5] = []
    return flist


def individualList():
    """Creates list that stores values for individuals"""
    return [0 for _ in range(7)]


def lastName(s):
    """Stripe the slashes around last name return last name"""
    string = ''
    for i in s:
        if i != '/':
            string += i
    return string


def getNameUsingID(individualList, ID):
    """This method returns the name which is associated with id i.e takes input as id and return name"""
    for i in individualList:
        if i[0] == ID:
            return i[1]


def gedcomParse(fileName):
    """Parse the gedcom stores the values in respective list and return them"""
    readFile = open(fileName, 'r')
    individualValue = 0
    famValue = 0
    individual_list = []
    fam_list = []
    individualData = individualList()
    famData = familyList()
    for line in readFile:
        lines = line.split()
        if lines:
            if lines[0] == '2':
                if lines[1] == 'DATE':
                    date = lines[4] + " " + lines[3] + " " + lines[2]
                    if dateID == 'BIRT':
                        individualData[3] = date
                    if dateID == 'DEAT':
                        individualData[4] = date
                    if dateID == 'MARR':
                        famData[3] = date
                    if dateID == 'DIV':
                        famData[4] = date

            if lines[0] == '1':
                if lines[1] == 'NAME':
                    individualData[1] = lines[2] + " " + lastName(lines[3])
                if lines[1] == 'SEX':
                    individualData[2] = lines[2]
                if lines[1] == 'BIRT':
                    dateID = 'BIRT'
                if lines[1] == 'DEAT':
                    dateID = 'DEAT'
                if lines[1] == 'MARR':
                    dateID = 'MARR'
                if lines[1] == 'DIV':
                    dateID = 'DIV'
                if lines[1] == 'FAMS':
                    individualData[5] = lines[2]
                if lines[1] == 'FAMC':
                    individualData[6] = lines[2]
                if lines[1] == 'HUSB':
                    famData[1] = lines[2]
                if lines[1] == 'WIFE':
                    famData[2] = lines[2]
                if lines[1] == 'CHIL':
                    famData[5] = lines[2]

            if lines[0] == '0':
                if individualValue == 1:
                    individual_list.append(individualData)
                    individualData = individualList()
                    individualValue = 0
                if famValue == 1:
                    fam_list.append(famData)
                    famData = familyList()
                    famValue = 0
                if lines[1] in ['NOTE', 'HEAD', 'TRLR']:
                    pass
                else:
                    if lines[2] == 'INDI':
                        individualValue = 1
                        individualData[0] = lines[1]
                    if lines[2] == 'FAM':
                        famValue = 1
                        famData[0] = lines[1]
    
    # for i in fam_list:
    #     table1 = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband's Name", "Wife ID",  "Wife's Name", "Children"])
    #     if i[4] == 0:
    #         i[4] = "NA"
    #     table1.add_row([i[0],i[3], i[4], i[1], getNameUsingID(individual_list, i[1]),i[2], getNameUsingID(individual_list, i[2]), i[-1]])
    #     print(table1)
    return individual_list, fam_list


