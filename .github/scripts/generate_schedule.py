from datetime import date, timedelta

# ======================
# CONFIG (EDIT THESE)
# ======================

SEMESTER_START = date(2026, 1, 5)   # any weekday
HOLIDAYS = {
    date(2026, 1, 20),
    date(2026, 2, 17),
}

TOTAL_CLASSES = 28
MEETING_DAYS = {1, 3}  # Tuesday=1, Thursday=3

README_PATH = "README.md"

# ======================
# MODULE SCHEDULE
# folder_name : [class_numbers where it applies]
# EDIT THIS SECTION
# ======================

MODULE_DAYS = {
    # examples
    "01-sql": [1,2,3,4,5,6,7],
    "02-erd-examples": [5,6,7,8,9,10],
    "03-functions": [3,4,5],
}

# ======================
# LOGIC
# ======================

def modules_for_class(class_number):
    """
    Returns list of folders relevant for a given class number.
    """
    return [
        folder
        for folder, days in MODULE_DAYS.items()
        if class_number in days
    ]


def first_class_day(start):
    d = start
    while d.weekday() not in MEETING_DAYS:
        d += timedelta(days=1)
    return d


dates = []
current = first_class_day(SEMESTER_START)

while len(dates) < TOTAL_CLASSES:
    if current.weekday() in MEETING_DAYS and current not in HOLIDAYS:
        dates.append(current)
    current += timedelta(days=1)


table_lines = [
    "| Class Date | Relevant Modules | Homework |",
    "|------------|------------------|----------|",
]

for i, d in enumerate(dates, start=1):

    modules = modules_for_class(i)

    module_links = " • ".join(
        f"[[{m[3:]}]]({m})" for m in modules
    )

    table_lines.append(
        f"| {d.strftime('%B %d, %Y')} | {module_links} | "
    )

table = "\n".join(table_lines)

# ======================
# WRITE TO README
# ======================

with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

start_tag = "<!-- SCHEDULE_START -->"
end_tag = "<!-- SCHEDULE_END -->"

before, rest = readme.split(start_tag)
_, after = rest.split(end_tag)

new_readme = (
    before
    + start_tag
    + "\n\n"
    + table
    + "\n\n"
    + end_tag
    + after
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)
