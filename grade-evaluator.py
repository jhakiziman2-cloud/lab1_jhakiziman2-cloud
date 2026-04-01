#!/usr/bin/python3
import csv
import sys
import os


def load_csv_data():

    filename = input("Enter the name of the CSV file to process: ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        if not rows:
            print("Error: The CSV file is empty. No grades to process.")
            sys.exit(1)

        for row in rows:
            assignments.append({
                'assignment': row['assignment'].strip(),
                'group': row['group'].strip(),
                'score': float(row['score']),
                'weight': float(row['weight'])
            })
        return assignments

    except KeyError as e:
        print(f"Error: Missing expected column in CSV: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid numeric value in CSV: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):

    print("\n  Processing Grades...\n")

    #  a) Score validation (0–100)
    invalid_scores = [a for a in data if not (0 <= a['score'] <= 100)]
    if invalid_scores:
        for a in invalid_scores:
            print(f"  X Invalid score {a['score']} for '{a['assignment']}' (must be 0-100).")
        sys.exit(1)
    print("OK  All scores are within the valid range (0-100).")

    #  b) Weight validation
    formatives = [a for a in data if a['group'].lower() == 'formative']
    summatives = [a for a in data if a['group'].lower() == 'summative']

    total_weight     = sum(a['weight'] for a in data)
    formative_weight = sum(a['weight'] for a in formatives)
    summative_weight = sum(a['weight'] for a in summatives)

    errors = []
    if total_weight != 100:
        errors.append(f"  X Total weight is {total_weight}, expected 100.")
    if formative_weight != 60:
        errors.append(f"  X Formative weight is {formative_weight}, expected 60.")
    if summative_weight != 40:
        errors.append(f"  X Summative weight is {summative_weight}, expected 40.")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print(" The OK  Weight for  validation passed  (Total=100 | Formative=60 | Summative=40).\n")

    # c) Final grade & GPA
    for a in data:
        a['weighted_score'] = (a['score'] / 100) * a['weight']

    formative_earned = sum(a['weighted_score'] for a in formatives)
    summative_earned = sum(a['weighted_score'] for a in summatives)
    total_earned     = formative_earned + summative_earned

    # Percentage within each category bucket
    formative_pct = (formative_earned / 60) * 100
    summative_pct = (summative_earned / 40) * 100

    gpa = (total_earned / 100) * 5.0

    #  d) Pass / Fail
    passed = formative_pct >= 50 and summative_pct >= 50

    # e) Resubmission logic
    failed_formatives = [a for a in formatives if a['score'] < 50]

    resubmit_candidates = []
    if failed_formatives:
        max_weight = max(a['weight'] for a in failed_formatives)
        resubmit_candidates = [a for a in failed_formatives if a['weight'] == max_weight]

    # f) Print results
    print("=" * 60)
    print(f"{'GRADE REPORT':^60}")
    print("=" * 60)

    print(f"\n{'Assignment':<38} {'Score':>5}  {'Weight':>6}  {'Final Wt':>8}")
    print("-" * 62)

    for a in formatives:
        print(f"  {a['assignment']:<36} {a['score']:>5.1f}  {a['weight']:>6.0f}  {a['weighted_score']:>8.2f}")
    print(f"  {'Formatives (60)':<36} {'':>5}  {'':>6}  {formative_earned:>8.2f}")

    print()
    for a in summatives:
        print(f"  {a['assignment']:<36} {a['score']:>5.1f}  {a['weight']:>6.0f}  {a['weighted_score']:>8.2f}")
    print(f"  {'Summatives (40)':<36} {'':>5}  {'':>6}  {summative_earned:>8.2f}")

    print()
    print(f"  {'Total Grade':<36} {total_earned:>28.2f}")
    print(f"  {'GPA (out of 5.0)':<36} {gpa:>28.3f}")
    print()
    print(f"  Formative category score : {formative_pct:.2f}%  (need >= 50%)")
    print(f"  Summative category score : {summative_pct:.2f}%  (need >= 50%)")
    print()

    status = "PASSED" if passed else "FAILED"
    print(f"  Status : {status}")

    print()
    if resubmit_candidates:
        names = ", ".join(a['assignment'] for a in resubmit_candidates)
        print(f"  Available for resubmission : {names}")
    else:
        if not passed:
            print("  Available for resubmission : None (no failed formative assignments).")
        else:
            print("  Available for resubmission : None (student passed).")

    print("=" * 60)


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)

