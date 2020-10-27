""" Implement user stories for GEDCOM parser

    date: 30-Sep-2020
    python: v3.8.4
"""
import operator
from typing import List, Dict, TextIO, Union
from datetime import datetime, timedelta
from models import Individual, Family
from app import get_lines, generate_classes, findParents, checkIfSiblings

lines = get_lines('SSW555-P1-fizgi.ged')
individuals, families = generate_classes(lines)
individuals.sort(key=operator.attrgetter('id'))
families.sort(key=operator.attrgetter('id'))


def birth_before_death_of_parents(family: Family, individuals: List[Individual]) -> bool:
    """ US09: verify that children are born before death of mother
        and before 9 months after death of father """

    husb = next(ind for ind in individuals if ind.id == family.husb)
    wife = next(ind for ind in individuals if ind.id == family.wife)

    if not husb.deat and not wife.alive:
        return True

    for child_id in family.chil:
        child_birth_date = next(ind.birt['date'] for ind in individuals if ind.id == child_id)
        child_birth_date = datetime.strptime(child_birth_date, "%d %b %Y")

        if husb.deat:
            husb_death_date = husb.deat['date']
            husb_death_date = datetime.strptime(husb_death_date, "%d %b %Y")

            if child_birth_date > husb_death_date + timedelta(days=270):
                print(f"✘ Family ({family.id}): Child ({child_id}) should be born "
                      f"before 9 months after death of father")
                return False

        if wife.deat:
            wife_death_date = wife.deat['date']
            wife_death_date = datetime.strptime(wife_death_date, "%d %b %Y")

            if child_birth_date > wife_death_date:
                print(f"✘ Family ({family.id}): Child ({child_id}) should be born before death of mother")
                return False
    else:
        print(f"✔ Family ({family.id}): Children are born before death of mother "
              f"and before 9 months after death of father")
        return True


def were_parents_over_14(family: Family, individuals: List[Individual]) -> bool:
    """ US10: verify that parents were at least 14 years old at the marriage date """
    marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")

    husb_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.husb)
    husb_birthday = datetime.strptime(husb_birthday, "%d %b %Y")
    husb_marr_age = marr_date.year - husb_birthday.year - \
                    ((marr_date.month, marr_date.day) < (husb_birthday.month, husb_birthday.day))

    wife_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.wife)
    wife_birthday = datetime.strptime(wife_birthday, "%d %b %Y")
    wife_marr_age = marr_date.year - wife_birthday.year - \
                    ((marr_date.month, marr_date.day) < (wife_birthday.month, wife_birthday.day))

    if husb_marr_age >= 14 and wife_marr_age >= 14:
        print(f"✔ Family ({family.id}): Both parents were at least 14 at the marriage date")
        return True

    if husb_marr_age < 14 and wife_marr_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_marr_age}) "
              f"and Wife ({wife_marr_age}) can not be less than 14")
    elif husb_marr_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_marr_age}) can not be less than 14")
    elif wife_marr_age < 14:
        print(f"✘ Family ({family.id}): Wife ({wife_marr_age}) can not be less than 14")

    return False


def fewer_than_15_siblings(family: Family) -> bool:
    if len(family.chil) < 15:
        print(f"✔ Family ({family.id}): Siblings are less than 15")
        return True
    else:
        print(f"✘ Family ({family.id}): Siblings are greater than 15")
        return False


def male_last_names(family: Family, individuals: List[Individual]):
    ids = [family.husb, family.wife]
    ids.extend(family.chil)
    males = [individual for individual in individuals if individual.sex == 'M' and individual.id in ids]
    names = [male.name.split('/')[1] for male in males]
    return len(set(names)) == 1


