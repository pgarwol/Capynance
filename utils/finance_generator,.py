from datetime import datetime, timedelta
import random as rnd
from typing import List


def randomize_income_and_outcome() -> float:
    income = rnd.random() * 1_000
    outcome = income + 1
    while income < outcome:
        outcome = rnd.random() * 1_000

    return income, outcome


def get_days_in_month(year: int, month: int):
    # Find the first day of the next month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)

    # Find the last day of the current month
    last_day_of_month = next_month - timedelta(days=1)

    return [datetime(year, month, day) for day in range(1, last_day_of_month.day + 1)]


def generate_income_outcome_data(year: int, months: List[int]) -> dict:
    output = {}
    for month in months:
        days = get_days_in_month(year, month)
        for day in days:
            income, outcome = randomize_income_and_outcome()
            output[day.strftime("%d-%m-%Y")] = {
                "in": f"{income:.2f}",
                "outcome": f"{outcome:.2f}",
            }
    return output


# Example usage:


if __name__ == "__main__":
    in_out_data = generate_income_outcome_data(2024, [6])
    print(in_out_data)
