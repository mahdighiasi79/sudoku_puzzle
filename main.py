import numpy as np
import copy

Sudoku = [[[[-1] * 3] * 3] * 3] * 3
Domains = [[[[[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 3] * 3] * 3] * 3


def SelectUnassignedVariable(sudoku, domains):
    biggest_heuristic_value = -1
    result = [-1, -1, -1, -1]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    variable = [i, j, k, l]

                    if sudoku[i][j][k][l] == -1:
                        heuristic_value = 9 - len(domains[i][j][k][l])

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

    variable = SelectUnassignedVariable(sudoku, domains)

    for values in OrderDomainValues(variable, domains):
        sudoku_copy = copy.deepcopy(sudoku)
        domains_copy = copy.deepcopy(domains)
        value = values[1]

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


def InitializeDomains():
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    value = Sudoku[i][j][k][l]
                    variable = [i, j, k, l]
                    if value != -1:
                        Inference(Domains, variable, value)


def Valid():
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    value = Sudoku[i][j][k][l]

                    if value != -1:
                        for m in range(3):
                            for n in range(3):

                                if Sudoku[i][m][k][n] == value:
                                    return False

                                if Sudoku[m][j][n][l] == value:
                                    return False

                                if Sudoku[i][j][m][n] == value:
                                    return False
    return True


if __name__ == '__main__':
    GetSudoku()
    if Valid():
        InitializeDomains()
        print(BackTrack(Sudoku, Domains))
    else:
        print("this is not a valid sudoku!")
