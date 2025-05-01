import tkinter as tk
import rclpy
import threading

from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration

from std_msgs.msg import String

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult



# === Define room name to pose mappings ===
WAYPOINTS = {
    "Woods 134": ([-20.0, 20.4], TurtleBot4Directions.EAST),
    "Woods 119": ([0.372, -0.028], TurtleBot4Directions.EAST),
    "Woods 136": ([-17.5, 32.3], TurtleBot4Directions.EAST),
    "Woods 137": ([-16.6, 30.6], TurtleBot4Directions.EAST),
    "Woods 138": ([-12.2, 22.5], TurtleBot4Directions.EAST),
    "Woods 139": ([-2.24, 23.7], TurtleBot4Directions.EAST),
    "stairs": ([-7.97, 24.6], TurtleBot4Directions.EAST),
    "Woods 140": ([1.09, 23.3], TurtleBot4Directions.EAST),
    "Woods 133": ([-17.8, 22.6], TurtleBot4Directions.EAST),
    "Woods 133A": ([-18.4, 18.1], TurtleBot4Directions.EAST),
    "Woods 132": ([-18.8, 15.2], TurtleBot4Directions.EAST),
    "Woods 131A": ([-24.2, 15.7], TurtleBot4Directions.EAST),
    "Woods 131": ([-23.6, 16.1], TurtleBot4Directions.EAST),
    "Woods 130": ([-19.2, 11.12], TurtleBot4Directions.EAST),
    "Woods 129": ([-20.8, 10.3], TurtleBot4Directions.EAST),
    "Woods 128": ([-21.6, 3.98], TurtleBot4Directions.EAST),
    "Woods 125": ([-20.3, 0.893], TurtleBot4Directions.EAST),
    "Woods 124": ([-16.0, 0.345], TurtleBot4Directions.EAST),
    "Woods 127-A": ([-12.5, 1.64], TurtleBot4Directions.EAST),
    "Woods 123": ([-11.3, -0.352], TurtleBot4Directions.EAST),
    "Woods 127": ([-8.66, 1.14], TurtleBot4Directions.EAST),
    "Woods 126": ([-7.12, 0.942], TurtleBot4Directions.EAST),
    "woods 121" : ([-5.95,-0.924], TurtleBot4Directions.EAST),
    "Woods 120": ([-1.27, 0.121], TurtleBot4Directions.EAST),
    "Woods 118": ([13.6, -3.38], TurtleBot4Directions.EAST),
    "Woods 118A": ([18.4, -3.95], TurtleBot4Directions.EAST),
    "Woods 117": ([24.0, -2.49], TurtleBot4Directions.EAST),
    "Woods 116": ([25.2, -4.9], TurtleBot4Directions.EAST),
    "Woods 115": ([26.7, -3.26], TurtleBot4Directions.EAST),
    "Woods 114": ([27.4, -5.09], TurtleBot4Directions.EAST),
    "Woods 113": ([35.9, -5.85], TurtleBot4Directions.EAST),
    "Woods 111": ([36.7, -5.79], TurtleBot4Directions.EAST),
    "Woods 112": ([36.2, 2.88], TurtleBot4Directions.EAST),
    "Woods 110": ([-37.2, 6.55], TurtleBot4Directions.EAST),
    "Woods 108": ([37.4, 10.4], TurtleBot4Directions.EAST),
    "elevator": ([36.1, -2.56], TurtleBot4Directions.EAST),
    "Men's bathroom": ([-19.9, 5.87], TurtleBot4Directions.EAST),
    "Women's bathroom": ([10.8, -1.36], TurtleBot4Directions.EAST),
    "Woods 148/Blackman's auditorium": ([10.7, 5.16], TurtleBot4Directions.EAST),
    # Add more rooms here
}


def main():

    rclpy.init()
    navigator = TurtleBot4Navigator()



    def navigate_to_room(room_name):
        if room_name in WAYPOINTS:
            coords, direction = WAYPOINTS[room_name]
            goal_pose = navigator.getPoseStamped(coords, direction)
            print(f"Navigating to: {room_name} at {coords}")



            threading.Thread(
                target=navigator.startToPose,
                args=(goal_pose,),
                kwargs={
                "eta_callback": lambda eta: eta_label.after(0, lambda: update_eta(eta))
                    },daemon=True).start()
            

        else:
            print(f"No known location for: {room_name}")

        # === Tkinter UI ===
    window = tk.Tk()
    window.title("Guide Robot")
    window.geometry("700x500")

    central_frame = tk.Frame(window)
    central_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_frame = tk.Frame(central_frame)
    status_frame.pack(pady=(10, 10))

    status_label = tk.Label(status_frame, text="Status:", font=("Arial", 16))
    status_label.pack(side=tk.LEFT)

    status_indicator = tk.Canvas(status_frame, width=20, height=20, highlightthickness=0)
    status_indicator.pack(side=tk.LEFT, padx=5)
    status_indicator.create_oval(2, 2, 18, 18, fill="gray", tags="indicator")

    eta_label = tk.Label(status_frame, text="1")
    eta_label.pack(side=tk.LEFT, padx=(10, 0))

    instruction_label = tk.Label(
        central_frame, text="Type the room you would like to be guided to:", font=("Arial", 22)
    )
    instruction_label.pack(pady=(10, 0))

    example_label = tk.Label(
        central_frame, text='e.g. "Woods 134"', font=("Arial", 16), fg="gray"
    )
    example_label.pack(pady=(0, 20))

    search_var = tk.StringVar()
    search_entry = tk.Entry(central_frame, textvariable=search_var, font=("Arial", 18), width=40)
    search_entry.pack()

    search_frame = tk.Frame(central_frame)
    search_frame.pack(pady=(10, 10))

    mic_button = tk.Button(search_frame, text="🎤", font=("Arial", 14), command=lambda: print("Mic button clicked"))
    mic_button.pack(side=tk.LEFT, padx=(5, 0))

    suggestion_list = tk.Listbox(central_frame, font=("Arial", 18), width=40, height=6)
    suggestion_list.pack()

    def update_suggestions(*args):
        search_term = search_var.get()
        suggestions = list(WAYPOINTS.keys())
        matching_suggestions = [s for s in suggestions if s.lower().startswith(search_term.lower())]
        suggestion_list.delete(0, tk.END)
        for s in matching_suggestions:
            suggestion_list.insert(tk.END, s)

    search_var.trace("w", update_suggestions)

    def select_suggestion(event):
        selected_suggestion = suggestion_list.get(suggestion_list.curselection())
        search_var.set(selected_suggestion)
        perform_search()

    def perform_search():
        room_name = search_var.get()
        print("Performing search for:", room_name)
        threading.Thread(target=navigate_to_room, args=(room_name,), daemon=True).start()

        

    suggestion_list.bind("<<ListboxSelect>>", select_suggestion)
    search_entry.bind("<Return>", lambda event: perform_search())

    def update_status(color):
        status_indicator.itemconfig("indicator", fill=color)

    def update_eta(eta_text):
        eta_label.config(text=f"ETA: {eta_text}")

    try:
        window.mainloop()
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()