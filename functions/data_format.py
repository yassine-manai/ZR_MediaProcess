from datetime import datetime
import random

def date_format(date_str: str) -> str:

    date_formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d:%m:%Y"]

    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Date format for '{date_str}' is not supported")


def generate_unique_random(range):
    if not range:
        raise ValueError("No more unique numbers to generate.")
    
    number = random.choice(list(range))
    
    range.remove(number)
    return number