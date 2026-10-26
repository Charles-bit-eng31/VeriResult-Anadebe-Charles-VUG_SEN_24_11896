# Anadebe Charles 
# VUG/SEN/24/11896
SESSION = "2025/2026"
SEMESTER = "First"

COURSES = (
    ("COS101", "Introduction to Computing Sciences", 3),
    ("MTH101", "Elementary Mathematics I", 3),
    ("PHY101", "General Physics I", 2),
    ("GST111", "Communication in English", 2),
    ("STA111", "Descriptive Statistics", 3),
    ("CHM101", "General Chemistry I", 2),
)

# Grading scale: (minimum score, letter grade, grade point)
GRADE_SCALE = (
    (70, "A", 5),
    (60, "B", 4),
    (50, "C", 3),
    (45, "D", 2),
    (40, "E", 1),
    (0, "F", 0),
)

# Raw scores as received from lecturers, in the same order as COURSES.
# Key: matric number. Value: (student name, list of scores as text).
RAW_SCORES = {
    "VUG/SEN/25/1001": ("Adaeze Okafor", ["78", "65", "71", "58", "82", "69"]),
    "VUG/SEN/25/1002": ("Musa Ibrahim", ["45", "38", "52", "61", "47", "40"]),
    "VUG/SEN/25/1003": ("Tunde Bakare", ["91", "88", "76", "70", "95", "84"]),
    "VUG/SEN/25/1004": ("Ngozi Eze", ["55", "62", "abs", "49", "58", "51"]),
    "VUG/SEN/25/1005": ("Emeka Nwosu", ["33", "41", "29", "50", "36", "44"]),
    "VUG/SEN/25/1006": ("Aisha Bello", ["68", "72", "64", "77", "105", "66"]),
}


# Part A: Variables and Data Types

print("=== PART A ===")

institution = "Veritas University, Abuja"
level = 100
pass_mark = 40.0
is_open = True

# A list of (name, value) pairs lets one loop print all four variables.
# {value!r} shows the value with quotes for text (like 'Veritas...') and
# type(value).__name__ gives just the type name, e.g. str, int, float, bool.
variables = (
    ("institution", institution),
    ("level", level),
    ("pass_mark", pass_mark),
    ("is_open", is_open),
)
for name, value in variables:
    print(f"{name:<12}= {value!r:<28} type: {type(value).__name__}")

score_text = "78"          # the score as text (a str)
score = int(score_text)    # converted to a whole number (an int)
print(f"Remember : '{score_text}' + '2' = {score_text + '2'} but {score} + 2 = {score + 2}")

number_of_courses = len(COURSES)
total_units = 0
for course in COURSES:
    total_units += course[2]   # index 2 is the credit units
print(f"Courses this semester: {number_of_courses}, total units: {total_units}")

# The scores in RAW_SCORES cannot be added up as they are because they are
# stored as text (strings), so + would join them together ("78" + "65" gives
# "7865") instead of adding. Some are also not numbers at all (like "abs").


# Part B: Conditional Statements

print("\n=== PART B ===")


def clean_score(text):
    """Return the score as an int if it is valid (whole number 0-100), else None."""
    text = text.strip()         
    if not text.isdigit():      
        return None
    number = int(text)
    if number < 0 or number > 100:
        return None
    return number


def grade_score(score):
    """Return (letter, grade_point) for a valid score using GRADE_SCALE."""
    for minimum, letter, point in GRADE_SCALE:
        if score >= minimum:   
            return (letter, point)


def classify(gpa):
    """Return the class standing for a GPA."""
    if gpa >= 4.50:
        return "First Class"
    elif gpa >= 3.50:
        return "Second Class Upper"
    elif gpa >= 2.40:
        return "Second Class Lower"
    elif gpa >= 1.50:
        return "Third Class"
    elif gpa >= 1.00:
        return "Pass"
    else:
        return "Fail"


for raw in ["78", " 45 ", "abs", "105", "-3", "39"]:
    cleaned = clean_score(raw)
    if cleaned is None:
        print(f"{raw!r} -> None invalid")
    else:
        print(f"{raw!r} -> {cleaned} {grade_score(cleaned)}")

