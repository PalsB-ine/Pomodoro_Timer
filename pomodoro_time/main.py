import time
import os
import sys
import sounddevice as sd
import soundfile as sf
from plyer import notification

def countdown(minutes):

    total_seconds = minutes * 60

    while total_seconds:
        minutes , seconds = divmod(total_seconds , 60)

        timer = f"{minutes:02d}:{seconds:02d}"

        print(timer , end="\r")
        time.sleep(1)
        total_seconds -= 1

    print("00:00", end="\r")


def send_notification(title : str, message : str):

    if getattr(sys , "frozen" , False):
        audio_path = os.path.join(sys._MEIPASS , "Discord_Notification.wav")

    else:
        audio_path = os.path.join(os.path.dirname(__file__) , "Discord_Notification.wav")

    # read the audio path (audio , audio_bit_rate)
    audio , audio_rate = sf.read(audio_path)

    # plays the sound and waits until it's finished
    sd.play(audio,audio_rate)
    sd.wait()

    # send the notfication
    notification.notify(title=title,message=message,)


def pomodoro_timer(work_duration=25, short_break=5, long_break=15, sessions=4):

    for session in range(1 , sessions + 1):

        send_notification("Pomodoro Timer" , f"Pomodoro Session {session}/{sessions} - Work Time")
        countdown(work_duration)

        if session < sessions:
            send_notification("Pomodoro Timer" , "Time for a short break!")
            countdown(short_break)

        if session % 4 == 0 and session != sessions:
            send_notification("Pomodoro Timer" , "Time for a long break!")
            countdown(long_break)


    send_notification("Pomodoro Timer" , "All sessions completed!")


def get_and_handle_user_input(prompt_message: str):

    while True:
        try:

            user_input = int(input(prompt_message))

            if user_input < 1:
                print("Please enter a number that is bigger than 1")
                continue

            return user_input

        except ValueError:
            print("Please enter a valid number")


def main():

    work_duration = get_and_handle_user_input("Please enter work duration (minutes): ")
    short_break = get_and_handle_user_input("Please enter short break duration (minutes) ")
    long_break = get_and_handle_user_input("Please enter long break duration (minutes) ")
    sessions = get_and_handle_user_input("Please enter number of sessions: ")

    pomodoro_timer(work_duration , short_break , long_break , sessions)


if __name__ == "__main__":
    main()