import random
def get_latest_data():
    #50%の確率でNoneを返す（データが来ない状態）
    if random.random()<0.5:
        return None
    #データが来たときは辞書を返す
    return{
        "t":random.uniform(0,30),
        "roll":random.uniform(-5,5),
        "pitch":random.uniform(-5,5),
        "yaw":random.uniform(0,360),
        "x":random.uniform(-10,10),
        "y":random.uniform(-10,10),
        "state":random.choice(["SEARCH","APPROACH","GOAL"]),
        "goal":random.choice([True,False]),
        "color":random.choice(["赤","青","緑",""]),
    }

import tkinter as tk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)
root=tk.Tk()
root.geometry("1000x650")
root.title("CanSat状況モニター")


top_frame=tk.Frame(root,height=50)
top_frame.pack(fill="x")
title_label=tk.Label(top_frame,text="CanSat状況モニター")
title_label.pack(side="left")
mode_labe=tk.Label(top_frame,text="モード：ライブ")
mode_labe.pack(side="left")
time_label=tk.Label(top_frame,text="経過：00:00")
time_label.pack(side="right")

main_frame=tk.Frame(root)
main_frame.pack(fill="both",expand=True)
sidebar=tk.Frame(main_frame,width=250)
sidebar.pack(side="left",fill="y")
label_title_pose=tk.Label(sidebar,text="姿勢")
label_title_pose.pack(anchor="w")
label_roll_title=tk.Label(sidebar,text="Roll:")
label_roll_title.pack(anchor="w")
label_pitch_title=tk.Label(sidebar,text="Pitch:")
label_pitch_title.pack(anchor="w")
label_yaw_title=tk.Label(sidebar,text="Yaw")
label_yaw_title.pack(anchor="w")
label_title_pos=tk.Label(sidebar,text="位置")
label_title_pos.pack(anchor="w")
label_x_title=tk.Label(sidebar,text="X:")
label_x_title.pack(anchor="w")
label_y_title=tk.Label(sidebar,text="Y:")
label_y_title.pack(anchor="w")
roll_value=tk.Label(sidebar,text="=---")
roll_value.pack(anchor="w")
pitch_value=tk.Label(sidebar,text="---")
pitch_value.pack(anchor="w")
yaw_value=tk.Label(sidebar,text="---")
yaw_value.pack(anchor="w")
x_value=tk.Label(sidebar,text="---")
x_value.pack(anchor="w")
y_value=tk.Label(sidebar,text="---")
y_value.pack(anchor="w")
label_state_title=tk.Label(sidebar,text="状態")
label_state_title.pack(anchor="w")
state_value = tk.Label(sidebar, text="---", width=10, bg="lightgray")
state_value.pack(anchor="w")
label_goal_title = tk.Label(sidebar, text="ゴール検出",  bg="#f0f0f0")
label_goal_title.pack(anchor="w")
goal_value = tk.Label(sidebar, text="---",  width=10, bg="lightgray")
goal_value.pack(anchor="w")
label_color_title = tk.Label(sidebar, text="色検出", bg="#f0f0f0")
label_color_title.pack(anchor="w")
color_value = tk.Label(sidebar, text="---", width=10, bg="lightgray")
color_value.pack(anchor="w")



map_area=tk.Canvas(main_frame,width=650,height=570)
map_area.pack(side="right",fill="both",expand=True)

label_roll=tk.Label(root,text="roll:---")
label_roll.pack()
label_pitch=tk.Label(root,text="pitch:---")
label_pitch.pack()
label_yaw=tk.Label(root,text="yaw:---")
label_yaw.pack()
label_x=tk.Label(root,text="x:---")
label_x.pack()
label_y=tk.Label(root,text="y:---")
label_y.pack()
label_state=tk.Label(root,text="state:---")
label_state.pack()
label_goal=tk.Label(root,text="goal:---")
label_goal.pack()
label_color=tk.Label(root,text="color:---")
label_color.pack()

def update_data():
    data=get_latest_data()
    if data is None:
        root.after(500,update_data)
        return
    label_roll.config(text=f"roll:{data['roll']:.2f}")
    label_pitch.config(text=f"pitch:{data['pitch']:.2f}")
    label_yaw.config(text=f"yaw:{data['yaw']:.2f}")
    label_x.config(text=f"x:{data['x']:.2f}")
    label_y.config(text=f"y:{data}['y']:.2f")
    label_state.config(text=f"state:{data['state']}")
    label_goal.config(text=f"goal:{data['goal']}")
    label_color.config(text=f"color:{data['color']}")
    root.after(500,update_data)
    
    roll_value.config(text=f"{data['roll']:.2f}")
    pitch_value.config(text=f"{data['pitch']:.2f}")
    yaw_value.config(text=f"{data['yaw']:.2f}")

    x_value.config(text=f"{data['x']:.2f}")
    y_value.config(text=f"{data['y']:.2f}")

    state = data["state"]
    if state == "SEARCH":
        state_value.config(text="探索中", bg="lightblue")
    elif state == "APPROACH":
        state_value.config(text="接近中", bg="orange")
    elif state == "GOAL":
        state_value.config(text="到達！", bg="red")
    else:
        state_value.config(text="不明", bg="gray")

    if data["goal"]:
        goal_value.config(text="検出！", bg="red", fg="white")
    else:
        goal_value.config(text="---", bg="lightgray", fg="black")

    color_value.config(text=data["color"])
    root.after(1,update_data)

update_data()
root.mainloop()