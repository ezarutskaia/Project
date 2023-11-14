import argparse
from function import Prediction
from function import Model
from function import interval

# Установка парсера и описание аргументов
parser = argparse.ArgumentParser(description='Accident severity prediction')
parser.add_argument('T', type=int, help='Temperature')
parser.add_argument('H', type=int, help='Humidity')
parser.add_argument('P', type=int, help='Pressure')
parser.add_argument('V', type=int, help='Visibility')
parser.add_argument('ST', type=int, help='Start_Time')
args = parser.parse_args()
#print(args.T)

knc = Model()

try:
        T = interval(args.T, -150, 150)
        H = interval(args.H, 0, 100)
        P = interval(args.P, 0, 100)
        V = interval(args.V, 0, 100)
        ST = interval(args.ST, 0, 23)
        result = Prediction(knc, T, H, P, V, ST)
        print({"severity": str(result)})
except ValueError:
        print ("data entry error")




