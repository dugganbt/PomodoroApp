from tkinter import *
import math
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Helvetica"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0

timer = None


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    # Stop the timer
    window.after_cancel(timer)

    # Reset the start button
    start_button.config(state="normal")

    # Reset the timer label
    canvas.itemconfig(timer_text, text=f"00:00")

    # Reset the label
    timer_label.config(text="Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)

    # Reset the check marks
    check_mark.config(text="")

    # Reset reps
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    # Turn of start button once timer is started
    start_button.config(state="disabled")

    work_sec = WORK_MIN*60
    short_break_sec = SHORT_BREAK_MIN*60
    long_break_sec = LONG_BREAK_MIN * 60

    # Alternate between work time and break time
    # Every 8th repetition is a longer break
    if reps % 2 != 0:
        count_down(work_sec)
        timer_label.config(text="Work", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)
    elif reps == 8:
        count_down(long_break_sec)
        timer_label.config(text="Long break", font=(FONT_NAME, 40, "bold"), fg=RED, bg=YELLOW)
    else:
        count_down(short_break_sec)
        timer_label.config(text="Short break", font=(FONT_NAME, 40, "bold"), fg=PINK, bg=YELLOW)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)  # floor of the amount of minutes
    count_sec = count % 60  # remainder of seconds after we get the minutes

    # formatting special case to add a zero
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()

        """
            Explanation of check marks calculation
                every two reps a work session is done
                after the first work session, rep = 2
                after the first break, work session = 3/2 = 1.5 -> 1
                after the second work session rep = 2/2 = 2 -> 2, etc
        """
        work_sessions_complete = math.floor(reps / 2)
        if work_sessions_complete > 0:
            checks_done_text = work_sessions_complete * "✓"
            check_mark.config(text=f"{checks_done_text}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

# Photo Image creation to convert file for the canvas
tomato_img = PhotoImage(file="tomato.png")

# Placing the image onto the canvas
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Timer text
timer_label = Label(text="Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

# Start button
start_button = Button(text="Start", bg=YELLOW, highlightbackground=YELLOW, command=start_timer)
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(text="Reset", bg=YELLOW, highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(column=2, row=2)

# Check mark
check_mark = Label(font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW)
check_mark.grid(column=1, row=3)

window.mainloop()
