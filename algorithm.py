from fitting import fitting

def smooth_in_section(xx, data, deviation, order):
    f = fitting(xx, data)
    f.fitting(order)
    for index in range(len(xx)):
        if data[index] - f.val[index] > deviation * f.ER2:
            data[index] = f.val[index] + deviation * f.ER2
        elif f.val[index] - data[index] > deviation * f.ER2:
            data[index] = f.val[index] - deviation * f.ER2
    #data += 1