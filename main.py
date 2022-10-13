import random as rand
import tkinter as tk


class Cell:
    """Represents each individual cell on the game board. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.underPopulated = 1
        self.overPopulated = 4
        self.reproduce = 3
        self.neighboursOccupied = 0

    def checkNeighbours(self, aBoard):
        """Checks if all adjacent cells are occupied or not. (Includes Diagonals)
           This then later decides if the cell will live or not. """
        self.neighboursOccupied = 0
        try:
            if aBoard.theBoard[self.y - 1][self.x - 1].occupied and self.y - 1 != -1 and self.x - 1 != -1:
                self.neighboursOccupied += 1
        except IndexError:
            pass
        try:
            if aBoard.theBoard[self.y - 1][self.x].occupied and self.y - 1 != -1:
                self.neighboursOccupied += 1
        except IndexError:
            pass
        try:
            if aBoard.theBoard[self.y - 1][self.x + 1].occupied and self.y - 1 != -1:
                self.neighboursOccupied += 1
        except IndexError:
            pass
        try:
            if aBoard.theBoard[self.y][self.x - 1].occupied and self.x - 1 != -1:
                self.neighboursOccupied += 1
        except IndexError:
            pass
        try:
            if aBoard.theBoard[self.y][self.x + 1].occupied:
                self.neighboursOccupied += 1
        except IndexError:
            pass
        try:
            if aBoard.theBoard[self.y + 1][self.x - 1].occupied and self.x - 1 != -1:
                self.neighboursOccupied += 1
        except IndexError:
            pass
        try:
            if aBoard.theBoard[self.y + 1][self.x].occupied:
                self.neighboursOccupied += 1
        except IndexError:
            pass
        try:
            if aBoard.theBoard[self.y + 1][self.x + 1].occupied:
                self.neighboursOccupied += 1
        except IndexError:
            pass

    def occupyUpdate(self):
        """Updates if the cell should still be occupied or not"""
        if self.occupied:
            if self.underPopulated >= self.neighboursOccupied or self.neighboursOccupied >= self.overPopulated:
                self.occupied = False
        else:
            if self.neighboursOccupied == self.reproduce:
                self.occupied = True


class Board:
    """The board the game happens on"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.theBoard = []
        for i in range(0, y):
            row = []
            for j in range(0, x):
                row.append(Cell(j, i))
            self.theBoard.append(row)

    def randomPopulate(self, amount):
        """Populates an amount of the board determined by the call method,
         cells can be randomly selected twice for simplicity"""
        area = self.x * self.y
        numOfOccupies = area // amount  # play testing to determine

        for i in range(0, numOfOccupies):
            self.theBoard[rand.randint(0, self.y - 1)][rand.randint(0, self.x - 1)].occupied = True

    def clearBoard(self):
        """clears all the occupied cells"""
        for row in self.theBoard:
            for cell in row:
                cell.occupied = False

    def occupyOne(self):
        """Occupies one chosen cell"""
        x = int(input("which x value to occupy? "))
        y = int(input("which y value to occupy? "))
        self.theBoard[y][x].occupied = True

    def checkAllNeighbours(self):
        """makes each cell check how many of its neighbours are occupied"""
        for row in self.theBoard:
            for cell in row:
                cell.checkNeighbours(self)

    def updateAllCells(self):
        """updates all cells occupied state"""
        for row in self.theBoard:
            for cell in row:
                cell.occupyUpdate()

    def PrintGridCoords(self):
        """way to visualise coordinates of the board"""
        for row in self.theBoard:
            print("\n")
            for cell in row:
                print("(" + str(cell.y) + "," + str(cell.x) + ")", end=",")
        print("\n")

    def PrintGrid(self):
        """way to visualise the board and which cells are occupied or not"""
        for row in self.theBoard:
            print("\n")
            for cell in row:
                if cell.occupied:
                    print("\033[7;31;40m X \033[0;0m", end=",")
                else:
                    print("\033[5;31;40m O \033[0;0m", end=",")
        print("\n")

    def PrintGridNeighboursOccupied(self):
        """way to check neighbours are counted correctly"""
        for row in self.theBoard:
            print("\n")
            for cell in row:
                print(cell.neighboursOccupied, end=",")
        print("\n")