for test_gpa in [4.62, 3.5, 2.39, 1.2, 0.8]:
    print(f"{test_gpa} -> {classify(test_gpa)}")



# Part C: Loops

print("\n=== PART C ===")

problems = []         # will hold (matric, course code, raw text) for bad scores
cleaned_by_student = {}   # matric -> list of cleaned scores (None where invalid)

for matric, (student_name, score_texts) in RAW_SCORES.items():
    cleaned_list = []
    # zip pairs each course with its score text, in order
    for course, text in zip(COURSES, score_texts):
        course_code = course[0]
        value = clean_score(text)
        cleaned_list.append(value)          # keeps None for invalid scores
        if value is None:
            problems.append((matric, course_code, text))
    cleaned_by_student[matric] = cleaned_list

print("Invalid entries:", problems)



# Part D: Functions



def compute_gpa(scores):
    """Return (gpa, units_taken, carryovers) for a list of cleaned scores."""
    total_points = 0
    units_taken = 0
    carryovers = []
    for course, score in zip(COURSES, scores):
        code, title, units = course
        if score is None:                  
            continue
        letter, point = grade_score(score)
        total_points += units * point
        units_taken += units
        if letter == "F":                 
            carryovers.append(code)
    if units_taken == 0:
        return (0.0, 0, carryovers)
    return (round(total_points / units_taken, 2), units_taken, carryovers)


def build_records(raw):
    """Build the records dictionary and the list of invalid entries from raw scores."""
    records = {}
    problems = []
    for matric, (student_name, score_texts) in raw.items():
        cleaned_list = []
        for course, text in zip(COURSES, score_texts):
            value = clean_score(text)
            cleaned_list.append(value)
            if value is None:
                problems.append((matric, course[0], text))
        gpa, units_taken, carryovers = compute_gpa(cleaned_list)
        records[matric] = {
            "name": student_name,
            "scores": cleaned_list,
            "gpa": gpa,
            "units": units_taken,
            "carryovers": carryovers,
            "class": classify(gpa),
        }
    return records, problems


records, problems = build_records(RAW_SCORES)
for matric, rec in records.items():
    print(f"{matric} {rec['name']} GPA {rec['gpa']:.2f} units {rec['units']} "
          f"{rec['carryovers']} {rec['class']}")



# Part E: Lists and List Methods

print("\n=== PART E ===")

codes = [course[0] for course in COURSES]
print("E1:", codes)

codes.append("CSC102")
print("E2:", codes)

codes.insert(0, "GST101")
print("E3:", codes)

codes.remove("CSC102")
print("E4:", codes)

removed_code = codes.pop()
print(f"E5: {removed_code} | {codes}")

print(f"E6: {sorted(codes)} | original: {codes}")

print("E7:", codes.index("MTH101"), codes.count("COS101"), len(codes))

print("E8:", codes[:3], codes[::-1])

adaeze_scores = list(records["VUG/SEN/25/1001"]["scores"])   # a copy of her scores
adaeze_scores.sort(reverse=True)
print(f"E9: {adaeze_scores} | highest: {adaeze_scores[0]} | lowest: {adaeze_scores[-1]}")



# Part F: Tuples and Tuple Methods

print("\n=== PART F ===")

first = COURSES[0]
code, title, units = first        # unpacking into three variables
print(f"F1: {code} | {title} | {units}")

print("F2:", COURSES[-1][1])

try:
    first[2] = 4
except TypeError as error:
    print("F3: TypeError:", error)

unit_values = tuple(course[2] for course in COURSES)
print("F4:", unit_values, unit_values.count(3), unit_values.index(2))

result = grade_score(64)
print("F5:", result, type(result).__name__)

letters = tuple(row[1] for row in GRADE_SCALE)
print("F6:", letters, "E" in letters)

# COURSES and GRADE_SCALE are tuples because they are fixed records that the
# program should never change by accident. Tuples are immutable, so nothing
# can add, remove or edit a course or a grade boundary while the program runs.



