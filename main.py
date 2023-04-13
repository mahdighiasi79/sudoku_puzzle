import numpy as np
import copy

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

    for value in domain:
        heuristic_value = LeastConstrainingHeuristic(domains, variable, value)
        heuristic_values.append([heuristic_value, value])

    heuristic_values.sort(key=f, reverse=True)
    return heuristic_values


def Consistent(sudoku, variable, value):
    row1 = variable[0]
    column1 = variable[1]

    row2 = variable[2]
    column2 = variable[3]

    for i in range(3):
        for j in range(3):

            if value == sudoku[row1][i][row2][j]:
                return False

            if value == sudoku[i][column1][j][column2]:
                return False

            if value == sudoku[row1][column1][i][j]:
                return False
    return True


def Inference(domains, variable, value):
    row1 = variable[0]
    column1 = variable[1]

    row2 = variable[2]
    column2 = variable[3]

    for i in range(3):
        for j in range(3):

            if value in domains[row1][i][row2][j]:
                if len(domains[row1][i][row2][j]) == 1:
                    return None
                domains[row1][i][row2][j].remove(value)

            if value in domains[i][column1][j][column2]:
                if len(domains[i][column1][j][column2]) == 1:
                    return None
                domains[i][column1][j][column2].remove(value)

            if value in domains[row1][column1][i][j]:
                if len(domains[row1][column1][i][j]) == 1:
                    return None
                domains[row1][column1][i][j].remove(value)


def complete(sudoku):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if sudoku[i][j][k][l] == -1:
                        return False
    return True


def BackTrack(sudoku, domains):
    if complete(sudoku):
        return sudoku

    variable = SelectUnassignedVariable(sudoku)

    for values in OrderDomainValues(variable, domains):
        value = values[1]

        if Consistent(sudoku, variable, value):
            sudoku_copy = copy.deepcopy(sudoku)
            domains_copy = copy.deepcopy(domains)

            sudoku_copy[variable[0]][variable[1]][variable[2]][variable[3]] = value

            if Inference(domains_copy, variable, value) is not None:
                result = BackTrack(sudoku_copy, domains_copy)
                if result is not None:
                    return result

    return None


def GetSudoku():
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    value = input()
                    if value != " ":
                        Sudoku[i][j][k][l] = int(value)


if __name__ == '__main__':
    GetSudoku()
    print(BackTrack(Sudoku, Domains))