is_running = False


class App(tk.Tk):
    """tkinter class that contains the GameOfLife application. """
    def __init__(self, theBoard):
        super().__init__()
        self.theBoard = theBoard

        # self.geometry("400x600")
        self.title("Conway's Game Of Life")
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(self.theBoard.y, weight=1)
        self.rowconfigure(self.theBoard.x, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """stores all the different buttons and widgets that load on the screen"""
        buttons = dict()

        def updateButton(n):
            """updates the button colour based on if that cell is occupied or not,
                finds the cell based on the buttons text which contains its coordinates"""
            text = buttons[n].cget("text")
            lst = text.split(",")
            row = int(lst[0])
            col = int(lst[1])
            if self.theBoard.theBoard[row][col].occupied:
                buttons[n].configure(highlightbackground="red", activebackground="red", activeforeground="red",
                                     fg="red", bg="red")
            else:
                buttons[n].configure(highlightbackground="blue", activebackground="blue", activeforeground="blue",
                                     fg="blue", bg="blue")

        def updateAllButtons():
            """updates the colour of all buttons"""
            for i in buttons:
                updateButton(i)

        def button_click(i, j):
            """allows for manual changing of each cell, i.e. drawing specific patterns"""
            n = str(i) + "," + str(j)
            text = buttons[n].cget("text")
            lst = text.split(",")
            row = int(lst[0])
            col = int(lst[1])

            if self.theBoard.theBoard[row][col].occupied:
                buttons[n].configure(highlightbackground="blue", activebackground="blue", activeforeground="blue",
                                     fg="blue", bg="blue")
                self.theBoard.theBoard[row][col].occupied = False
            else:
                buttons[n].configure(highlightbackground="red", activebackground="red", activeforeground="red",
                                     fg="red", bg="red")
                self.theBoard.theBoard[row][col].occupied = True

        def clearBoard():
            """kills all cells"""
            self.theBoard.clearBoard()
            updateAllButtons()

        def step1gen():
            """the game runs once, following the rules of GoL"""
            self.theBoard.checkAllNeighbours()
            self.theBoard.updateAllCells()
            updateAllButtons()

        def populateBoard():
            """randomly populates the board with alive cells for simulation,
            a value of 2 = half coverage, 4 would be a quarter, etc."""
            self.theBoard.randomPopulate(2)
            updateAllButtons()

        for i in range(0, self.theBoard.x):
            for j in range(0, self.theBoard.y):
                # Creates all the board grid buttons
                n = str(i) + "," + str(j)
                if self.theBoard.theBoard[i][j].occupied:
                    buttons[n] = tk.Button(self, text=n,
                                           command=lambda i=i, j=j: button_click(i, j),
                                           highlightbackground="red", fg="red", bg="red")
                    buttons[n].grid(column=j, row=i, sticky="nesw")
                else:
                    buttons[n] = tk.Button(self, text=n,
                                           command=lambda i=i, j=j: button_click(i, j),
                                           highlightbackground="blue", fg="blue", bg="blue")
                    buttons[n].grid(column=j, row=i, sticky="nesw")

        menuLabel = tk.Label(self, text="Menu Options")
        menuLabel.grid(column=3, row=self.theBoard.y+1, columnspan=4, sticky="nesw")

        step1GenButton = tk.Button(self, text="stepAgeneration", command=lambda: step1gen())
        step1GenButton.grid(column=0, row=self.theBoard.y+2, columnspan=4, sticky="nesw")

        populateButton = tk.Button(self, text="randomly populate board", command=lambda: populateBoard())
        populateButton.grid(column=4, row=self.theBoard.y+2, columnspan=6, sticky="nesw")

        clearButton = tk.Button(self, text="clear board", command=lambda: clearBoard())
        clearButton.grid(column=0, row=self.theBoard.y+3, columnspan=4, sticky="nesw")


if __name__ == '__main__':
    app = App(Board(20, 20))
    app.mainloop()

 
