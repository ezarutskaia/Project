import argparse
from function import prediction
from function import model
from function import interval

# Установка парсера и описание аргументов
parser = argparse.ArgumentParser(description='Accident severity prediction')
parser.add_argument('t', type=int, help='Temperature')
parser.add_argument('h', type=int, help='Humidity')
parser.add_argument('p', type=int, help='Pressure')
parser.add_argument('v', type=int, help='Visibility')
parser.add_argument('st', type=int, help='Start_Time')
args = parser.parse_args()

dtc = model()

try:
    t = interval(args.t, -150, 150)
    h = interval(args.h, 0, 100)
    p = interval(args.p, 0, 100)
    v = interval(args.v, 0, 100)
    st = interval(args.st, 0, 23)
    result = prediction(dtc, t, h, p, v, st)
    print({"severity": str(result)})
except ValueError:
    print ("data entry error")




