import tkinter as tk
from state import State

def validate_float(self, action, index, value_if_allowed,
             prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False


def validate_int(self, action, index, value_if_allowed,
             prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False

def popup(state: State):

    root = tk.Tk("Axis constraints")

    canvas = tk.Canvas(root, width=250, height=200)
    canvas.pack()

    x0 = tk.StringVar()
    x_entry_0 = tk.Entry(canvas, textvariable=x0, validate='all', validatecommand=(validate_float, '%P'))
    canvas.create_window(150, 30, window=x_entry_0)
    x0.set(str(state.x0))

    x_label_0 = tk.Label(canvas, text="x0")
    canvas.create_window(50, 30, window=x_label_0)

    x1 = tk.StringVar()
    x_entry_1 = tk.Entry(canvas, textvariable=x1, validate='all', validatecommand=(validate_float, '%P'))
    canvas.create_window(150, 60, window=x_entry_1)
    x1.set(str(state.x1))

    x_label_1 = tk.Label(canvas, text="x1")
    canvas.create_window(50, 60, window=x_label_1)

    y0 = tk.StringVar()
    y_entry_0 = tk.Entry(canvas, textvariable=y0, validate='all', validatecommand=(validate_float, '%P'))
    canvas.create_window(150, 90, window=y_entry_0)
    y0.set(str(state.y0))

    y_label_0 = tk.Label(canvas, text="y0")
    canvas.create_window(50, 90, window=y_label_0)

    y1 = tk.StringVar()
    y_entry_1 = tk.Entry(root, textvariable=y1, validate='all', validatecommand=(validate_float, '%P'))
    canvas.create_window(150, 120, window=y_entry_1)
    y1.set(str(state.y1))

    y_label_1 = tk.Label(root, text="y1")
    canvas.create_window(50, 120, window=y_label_1)

    #
    # resolution = tk.StringVar()
    # res_entry = tk.Entry(root, textvariable=resolution, validate='all', validatecommand=(validate_int, '%P'))
    # canvas.create_window(150, 150, window=res_entry)
    # resolution.set(str(state.resolution))
    #
    # res_label = tk.Label(root, text="samples")
    # canvas.create_window(35, 150, window=res_label)

    def do_stuff():
        try:
            state.x0 = float(x0.get())
            state.x1 = float(x1.get())
            state.y0 = float(y0.get())
            state.y1 = float(y1.get())
            # state.resolution = int(resolution.get())

        except:
            print("Failed to set all variables")

        root.destroy()

    button1 = tk.Button(text='OK', command=do_stuff)
    canvas.create_window(125, 180, window=button1)


    root.mainloop()

if __name__ == "__main__":
    popup(State())