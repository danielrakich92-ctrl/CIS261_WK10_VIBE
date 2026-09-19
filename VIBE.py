#Danny Rakich
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator."""

FILE_NAME = "student_grades.txt"


class Student:
	"""Store a student's identifying information and calculated grade."""

	def __init__(self, name, student_id, test1, test2, test3):
		self.name = name
		self.student_id = student_id
		self.test_scores = [float(test1), float(test2), float(test3)]
		self.average = sum(self.test_scores) / len(self.test_scores)
		self.grade = self.calculate_grade()

	def calculate_grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		scores = "|".join(f"{score:.2f}" for score in self.test_scores)
		return f"{self.name}|{self.student_id}|{scores}|{self.average:.2f}|{self.grade}\n"


def prompt_for_text(prompt):
	while True:
		value = input(prompt).strip()
		if value:
			return value
		print("This field cannot be empty.")


def prompt_for_score(test_number):
	while True:
		try:
			score = float(input(f"Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Enter a score from 0 to 100.")
		except ValueError:
			print("Enter a valid number.")


def add_student(students):
	print("\nAdd Student")
	name = prompt_for_text("Name: ")
	student_id = prompt_for_text("Student ID: ")
	test_scores = [prompt_for_score(number) for number in range(1, 4)]
	student = Student(name, student_id, *test_scores)
	students.append(student)
	print(f"\nAdded {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	headers = ["Name", "ID", "Test 1", "Test 2", "Test 3", "Average", "Grade"]
	rows = []
	for student in students:
		rows.append([
			student.name,
			student.student_id,
			*(f"{score:.2f}" for score in student.test_scores),
			f"{student.average:.2f}",
			student.grade,
		])
	widths = [max(len(header), *(len(row[index]) for row in rows)) for index, header in enumerate(headers)]
	separator = "-+-".join("-" * width for width in widths)
	print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
	print(separator)
	for row in rows:
		print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def display_statistics(students):
	if not students:
		print("\nNo student records found.")
		return

	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	class_average = sum(student.average for student in students) / len(students)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average: {lowest.average:.2f} ({lowest.name})")
	print(f"Class average: {class_average:.2f}")


def search_student(students):
	search_name = prompt_for_text("\nEnter student name to search: ").casefold()
	matches = [student for student in students if search_name in student.name.casefold()]
	if not matches:
		print("No matching students found.")
		return
	display_students(matches)


def save_students(students):
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		print(f"Saved {len(students)} student record(s) to {FILE_NAME}.")
		return True
	except OSError as error:
		print(f"Could not save student records: {error}")
		return False


def load_students():
	students = []
	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				values = line.rstrip("\n").split("|")
				if len(values) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				try:
					students.append(Student(values[0], values[1], values[2], values[3], values[4]))
				except (TypeError, ValueError):
					print(f"Skipped invalid record on line {line_number}.")
		print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")
	except FileNotFoundError:
		print(f"No {FILE_NAME} file found. Starting with an empty record list.")
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def display_menu():
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("Press ESC or enter 6 to exit")


def main():
	students = load_students()
	while True:
		display_menu()
		choice = input("Choose an option: ")
		if choice == "\x1b" or choice == "6":
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
			save_students(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid choice. Select an option from the menu.")


if __name__ == "__main__":
	main()