# Part G: Dictionaries and Dictionary Methods

print("\n=== PART G ===")

print("G1:", len(records), list(records.keys())[:2])

found = records.get("VUG/SEN/25/1003", {"name": "Not found"})["name"]
missing = records.get("VUG/SEN/25/9999", {"name": "Not found"})["name"]
print(f"G2: {found} | {missing}")

RAW_SCORES.update({
    "VUG/SEN/25/1007": ("Chidi Obi", ["60", "58", "63", "70", "55", "49"])
})
records, problems = build_records(RAW_SCORES)
chidi = records["VUG/SEN/25/1007"]
print(f"G3: {len(records)} {chidi['gpa']:.2f} {chidi['class']}")

withdrawn = RAW_SCORES.pop("VUG/SEN/25/1007")     # pop returns (name, scores)
records.pop("VUG/SEN/25/1007")
print(f"G4: {withdrawn[0]} withdrawn | {len(records)} students left")

for matric, rec in records.items():
    if rec["carryovers"]:      # an empty list is False, so this means "has carry-overs"
        print(f"G5: {matric} {rec['name']} {rec['carryovers']}")



# Part H: Putting It Together



def result_slip(matric, record):
    """Print a neat result slip for one student."""
    line = "-" * 62
    print("=" * 62)
    print(f"{institution.upper()} | {SESSION} {SEMESTER} Semester")
    print()
    print(f"Name: {record['name']:<24} Matric No: {matric}")
    print(line)
    print(f"{'Code':<7}{'Course title':<36}{'Unit':>4}{'Score':>7}{'Grade':>7}")
    for course, score in zip(COURSES, record["scores"]):
        course_code, course_title, units = course
        if score is None:
            shown_score, grade = "--", "ABS"
        else:
            shown_score, grade = score, grade_score(score)[0]
        print(f"{course_code:<7}{course_title:<36}{units:>4}{shown_score:>7}{grade:>7}")
    print(line)
    print(f"Units taken: {record['units']}  GPA: {record['gpa']:.2f}  "
          f"Class: {record['class']}")
    if record["carryovers"]:
        print("Carry-over courses:", ", ".join(record["carryovers"]))
    else:
        print("Carry-over courses: None")
    print("=" * 62)


def class_summary(records):
    """Print the class ranking, average GPA, carry-over count, grade distribution
    and the students grouped by class standing."""
    print("CLASS RANKING")
    ranking = sorted(records.items(), key=lambda item: item[1]["gpa"], reverse=True)
    for position, (matric, rec) in enumerate(ranking, start=1):
        print(f"{position}. {rec['name']:<13} {matric} GPA {rec['gpa']:.2f} {rec['class']}")

    total_gpa = 0
    for rec in records.values():
        total_gpa += rec["gpa"]
    print(f"Class average GPA: {total_gpa / len(records):.2f}")

    no_carryover = 0
    for rec in records.values():
        if not rec["carryovers"]:
            no_carryover += 1
    print(f"Students with no carry-over: {no_carryover} of {len(records)}")

    distribution = {}
    for rec in records.values():
        for score in rec["scores"]:
            if score is not None:
                letter = grade_score(score)[0]
                distribution[letter] = distribution.get(letter, 0) + 1
    distribution = dict(sorted(distribution.items()))     # A to F order
    print("Grade distribution:", distribution)

    by_class = {}
    for rec in records.values():
        by_class.setdefault(rec["class"], []).append(rec["name"])
    print("Students by class standing:", by_class)




def menu():
    """Show the menu and respond to the user's choices until they enter 0."""
    while True:
        print("\n1. Result slip 2. Class ranking and summary 0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        elif choice == "1":
            matric = input("Enter matric number: ").strip()
            if matric in records:
                result_slip(matric, records[matric])
            else:
                print("No student with that matric number.")
        elif choice == "2":
            class_summary(records)
        else:
            print("Invalid choice, try again.")


print("\n=== PART H ===")
menu()
