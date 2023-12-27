from tkinter import *
import pygame
from tkinter import filedialog
import cv2
import requests
import matplotlib.pyplot as plt
from deepface import DeepFace
root = Tk()
root.geometry("500x400")
root.title('MP3 player')
pygame.mixer.init()

emotion_var = StringVar()

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Could not open camera")
    exit()

# Capture a frame
ret, frame = cap.read()

# Check if the frame is captured successfully
if not ret:
    print("Could not capture frame")
    exit()

# Save the frame to a file
cv2.imwrite('capture.jpg', frame)

# Release the camera
cap.release()
img = cv2.imread("capture.jpg")

plt.imshow(img[:, :, :: -1])
# ensures that the image is displayed
plt.show()
# Add the emotion-based song selection feature
result = DeepFace.analyze(img, actions = ['emotion'])
# print result
print(result)
query = str(max(zip(result[0]['emotion'].values(), result[0]['emotion'].keys()))[1])
print(query)

emotion_var=query

def add_song():
    # Set the value of the emotion variable
    song_directory = '<file_path>'+emotion_var
    song = filedialog.askopenfilename(
        initialdir=song_directory, title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    song = song.replace('<file_path>'+emotion_var+'/', "")
    song = song.replace(".mp3", "")

    song_box.insert(END, song)

# Add the emotion-based multiple song selection feature


def add_many_song():
    # Set the value of the emotion variable
    songs = filedialog.askopenfilenames(
        initialdir='<file_path>'+emotion_var,
        title="Choose songs", filetypes=(("mp3 Files", "*.mp3"), ))
    for song in songs:
        song = song.replace(<file_path>'+emotion_var+'/', "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)

# Modified play function with updated file path and emotion argument


def play():
    song = song_box.get(ACTIVE)
    song_directory = '<file_path>'/'+song+'.mp3'
    pygame.mixer.music.load(song_directory)
    pygame.mixer.music.play(loops=0)


def stop():
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)


def next_song():
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song =’ <file_path>'+emotion_var+'/'+song+'.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


def previous_song():
    next_one = song_box.curselection()
    next_one = next_one[0]-1
    song = song_box.get(next_one)
    song = '<file_path>'+emotion_var+'/'+song+'.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_all_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()


global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


song_box = Listbox(root, bg="black", fg="white", width=60,
                   selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

back_btn_img = PhotoImage(file='<file_path>/back.png')
forward_btn_img = PhotoImage(file='<file_path>/forward.png')
play_btn_img = PhotoImage(file='<file_path>/play.png')
pause_btn_img = PhotoImage(file='<file_path>/pause.png')
stop_btn_img = PhotoImage(file=’<file_path>/stop.png')

controls_frame = Frame(root)
controls_frame.pack()

back_button = Button(controls_frame, image=back_btn_img,
                     borderwidth=0, command=previous_song)
forward_button = Button(
    controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img,
                     borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img,
                      borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img,
                     borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist", command=add_song)

add_song_menu.add_command(
    label="Add Many song to playlist", command=add_many_song)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(
    label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(
    label="Delete all songs from playlist", command=delete_all_songs)
root.mainloop()




