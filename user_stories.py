""" Implement user stories for GEDCOM parser

    date: 30-Sep-2020
    python: v3.8.4
"""

from typing import List, Dict
from datetime import datetime, timedelta
from models import Individual, Family


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


# User story 14
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


# User story 13
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


def checkBigamy(family: Dict):
    """Method that checks bigamy in the given gedcom data if yes then it pops and update data with no bigamy"""
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



