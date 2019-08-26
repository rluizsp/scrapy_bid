import re


def find_numbers(string):
    numexp = re.compile(r'[-]?\d[\d,]*[\.]*[\,]?[\d{2}]*')  # optional - in front
    numbers = numexp.findall(string)
    numbers = [x.replace(',', '.') for x in numbers]

    return numbers


print(find_numbers('R$10.800,00'))