def marriage_before_death(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that marrriage before death of either spouse """
    mrgDate = datetime.strptime(family.marr.get('date'), "%d %b %Y")

    husb = list(filter(lambda x: x.id == family.husb, individuals))[0]
    wife = list(filter(lambda x: x.id == family.wife, individuals))[0]

    husbandDeathDate = datetime.strptime(husb.deat.get('date'), "%d %b %Y") if husb.deat else None
    wifeDeathDate = datetime.strptime(wife.deat.get('date'), "%d %b %Y") if wife.deat else None

    if (husbandDeathDate and husbandDeathDate - mrgDate > timedelta(minutes=0)) or (
            wifeDeathDate and wifeDeathDate - mrgDate > timedelta(minutes=0)):
        print(
            f"✔ Family ({family.husb}) and ({family.wife}):Their marriage took place, before either of their death, So the condition is valid.")
        return True
    else:
        print(
            f"✘ Husband ({family.husb}): Wife ({family.wife}) Marriage did not take place before either of their death, So that is not valid.")
        return False


def divorce_before_death(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that divorce before death of either spouse """
    divdate = datetime.strptime(family.div.get('date'), "%d %b %Y")

    husb = list(filter(lambda x: x.id == family.husb, individuals))[0]
    wife = list(filter(lambda x: x.id == family.wife, individuals))[0]

    husbandDeathDate = datetime.strptime(husb.deat.get('date'), "%d %b %Y") if husb.deat else None
    wifeDeathDate = datetime.strptime(wife.deat.get('date'), "%d %b %Y") if wife.deat else None

    if (husbandDeathDate and husbandDeathDate - divdate > timedelta(minutes=0)) \
            or (wifeDeathDate and wifeDeathDate - divdate > timedelta(minutes=0)):
        print(f"✔ Family ({family.husb}) and ({family.wife}): Their divorce took place, "
              f"before either of their death, So the condition is valid.")
        return True
    else:
        print(f"✘ Husband ({family.husb}) and Wife ({family.wife}): Divorce did not take place "
              f"before either of their death, So that is not valid.")
        return False


def checkBigamy(family: Dict):
    """Method that checks bigamy in the given gedcom data
    if yes then it pops and update data with no bigamy"""
    for f in family:
        if 'HUSB' in family[f]:
            hus_id = family[f]['HUSB']
            if 'WIFE' in family[f]:
                wife_id = family[f]['WIFE']

        wife_count = 0
        husb_count = 0

        for f in family:
            if 'HUSB' in family[f]:
                hus_id2: List = family[f]['HUSB']
                if hus_id == hus_id2:
                    husb_count += 1
                if 'WIFE' in family[f]:
                    wife_id2: List = family[f]['WIFE']
                    if wife_id == wife_id2:
                        wife_count += 1
            else:
                continue


def getAge(born):
    """returns age of individual"""
    born = datetime.strptime(born, '%d %b %Y')
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def checkForOldParents(fam: Dict, ind: Dict, file: TextIO):
    """check the age of individuals and return boolean value
    if there are old parents in given data false otherwise"""
    result: bool = True
    for f in fam:
        if "CHIL" in fam[f]:
            wife: str = "0"
            husb: str = "0"
            if "HUSB" in fam[f]:
                husb: str = fam[f]["HUSB"]
            if "WIFE" in fam[f]:
                wife: str = fam[f]["WIFE"]
            wifeAge: int = 0
            husbAge: int = 0
            if wife in ind and "BIRT" in ind[wife]:
                wifeAge: Union[int, bool] = getAge(ind[wife]["BIRT"])
            if husb in ind and "BIRT" in ind[husb]:
                husbAge: Union[int, bool] = getAge(ind[husb]["BIRT"])
            for c in fam[f]["CHIL"]:
                childAge: int = 0
                if "BIRT" in ind[c]:
                    childAge: Union[int, bool] = getAge(ind[c]["BIRT"])
                if wifeAge - childAge > 60:  # throw wife error
                    file.write(
                        "ERROR US12: Mother " + wife + " is older than their child, " + c + " by over 60 years\n")
                    result: bool = False
                if husbAge - childAge > 80:  # throw husb error
                    file.write(
                        "ERROR US12: Father " + husb + " is older than their child, " + c + " by over 80 years\n")
                    result: bool = False
    return result


def birth_before_marriage_of_parents(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that divorce before death of either spouse """
    mrgdate = datetime.strptime(family.marr.get('date'), "%d %b %Y")
    divdate = datetime.strptime(family.div.get('date'), "%d %b %Y")
    birthdate_child = datetime.strptime(individuals.birt.get('date'), "%d %b %Y")

    if family.marr:
        if birthdate_child - mrgdate > timedelta(minutes=0) and birthdate_child - divdate < timedelta(days=275):
            print(f"({family.id}) : birth_before_marriage_of_parents")
            return True
        else:
            print(f"({family.id}) : not birth_before_marriage_of_parents")
            return False
    else:
        print(f"({family.id}) : marrige is not happen")
        return False


def less_than_150(individual: Individual) -> bool:
    birth_date: datetime = datetime.strptime(individual.birt['date'], "%d %b %Y")
    current_date: datetime = datetime.now()
    years_150 = timedelta(days=54750)

    if individual.deat:
        death_date: datetime = datetime.strptime(individual.deat['date'], "%d %b %Y")
        if birth_date - death_date > timedelta(days=0):
            print(f"✘ individual ({individual.id}): The person's age is grater than 150 ")
            return False
        elif death_date - birth_date < years_150:
            print(f"✔ individual ({individual.id}): The person's age is less than 150 ")
            return True

    else:
        if current_date - birth_date < years_150:
            print(f"✔ individual ({individual.id}): The person's age is less than 150 ")
            return True

    print(f"✘ individual ({individual.id}): The person's age is not than than 150 ")

    return False


today: datetime = datetime.now()
year: timedelta = timedelta(minutes=0)


def marriage(family: Family) -> bool:
    if family.marr:
        marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")
        if today - marr_date > timedelta(minutes=0):
            print(f"✔ ({family.id}): marrige take place before current date ")
            return True
        else:
            print(f"✘ ({family.id}): marrige didn't take place before current date ")

    else:
        print(f"✘ ({family.id}): marrige didn't take place ")


def divo(family: Family) -> bool:
    if family.div:
        div_date: datetime = datetime.strptime(family.div['date'], "%d %b %Y")
        if today - div_date > timedelta(minutes=0):
            print(f"✔ ({family.id}): divorce take place before current date ")
            return True
        else:
            print(f"✘ ({family.id}): divorce didn't take place before current date ")

    else:
        print(f"✘ ({family.id}): divorce didn't take place ")


def birth(indi: Individual) -> bool:
    if indi.birt:
        birt_date: datetime = datetime.strptime(indi.birt['date'], "%d %b %Y")
        if today - birt_date > timedelta(minutes=0):
            print(f"✔ ({indi.id}): birth take place before current date ")
            return True
        else:
            print(f"✘ ({indi.id}): birth didn't take place before current date ")

    else:
        print(f"✘ ({indi.id}): birth didn't take place ")


def death(indi: Individual) -> bool:
    if indi.deat:
        death_date: datetime = datetime.strptime(indi.deat['date'], "%d %b %Y")
        if today - death_date > timedelta(minutes=0):
            print(f"✔ ({indi.id}): death take place before current date ")
            return True
        else:
            print(f"✘ ({indi.id}): death didn't take place before current date ")

    else:
        print(f"✘ ({indi.id}): death didn't take place ")


def birth_before_mrg(family: Family, individuals: Individual) -> bool:
    birth_date: datetime = datetime.strptime(individuals.birt['date'], "%d %b %Y")

    if family.marr:  # condition for the divorce
        marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")
        if marr_date - birth_date > timedelta(minutes=0):
            print(f"✔ ({individuals.id}):birth is before mrg")
            return True
        else:
            print(f"✘ ({individuals.id}):birth is not before mrg")
            return False
    else:
        print(f"✘ ({individuals.id}):no mrg")
        return True


def marriage_before_divorce(family: Family) -> bool:
    marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")  # get the marriage date

    if family.div:  # condition for the divorce
        div_date: datetime = datetime.strptime(family.div['date'], "%d %b %Y")
        if div_date - marr_date > timedelta(minutes=0):
            print(f"Individual:({family.id}):marriage is before divorce")
            return True
        else:
            print(f"({family.id}):marriage can not take place before divorce")
            return False
    else:
        print(f"({family.id}):There is no divorce")
        return True


# US14 no more than 5 siblings born the same day
def verifySiblingsDates(allDates):
    retValue = True
    datesDict = {}
    for d in allDates:
        if d in datesDict:
            datesDict[d] = datesDict.get(d) + 1
            if datesDict[d] > 5:
                return False
        else:  # if we did not find this date, we first check if we have date within day of already found dates
            found = False
            for d2 in datesDict:
                delta = d2 - d
                if abs(delta.days) < 2:
                    datesDict[d2] = datesDict.get(d2) + 1
                    found = True
                    if datesDict[d2] > 5:
                        retValue = False
                        break
            if not found:
                datesDict[d] = 1

    return retValue


# US13 Sbiling space
def verifySiblingsSpace(allDates):
    retValue = True
    datesSet = set()
    for d in allDates:
        if d in datesSet:
            retValue = False
            break
        else:
            found = False
            for d2 in datesSet:
                delta = d2 - d
                if abs(delta.days) > 1 and abs(delta.days) < 280:
                    retValue = False
                    break
            if retValue:
                datesSet.add(d)
            else:
                break

    return retValue


# siblingsDates = (datetime.date(1990, 1, 1), datetime.date(1991, 1, 1))
# print(verifySiblingsDates(siblingsDates))


def birth_before_death(individuals: Individual) -> bool:
    birth_date: datetime = datetime.strptime(individuals.birt['date'], "%d %b %Y")

    if individuals.deat:  # condition for the divorce
        deat_date: datetime = datetime.strptime(individuals.deat['date'], "%d %b %Y")
        if deat_date - birth_date > timedelta(minutes=0):
            print(f"({individuals.id}):birth is before death")
            return True
        else:
            print(f"({individuals.id}):birth can not take place not before death")
            return False
    else:
        print(f"({individuals.id}):no death")
        return True


def correct_gender_for_role(family: Family, individuals: List[Individual]) -> bool:
    """ US21: verify that Husband in family is male and wife in family is female """
    husb_gender = next(ind.sex for ind in individuals if ind.id == family.husb)
    wife_gender = next(ind.sex for ind in individuals if ind.id == family.wife)

    if husb_gender == 'M' and wife_gender == 'F':
        print(f"✔ Family ({family.id}): Both parents have the correct gender for the role")
        return True

    if husb_gender == 'F' and wife_gender == 'M':
        print(f"✘ Family ({family.id}): Husband should be Male and Wife should be Female")
    elif husb_gender == 'F':
        print(f"✘ Family ({family.id}): Husband should be Male")
    elif wife_gender == 'M':
        print(f"✘ Family ({family.id}): Wife should be Female")

    return False


def unique_ids(families: List[Family], individuals: List[Individual]) -> bool:
    """ US22: verify that All individual IDs are unique and all family IDs are unique """
    ids = [family.id for family in families] + [individual.id for individual in individuals]

    recurrent_ids = list(set([_id for _id in ids if ids.count(_id) > 1]))

    if len(recurrent_ids) > 0:
        print(f"✘ ID check: Recurrent ids detected", recurrent_ids)
        return False

    print(f"✔ ID check: No recurrent ids detected")
    return True


def individual_ages(individuals: List[Individual]):
    list_of_ages = []
    for individual in individuals:
        list_of_ages.append(individual.age())
    print("List of individual age -", list_of_ages)
    return list_of_ages


def order_sibling_by_age(family: Family, individuals: List[Individual]):
    children = []
    for child in family.chil:
        children.append(next(ind for ind in individuals if ind.id == child))
    children.sort(key=lambda x: x.age(), reverse=True)
    print(
        f"Family[{family.id}] age of sibling in descending order " + " ".join([str(child.age()) for child in children]))
    return children


def firstCousinShouldNotMarry() -> List:
    """ check if parents of husband and spouse. If parents are siblings in each others families then first cousins.
    Return """

    listFam: List = families

    individualError: List = []

    for fam in listFam:
        if fam.husb != 'NA' and fam.wife != 'NA':
            husbParents: str = findParents(fam.husb, listFam)
            wifeParents: str = findParents(fam.wife, listFam)
            if husbParents and wifeParents:
                siblings: bool = checkIfSiblings(husbParents, wifeParents, listFam)
                if siblings:
                    individualError.append(fam)
    return individualError


def auntsAndUncle() -> List:
    listFam: List = families

    individualError: List = []
    for fam in listFam:
        if fam.husb != 'NA' and fam.wife != 'NA':
            husbParents: str = findParents(fam.husb, listFam)
            wifeParents: str = findParents(fam.wife, listFam)
            if husbParents and wifeParents:
                hSiblings: bool = checkIfSiblings(husbParents, fam, listFam)
                wSiblings: bool = checkIfSiblings(wifeParents, fam, listFam)
                if hSiblings:
                    individualError.append(fam)
                elif wSiblings:
                    individualError.append(fam)
    return individualError

def hasMultipleBirths(siblingDates):
    retValue = True
    datesDict = {}
    for d in siblingDates:
        if d in datesDict:
            datesDict[d] = datesDict.get(d) + 1
        else:  # if we did not find this date, we first check if we have date within day of already found dates
            found = False
            for d2 in datesDict:
                delta = d2 - d
                if (abs(delta.days) < 2):
                    datesDict[d2] = datesDict.get(d2) + 1
                    found = True
            if not found:
                datesDict[d] = 1
    for birthDate in datesDict.keys():
        if datesDict[birthDate] > 1:
            return birthDate.strftime('%d %b %Y')
    return False


# US 031

def isSingleAliveOver30():
    retValue = False
    age = -1
    alive = False
    spouse = []
    try:
        retValue = int(age) > 30 and alive and len(spouse) == 0
    except:
        retValue = False

    return retValue

