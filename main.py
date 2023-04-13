sudoku = [[[[-1] * 3] * 3] * 3] * 3


def RemainingValues(sudoku, row1, column1, row2, column2):
    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

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

    result = 9 - len(domain)
    return result


def MRV(sudoku):
    biggest_heuristic_value = -1
    result = [-1, -1, -1, -1]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    heuristic_value = RemainingValues(sudoku, i, j, k, l)
                    if heuristic_value > biggest_heuristic_value:
                        biggest_heuristic_value = heuristic_value
                        result = [i, j, k, l]
    return result


if __name__ == '__main__':
    print(sudoku)
