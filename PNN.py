from random import uniform
from math import exp

teach_f_name = "teach_PNN.txt"
gaus = 0.3
maximums = None
network = None

# Neuron
class activation_functions():
    """docstring for activation_functions"""
    def PNN(self, data, weights):
        result = 0
        for i in range(len(data)):
            result+= exp(-((weights[i] - data[i])**2)/gaus**2)
            '''print("weights: ", weights[i])
            print("data[i]: ", data[i])
            print("gaus: ", gaus**2)
            print("((weights[i] - data[i])**2)/gaus**2", ((weights[i] - data[i])**2)/gaus**2)
            print("Exp: ", 1/2.71828182845904523536028747135266249775724709369995**(((weights[i] - data[i])**2)/gaus**2))
            print(result)'''
        return result/len(data)


    def sum(self, data, weights):
        return sum(data)/len(data)

class neu(activation_functions):
    def __init__(self, signals, image = None, W = None, activation_f = "sigmoid", w_random = 0.1, w_delta = 0.05):
        self.image = image
        if W is None:
            self.W = [uniform(w_random - w_delta, w_random + w_delta) for i in range(signals)]
        elif W == False:
            self.W = False
        else:
            self.W = W
        self.sigma = 0
        if activation_f == "PNN":
            self.activation_f = self.PNN
        elif activation_f == "sum":
            self.activation_f = self.sum


    def out(self, signals:list):
        self.y_out = self.activation_f(signals, self.W)
        return self.y_out


# Network

class PNN():
    def __init__(self, data, f="sigmoid"):
        self.images = {} #Считаю количество нейронов одного образа
        for row in data:
            if row[1] not in self.images:
                self.images[row[1]] = 1
            else:
                self.images[row[1]] += 1
        self.network = [[neu(data[i][0], image = data[i][1], activation_f="PNN", W=data[i][0]) for i in range(len(data))]] \
                       + [[neu(k, image = i, activation_f="sum", W=False) for i, k in self.images.items()]]


    def out(self, signals: list):
        self.images_out = {}
        for sum_neu in self.network[1]:
            image_neu_out = [] #Храню выходы с шара образов
            for image_neu in self.network[0]:
                if image_neu.image == sum_neu.image: #Ищу нейроны отвечающие за образ данного сумматора
                    image_neu_out.append(image_neu.out(signals)) #Сохраняю выход нейрона с шара образов
            #print(image_neu_out)
            self.images_out[sum_neu.image] = sum_neu.out(image_neu_out) #Сохраняю значение сумматора для образа
        #print(self.images_out)
        for i in self.images_out.items():
            self.y_out = i
            break
        for image in self.images_out.items(): #Перебираю все образы и значение сумматоров
            if image[1] > self.y_out[1]: #При совпадении перезаписываю выходной класс образа
                self.y_out = image
        return self.y_out


    def learn(self, y_out, y_pr):
        pass

def teach():
    t_data = []
    global maximums
    global network
    with open(teach_f_name, 'r') as file:
        for line in file:
            X = line.split(",") #считывание списка сигналов
            y = X[len(X)-1] #Сохранение ожидаемого
            
            X = list(map(float, X[:len(X)-2])) # Удаление ожидаеммого из списка сигналов
            t_data.append((X, y)) #[([x1, x2], y), ([x1, x2], y)] - формат сохрнения данных

    maximums = [0 for i in range(len(t_data))]
    for row in range(len(t_data)): #нахождение максимумов
        for col in range(len(t_data[row][0])):
            if t_data[row][0][col] > maximums[col]:
                maximums[col] = t_data[row][0][col]


    for row in range(len(t_data)): #нормализация
        for col in range(len(t_data[row][0])):
            if maximums[col] != 0:
                t_data[row][0][col] /= maximums[col]

    network = PNN(t_data)

def recognise(data):
    X = list(map(float, X[:len(X)-1])) #Считывание данных пробного примера
    #Нормализация
    for i in range(len(X)):
        if maximums[i] != 0:
            X[i] /= maximums[i]
    y_out = network.out(X)
    return y_out

teach()
print([1254, 1124.14])