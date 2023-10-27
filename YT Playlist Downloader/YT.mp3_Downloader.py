from pytube import Playlist, YouTube
import os
import moviepy.editor as mp
import tkinter as tk
from tkinter import ttk

def download_playlist():
    url = url_entry.get()

    try:
        playlist = Playlist(url)
        playlist_size = len(playlist.video_urls)
        videos_downloaded = 0

        os.makedirs('./Downloads/', exist_ok=True)

        for url in playlist:
            video = YouTube(url)
            stream = video.streams.filter(only_audio=True).first()
            file_name = stream.default_filename
            stream.download(output_path = "./Downloads/")
            videos_downloaded += 1
            
            log_text.insert(tk.END, f"Downloaded: {file_name}\n")
            log_text.see(tk.END)
            progress_label.config(text=f"Downloading Videos: {videos_downloaded}/{playlist_size}")
            progress_bar['value'] = (videos_downloaded / playlist_size) * 100
            window.update()

            # Convert the downloaded audio file from MP4 to MP3
            mp4_path = os.path.join("./Downloads/", file_name)
            mp3_path = os.path.join("./Downloads/", os.path.splitext(file_name)[0] + '.mp3')
            mp.AudioFileClip(mp4_path).write_audiofile(mp3_path)
            os.remove(mp4_path)

        completion_label.config(text="Success!!\nDownload & Conversion Completed!")

    except Exception as e:
        completion_label.config(text=f"An error has occurred: {e}")
        
window = tk.Tk()
window.title("YouTube Playlist Downloader")
window.option_add("*Font", ("Helvetica", 11))

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_offset = (screen_width - 500) // 2
y_offset = (screen_height - 450) // 2   

window.geometry(f"500x450+{x_offset}+{y_offset}")

url_label = tk.Label(window, text = "Enter the playlist URL: ")
url_label.pack(pady = 10)
url_entry = tk.Entry(window, width = 50)
url_entry.pack()

def change_color(event):
    download_button.config(bg = "#89F6FA")  # Change the background color to red

def reset_color(event):
    download_button.config(bg = "SystemButtonFace") 

download_button = tk.Button(window, text = "Download", command = download_playlist)
download_button.pack(pady = 10)
download_button.bind("<Enter>", change_color)
download_button.bind("<Leave>", reset_color)

progress_label = tk.Label(window, text="Videos Downloaded: 0/0")
progress_label.pack()
progress_bar = ttk.Progressbar(window, orient = 'horizontal', length = 350, mode = 'determinate')
progress_bar.pack(pady = 10)

log_label = tk.Label(window, text = "Log:")
log_label.pack()
log_text = tk.Text(window, width = 60, height=10)
log_text.pack(padx = 20)

completion_label = tk.Label(window, text="", font = ("Tahoma", 15, "bold"))
completion_label.pack(pady=10)

window.mainloop()