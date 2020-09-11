import pygame
pygame.init()

def setupCanvas():
    global canvasdim
    global griddim
    global offset
    global canvas
    global canvas_colour

    canvas_colour = (85, 52, 43)

    griddim = 50
    offset = griddim

    emptyspaces = 1
    canvasdim = griddim*9 + emptyspaces*offset*2 + 3*griddim//10
    canvas = pygame.display.set_mode((canvasdim, canvasdim))

    global grid_colour
    global input_colour
    grid_colour = (253, 245, 232)
    input_colour = (0, 255, 0)

    global font
    global fpoint
    global font_colour
    font_colour = canvas_colour
    fpoint = 32
    font = pygame.font.SysFont('impact', fpoint)

    global delay_time
    delay_time = 5

    pygame.display.update()


def drawSquares(index = (None, None), isInput = False):
    canvas.fill(canvas_colour)
    for i in range(9):
        for j in range(9):
            xgap = int(griddim/10*(j//3))
            ygap = int(griddim/10*(i//3))
            x = offset + j*griddim + xgap
            y = offset + i*griddim + ygap

            if isInput and index == (j, i):
                    colour = input_colour
            else:
                colour = grid_colour

            pygame.draw.rect(canvas, colour, (x, y, griddim - 4, griddim - 4))

            if sudokuGrid[i][j]:
                num = font.render((str(sudokuGrid[i][j])), 1, font_colour)
                canvas.blit(num, (x+3*(griddim//10), y+(griddim//20)))

    pygame.time.delay(delay_time)
    pygame.display.update()


def inputGrid():
    # the puzzle is inputted here:
    # blank cells are denoted by 0's
    global sudokuGrid
    sudokuGrid = [[0] * 9 for i in range(9)]

    setupCanvas()
    drawSquares()

    breakInput = False

    while True:
        pygame.event.pump()
        drawSquares()

        if breakInput:
            break

        breakLoop = False

        for event in pygame.event.get():

            if breakLoop:
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    breakInput = True
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    for i in range(9):

                        if breakLoop:
                            break

                        for j in range(9):

                            if breakLoop:
                                break

                            xgap = int(griddim / 10 * (j // 3))
                            ygap = int(griddim / 10 * (i // 3))
                            xpos = offset + (j + 1) * griddim + xgap
                            ypos = offset + (i + 1) * griddim + ygap

                            d1 = xpos - pos[0]
                            d2 = ypos - pos[1]
                            isIndex = d1 <= griddim - 4 and d2 <= griddim - 4
                            isIndex = isIndex and d1 >= 0 and d2 >= 0

                            if isIndex:
                                drawSquares((j, i), True)

                                while True:
                                    if breakLoop:
                                        break

                                    for ev in pygame.event.get():
                                        if ev.type == pygame.KEYDOWN:
                                            num = 0
                                            if ev.key in range(49, 58):
                                                num = ev.key - 48
                                            elif ev.key in range(257, 266):
                                                num = ev.key - 256

                                            sudokuGrid[i][j] = num

                                            drawSquares()

                                            breakLoop = True
                                            break

                                breakLoop = True
                                break


def possibleSolution(row, column, digit):
    for rowTest in range (9):
        if sudokuGrid[rowTest][column] == digit:
            return False

    for columnTest in range (9):
        if sudokuGrid[row][columnTest] == digit:
            return False

    rowOffset = 3*(row//3)
    columnOffset = 3*(column//3)

    for rowTest in range (rowOffset, rowOffset+3):
        for columnTest in range (columnOffset, columnOffset+3):
            if sudokuGrid[rowTest][columnTest] == digit:
                return False

    return True


def solveGrid():
    for row in range (9):
        for column in range (9):
            if sudokuGrid[row][column] == 0:
                for digit in range (1,10):
                    if possibleSolution(row, column, digit):
                        sudokuGrid[row][column] = digit
                        drawSquares()
                        pygame.event.pump()
                        solveGrid()
                        sudokuGrid[row][column] = 0
                        drawSquares()

                return

    endScript = False
    while True:
        pygame.event.pump()

        if endScript:
            break

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    endScript = True
                    break
    exit()


if __name__ == '__main__':
    inputGrid()
    solveGrid()