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

LINK_TEMPLATE = "{num:02d}_"

README_PATH = "README.md"

# ======================
# LOGIC
# ======================

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
    "| Class | Date | Materials |",
    "|-------|------|-----------|",
]

for i, d in enumerate(dates, start=1):
    link = LINK_TEMPLATE.format(num=i)
    table_lines.append(
        f"| {i} | {d.strftime('%B %d, %Y')} | [{link}]({link}) |"
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
