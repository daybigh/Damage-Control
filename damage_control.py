from __future__ import annotations
from typing import *


class Year:
    """A collection of all of my courses.
    === Attributes ===

    year: The current school year

    courses: A list containing all the courses I took in the year

    average: The average grade for the year.

    max: The maximum possible average for the year
    """

    courses: Optional[list[Course]]
    average: Optional[float]

    def __init__(self, year: str) -> None:
        self.year = year
        self.courses = None
        self.average = None
        self.max = None

    def read_txt(self, f: TextIO) -> None:
        courses = []
        for line in f:
            lst = line.split(',')
            for i, e in enumerate(lst):
                lst[i] = lst[i].strip()

            course = Course(str(lst[0]), str(lst[1]))
            for assignment in lst[2:]:
                temp = assignment.split(":")
                course.mark_assignment(str(temp[0]), float(temp[1]),
                                       float(temp[2]))
            courses.append(course)

        self.courses = courses

        count = 0
        mark = 0
        max_ = 0
        for course in self.courses:
            if course.credit == "h":
                mark += course.total
                max_ += course.max
                count += 1
            elif course.credit == 'y':
                mark += (2 * course.total)
                max_ += (2 * course.max)
                count += 2

        self.average = mark / count
        self.max = max_ / count

    def __str__(self):
        temp = f"REPORT FOR {self.year}:\n\n"

        for course in self.courses:
            temp += course.__str__()

        temp += f"My current year average is {self.average}%\n"
        temp += f"My max possible year average is {self.max}%"
        return temp


class Course:
    """A course in my uni schedule.

    === Attributes ===

    name: The course title.

    credit: shows if the year is half credit or full credit

    assignments: a dictionary of assignments for the course. The key is the
    name of the assignment and the values are a list containing a float of
    the weight of the assignment, and a float of the mark obtained.

    max: The maximum possible grade in the course

    total: the total grade I have in the course currently

    === Private Attributes ===

    _achieved: The combined total of all my marks

    _weight: The combined weight of all the released marks multiplied by 100

    """

    name: str
    credit: str
    assignments: dict[str, List[float, Optional[float]]]
    total: Optional[float]
    _weight: Optional[float]
    _achieved: Optional[float]
    max: Optional[float]

    def __init__(self, name: str, credit: str) -> None:
        self.name = name
        self.assignments = {}
        self.total = None
        self._weight = None
        self._achieved = None
        self.max = None
        self.credit = credit

    def mark_assignment(self, assignment: str, mark: float, weight: float) ->\
            None:
        self.assignments[assignment] = [weight, mark]
        self._weight = 0
        self._achieved = 0

        for (key, value) in self.assignments.items():
            self._weight += value[0]
            self._achieved += value[1] * value[0]
        self.total = self._achieved / self._weight
        self.max = (self._achieved + 100 * (100 - self._weight)) / 100

    def __str__(self):
        temp = f"{self.name} grade report:\n"
        if self.credit == "h":
            temp += f"{self.name} is worth 0.5 credits \n"
        elif self.credit == 'y':
            temp += f"{self.name} is worth 1.0 credits \n"
        for (key, value) in self.assignments.items():
            temp += f"{key} is worth {value[0]}% and I got a {value[1]}% " \
                    f"on it\n"
        if self.total is not None:
            temp += f"I currently have a {self.total}% in {self.name}\n"
        else:
            temp += f"I don't have any marks in {self.name}\n"

        temp += f"Currently, {self._weight}%/100% of the course weight has " \
                f"been released\n"
        temp += f"The maximum possible grade I could get now in {self.name} " \
                f"is a {self.max}% \n\n"

        return temp


def main():
    year = Year("Year of the Arbus")

    with open("damage_control.txt") as f:
        year.read_txt(f)

    print(year)


if __name__ == '__main__':
    main()



