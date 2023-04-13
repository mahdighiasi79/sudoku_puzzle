import numpy as np

Sudoku = [[[[-1] * 3] * 3] * 3] * 3
Domains = [[[[[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 3] * 3] * 3] * 3


def Domain(sudoku, variable):
    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    row1 = variable[0]
    column1 = variable[1]

    row2 = variable[2]
    column2 = variable[3]

    for i in range(3):
        for j in range(3):

            value = sudoku[row1][i][row2][j]
            if value != -1 and value in domain:
                domain.remove(value)

            value = sudoku[i][column1][j][column2]
            if value != -1 and value in domain:
                domain.remove(value)

            value = sudoku[row1][column1][i][j]
            if value != -1 and value in domain:
                domain.remove(value)

    return domain


def SelectUnassignedVariable(sudoku):
    biggest_heuristic_value = -1
    result = [-1, -1, -1, -1]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    variable = [i, j, k, l]
                    if sudoku[i][j][k][l] == -1:
                        heuristic_value = 9 - len(Domain(sudoku, variable))
                        if heuristic_value > biggest_heuristic_value:
                            biggest_heuristic_value = heuristic_value
                            result = variable
    return result


def LeastConstrainingHeuristic(domains, variable, value):
    result = 0

    row1 = variable[0]
    column1 = variable[1]

    row2 = variable[2]
    column2 = variable[3]

    for i in range(3):
        for j in range(3):

            domain = domains[row1][i][row2][j]
            if value in domain:
                result += np.log(len(domain) - 1) * 10
            else:
                result += np.log(9) * 10

            domain = domains[i][column1][j][column2]
            if value in domain:
                result += np.log(len(domain) - 1) * 10
            else:
                result += np.log(9) * 10

            domain = domains[row1][column1][i][j]
            if value in domain:
                result += np.log(len(domain) - 1) * 10
            else:
                result += np.log(9) * 10

    return result


def f(e):
    return e[0]


def OrderDomainValues(variable, domains):
    row1 = variable[0]
    column1 = variable[1]

    row2 = variable[2]
    column2 = variable[3]

    domain = domains[row1][column1][row2][column2]
    heuristic_values = []

    for i in range(len(domain)):
        value = domain[i]
        heuristic_value = LeastConstrainingHeuristic(domains, variable, value)
        heuristic_values.append([heuristic_value, i])

    heuristic_values.sort(key=f, reverse=True)
    return heuristic_values


def Inference(domains, variable, value):
    row1 = variable[0]
    column1 = variable[1]

    row2 = variable[2]
    column2 = variable[3]

    for i in range(3):
        for j in range(3):

            if value in domains[row1][i][row2][j]:
                domains[row1][i][row2][j].remove(value)
                if len(domains[row1][i][row2][j]) == 0:
                    return None

            if value in domains[i][column1][j][column2]:
                domains[i][column1][j][column2].remove(value)
                if len(domains[i][column1][j][column2]) == 0:
                    return None

            if value in domains[row1][column1][i][j]:
                domains[row1][column1][i][j].remove(value)
                if len(domains[row1][column1][i][j]) == 0:
                    return None


def complete(sudoku):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if sudoku[i][j][k][l] == -1:
                        return False
    return True


if __name__ == '__main__':
    print(np.log(np.e))
