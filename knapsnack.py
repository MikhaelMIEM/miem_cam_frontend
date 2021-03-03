def knapSack(students, data, n):
    '''
    0 - aud
    1 - qual
    2 - cap
    '''
    if n == 0 or students == 0:
        return []
    if (data[n-1][2] > students):
        return knapSack(students, data, n-1)
    else:
        next_knapsack = knapSack(students - data[n-1][2], data, n-1)
        if data[n-1][1] + sum(i[1] for i in next_knapsack) > sum(i[1] for i in next_knapsack):
            return [data[n-1], *next_knapsack]
        else:
            return knapSack(students, data, n-1)

auditories = [520, 630, 710]
qualityes = [60, 100, 120]
capacities = [10, 20, 30]
data = [(auditories[i], qualityes[i], capacities[i]) for i in range(len(auditories))]
students = 30
print(knapSack(students, data, len(qualityes)))
