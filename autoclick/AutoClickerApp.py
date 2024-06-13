import time
import threading
import tkinter as tk
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, Key
import re

# Global constants for min and max sleep intervals (in seconds)
MIN_SLEEP_INTERVAL = 0.001  # 0.1 millisecond
MAX_SLEEP_INTERVAL = 1.0  # 1 second
DEFAULT_TOGGLE_KEY = Key.f1  # Default toggle key F1


class AutoClickerApp:
    """
    Auto Clicker application using tkinter for GUI and pynput for keyboard and mouse control.

    Attributes:
        root (tk.Tk): Main tkinter window.
        clicking (bool): Indicates if the auto clicker is currently active.
        click_interval (float): Time interval between each click, in seconds.
        toggle_key (pynput.keyboard.Key): Key used to toggle auto clicker on/off.
        timer_active (bool): Indicates if the timer is currently active.
        timer_duration (int): Duration of the timer in seconds.
        timer_start_time (float): Start time of the timer in seconds since Unix epoch.
        remaining_time (int): Remaining time of the timer in seconds.
        mouse (pynput.mouse.Controller): Mouse controller for simulating clicks.

    Methods:
        __init__(self, root):
            Initializes the Auto Clicker application with all GUI elements and necessary threads.

        clicker(self):
            Thread function to perform auto clicks at regular intervals.

        toggle_clicker(self):
            Toggles the auto clicker on/off and updates the GUI accordingly.

        start_timer(self):
            Starts the timer with user-specified duration and activates the auto clicker.

        stop_timer(self):
            Stops the timer, deactivates the auto clicker, and resets the GUI.

        validate_timer_input(self, timer_input):
            Validates the format of the timer input (HH:MM:SS).

        update_remaining_time(self):
            Updates the display of remaining time every second.

        change_speed(self, event):
            Updates the auto click speed based on GUI scale position.

        keyboard_listener(self):
            Thread function to listen for keyboard key presses.

        on_key_press(self, key):
            Callback function when a key is pressed, used to toggle the auto clicker.

    """

    def __init__(self, root):
        """
        Initializes the Auto Clicker application with all GUI elements and necessary threads.

        Args:
            root (tk.Tk): Main tkinter window.
        """
        self.root = root
        self.root.title("ATC's Auto-Clicker")
        self.root.geometry("400x350")  # Window size

        self.clicking = False
        self.click_interval = MAX_SLEEP_INTERVAL  # Default click interval
        self.toggle_key = DEFAULT_TOGGLE_KEY
        self.timer_active = False
        self.timer_duration = 0  # Timer duration in seconds
        self.timer_start_time = 0  # Timer start time in seconds
        self.remaining_time = 0  # Remaining time of the timer in seconds

        self.mouse = Controller()

        # Main frame to contain all elements
        self.main_frame = tk.Frame(root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Label for clicker status
        self.status_label = tk.Label(self.main_frame, text="Auto-clicker is disabled", fg="red", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Label to display current toggle key
        self.current_key_label = tk.Label(self.main_frame, text=f"Current toggle key: '{self.toggle_key}'",
                                          font=("Arial", 10))
        self.current_key_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Label and entry field for timer
        self.timer_label = tk.Label(self.main_frame, text="Timer (HH:MM:SS):", font=("Arial", 10))
        self.timer_label.grid(row=2, column=0, padx=(10, 5), pady=5)

        self.timer_entry = tk.Entry(self.main_frame, font=("Arial", 10))
        self.timer_entry.grid(row=2, column=1, padx=(5, 10), pady=5)

        # Start Timer button to start the timer
        self.start_timer_button = tk.Button(self.main_frame, text="Start Timer", command=self.start_timer,
                                            font=("Arial", 10))
        self.start_timer_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Label to display remaining time
        self.remaining_time_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.remaining_time_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Label to display current clicks per second
        self.current_speed_label = tk.Label(self.main_frame, text="", font=("Arial", 10))
        self.current_speed_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Scale to adjust clicks per second from 1 to 1000
        self.speed_scale = tk.Scale(self.main_frame, from_=1, to=1000, orient=tk.HORIZONTAL, font=("Arial", 10))
        self.speed_scale.set(1)  # Default to 1 click per second
        self.speed_scale.grid(row=6, column=0, columnspan=2, padx=20, pady=10)
        self.speed_scale.bind("<Motion>", self.change_speed)

        # Start the clicker thread
        self.click_thread = threading.Thread(target=self.clicker)
        self.click_thread.daemon = True
        self.click_thread.start()

        # Start the keyboard listener thread
        self.listener_thread = threading.Thread(target=self.keyboard_listener)
        self.listener_thread.daemon = True
        self.listener_thread.start()

        # Method to update remaining time display
        self.update_remaining_time()

    def clicker(self):
        """
        Thread function to perform auto clicks at regular intervals.
        """
        while True:
            if self.clicking:
                self.mouse.click(Button.left, 1)
            time.sleep(max(MIN_SLEEP_INTERVAL, self.click_interval))
            # Update label with current clicks per second
            clicks_per_second = int(1 / self.click_interval)
            self.current_speed_label.config(text=f"Current speed: {clicks_per_second} click(s)/sec")

    def toggle_clicker(self):
        """
        Toggles the auto clicker on/off and updates the GUI accordingly.
        """
        self.clicking = not self.clicking
        status = "enabled" if self.clicking else "disabled"
        self.status_label.config(text=f"Auto-clicker is {status}", fg="green" if self.clicking else "red")
        print(f'Auto-clicker is now {status}.')

    def start_timer(self):
        """
        Starts the timer with the user-specified duration and activates the auto clicker.
        Displays an error message if the timer format is incorrect.
        """
        if not self.timer_active:
            timer_input = self.timer_entry.get().strip()
            if self.validate_timer_input(timer_input):
                hours, minutes, seconds = map(int, timer_input.split(":"))
                self.timer_duration = hours * 3600 + minutes * 60 + seconds
                self.remaining_time = self.timer_duration
                self.timer_start_time = time.time()
                self.timer_active = True
                self.start_timer_button.config(state=tk.DISABLED)  # Disable button during timer
                self.toggle_clicker()  # Activate clicker when timer starts
                self.update_remaining_time()
                print(f"Timer set for {hours} hours, {minutes} minutes, and {seconds} seconds.")
            else:
                print("Invalid timer format. Please use HH:MM:SS.")

    def stop_timer(self):
        """
        Stops the timer, deactivates the auto clicker, and resets the GUI.
        """
        self.timer_active = False
        self.start_timer_button.config(state=tk.NORMAL)  # Enable button after timer
        self.remaining_time = 0
        self.update_remaining_time()
        self.toggle_clicker()  # Deactivate clicker at end of timer

    def validate_timer_input(self, timer_input):
        """
        Validates the format of the timer input (HH:MM:SS).

        Args:
            timer_input (str): User input for timer duration.

        Returns:
            bool: True if the input format is valid, False otherwise.
        """
        pattern = re.compile(r'^([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$')
        return bool(pattern.match(timer_input))

    def update_remaining_time(self):
        """
        Updates the display of remaining time every second.
        """
        if self.timer_active or self.remaining_time > 0:
            if self.timer_active:
                elapsed_time = time.time() - self.timer_start_time
                self.remaining_time = max(self.timer_duration - elapsed_time, 0)
            hours = int(self.remaining_time // 3600)
            minutes = int((self.remaining_time % 3600) // 60)
            seconds = int(self.remaining_time % 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.remaining_time_label.config(text=f"Time remaining: {time_str}")
        else:
            self.remaining_time_label.config(text="Time remaining: 0:00:00")

        if self.timer_active or self.remaining_time > 0:
            if self.remaining_time > 0:
                self.root.after(1000, self.update_remaining_time)  # Update every second
            else:
                self.stop_timer()  # Stop timer and deactivate auto-clicker

    def change_speed(self, event):
        """
        Updates the speed of automatic clicks based on GUI scale position.

        Args:
            event: The event object triggered by interacting with the speed scale GUI element.
        """
        clicks_per_second = self.speed_scale.get()
        self.click_interval = MAX_SLEEP_INTERVAL / clicks_per_second
        self.current_speed_label.config(text=f"Current speed: {clicks_per_second} click(s)/sec")
        print(f'Click interval changed to: {self.click_interval:.4f} seconds')

    def keyboard_listener(self):
        """
        Function run as a thread to listen for keyboard key presses.
        """
        with Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def on_key_press(self, key):
        """
        Called when a key is pressed, used to toggle the auto-clicker on/off.

        Args:
            key (pynput.keyboard.Key): The key object representing the key that was pressed.
        """
        if key == self.toggle_key:
            if not self.timer_active:
                self.toggle_clicker()
            else:
                self.stop_timer()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
