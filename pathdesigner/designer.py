import tkinter as tk


CIRCLE_RAD = 5
CELL_PX = 50
CELLS = 20
grid_width = grid_height = CELLS * CELL_PX

points = list()
tkinter_circles = list()


# Snap point to nearest half-square
def snap(x):
    snap_size = CELL_PX / 4
    mod = x % snap_size
    lower = (x // snap_size) * snap_size
    higher = ((x // snap_size)+1) * snap_size
    return lower if mod < (snap_size/2) else higher

# From tkinter coords to geometric
def transform(x, y):
    x = x - grid_width / 2
    y = grid_height / 2 - y
    return x,y

# From geometrix coords to tkinter
def inverse_transform(x, y):
    x = grid_width / 2 + x
    y = y + grid_height / 2
    return x, y

def on_mouse_move(event, position_label):
    position_label.config(text=f"Mouse position: ({transform(event.x, event.y)})")

def create_grid(canvas, width, height, cell_size):
    for i in range(0, width, cell_size):
        for j in range(0, height, cell_size):
            canvas.create_rectangle(i, j, i + cell_size, j + cell_size, fill='white')

def add_point(canvas, x, y):
    x = snap(x)
    y = snap(y)
    points.append(transform(x,y))
    id = canvas.create_oval(x - CIRCLE_RAD, y - CIRCLE_RAD, x + CIRCLE_RAD, y + CIRCLE_RAD, fill='red')
    tkinter_circles.append(id)

def undo_point(canvas):
    if points and tkinter_circles:
        points.pop()
        canvas.delete(tkinter_circles.pop())


def display():
    for p in points:
        print(f"{p[0] / CELL_PX},{p[1] / CELL_PX}")
    print("---")


def main():
    root = tk.Tk()
    root.title("20x20 Grid")
    

    canvas = tk.Canvas(root, width=grid_width, height=grid_height)
    canvas.pack()

    create_grid(canvas, grid_width, grid_height, CELL_PX)

    position_label = tk.Label(root, text="Mouse position: (0, 0)")
    position_label.pack(side="bottom")
    canvas.bind("<Motion>", lambda event: on_mouse_move(event, position_label))
    canvas.bind("<Button-1>", lambda event: add_point(canvas, event.x, event.y))
    root.bind_all("<Control-s>", lambda event: display())
    root.bind_all("<Control-z>", lambda event: undo_point(canvas))

    add_point(canvas, *inverse_transform(0, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
