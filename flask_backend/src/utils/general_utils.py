from datetime import datetime


class GeneralUtils:
    @staticmethod
    def calculate_three_previous_months(date):
        curr_date = datetime.strptime(date, '%m-%Y')

        prev_moth = curr_date.month - 2
        prev_year = curr_date.year

        if prev_moth < 1:
            prev_moth += 12
            prev_year -= 1

        prev_date = datetime(prev_year, prev_moth, 1)

        prev_date_str = prev_date.strftime('%m/%Y')

        return prev_date_str, curr_date.strftime('%m/%Y')
