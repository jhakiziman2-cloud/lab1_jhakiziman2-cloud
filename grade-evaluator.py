#!/usr/bin/python3
import csv
import sys
import os

def load_csv_data():
    filename = input("Enter the name of the CSV file to process : ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Checking if file is empty
            if reader.fieldnames is None:
                print("Error: CSV file is empty.")
                sys.exit(1)

            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    print("\nProcessing Grades ...")

    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    formative_score = 0
    summative_score = 0

    failed_formatives = []

    # Validation + Calculation 
    for item in data:
        score = item['score']
        weight = item['weight']
        group = item['group']

        #  a)Score validation
        if score < 0 or score > 100:
            print(f"Invalid score in {item['assignment']}")
            sys.exit(1)

        total_weight += weight

        if group == "Formative":
            formative_weight += weight
            formative_score += (score * weight) / 100

            if score < 50:
                failed_formatives.append(item)

        elif group == "Summative":
            summative_weight += weight
            summative_score += (score * weight) / 100

    # b)Weight validation
    if total_weight != 100:
        print("Error: Total weight must equal 100.")
        sys.exit(1)

    if formative_weight != 60 or summative_weight != 40:
        print("Error: Formative must be 60 and Summative must be 40.")
        sys.exit(1)

    # c)GPA Calculation
    total_grade = formative_score + summative_score
    GPA = (total_grade / 100) * 5.0

    # d)Pass/Fail
    formative_percentage = (formative_score / formative_weight) * 100
    summative_percentage = (summative_score / summative_weight) * 100

    if formative_percentage >= 50 and summative_percentage >= 50:
        status = "PASSED"
    else:
        status = "FAILED"

    #  e)Resubmission Logic
    resubmissions = []
    if failed_formatives:
        max_weight = max(item['weight'] for item in failed_formatives)
        for item in failed_formatives:
            if item['weight'] == max_weight:
                resubmissions.append(item['assignment'])

    # OUTPUT 
    print(f"Formative Score: {round(formative_score,2)} / 60")
    print(f"Summative Score: {round(summative_score,2)} / 40")
    print(f"Total Grade: {round(total_grade,2)} / 100")
    print(f"GPA: {round(GPA,3)}")
    print(f"Status: {status}")

    if resubmissions:
        print("Available for resubmission:", ", ".join(resubmissions))
    else:
        print("No resubmissions needed.")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
