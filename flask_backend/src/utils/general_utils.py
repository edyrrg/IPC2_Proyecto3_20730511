from datetime import datetime


class GeneralUtils:
    @staticmethod
    def calculate_three_previous_months(date):
        curr_date = datetime.strptime(date, '%m-%Y')

        prev_moth = curr_date.month - 1
        prev_year = curr_date.year

        # moth previous
        if prev_moth < 1:
            prev_moth += 12
            prev_year -= 1

        # last month
        last_month = curr_date.month - 2
        last_year = curr_date.year
        if last_month < 1:
            last_month += 12
            last_year -= 1

        prev_date = datetime(prev_year, prev_moth, 1)

        prev_date_str = prev_date.strftime('%m/%Y')

        last_date = datetime(last_year, last_month, 1)

        last_date_str = last_date.strftime('%m/%Y')

        return curr_date.strftime('%m/%Y'), prev_date_str, last_date_str
