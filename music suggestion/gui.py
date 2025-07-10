import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
import pygame
from Spotify import get_random_tracks, save_liked_song, load_liked_songs, create_playlist
import os

class MusicSuggestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Müzik Öneri Uygulaması")
        self.root.geometry("1000x800")
        self.root.configure(bg="#282828")

        # Pygame mixer başlatma
        pygame.mixer.init()
        self.current_preview = None

        # Stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.TFrame", background="#282828")
        style.configure("Custom.TButton", 
                       background="#1DB954",
                       foreground="white",
                       padding=10,
                       font=('Helvetica', 10))
        style.configure("Custom.TLabel",
                       background="#282828",
                       foreground="white",
                       font=('Helvetica', 12))

        # Ana çerçeve
        self.main_frame = ttk.Frame(root, style="Custom.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Başlık
        self.title_label = ttk.Label(self.main_frame,
                                   text="Spotify Müzik Önerileri",
                                   style="Custom.TLabel",
                                   font=('Helvetica', 24))
        self.title_label.pack(pady=20)

        # Şarkı listesi için kaydırma çerçevesi
        self.canvas = tk.Canvas(self.main_frame, bg="#282828", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.songs_frame = ttk.Frame(self.canvas, style="Custom.TFrame")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack widgets
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Canvas içine frame yerleştirme
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.songs_frame, anchor="nw")

        # Scroll olayları
        self.songs_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Butonlar çerçevesi
        self.buttons_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.buttons_frame.pack(fill=tk.X, pady=10)

        # Butonlar
        self.refresh_button = ttk.Button(self.buttons_frame,
                                       text="Önerileri Yenile",
                                       style="Custom.TButton",
                                       command=self.refresh_recommendations)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.liked_songs_button = ttk.Button(self.buttons_frame,
                                           text="Beğenilen Şarkılar",
                                           style="Custom.TButton",
                                           command=self.show_liked_songs)
        self.liked_songs_button.pack(side=tk.LEFT, padx=5)

        self.create_playlist_button = ttk.Button(self.buttons_frame,
                                               text="Çalma Listesi Oluştur",
                                               style="Custom.TButton",
                                               command=self.create_new_playlist)
        self.create_playlist_button.pack(side=tk.LEFT, padx=5)

        # Şarkı önerilerini yükle
        self.current_recommendations = []
        self.refresh_recommendations()

        # Pencere kapatıldığında çalan müziği durdur
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def load_album_image(self, image_url):
        try:
            response = requests.get(image_url)
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize((100, 100), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img_data)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def play_preview(self, preview_url, play_button):
        if self.current_preview:
            pygame.mixer.music.stop()
            self.current_preview = None
            play_button.configure(text="▶")
            return

        if preview_url:
            try:
                response = requests.get(preview_url)
                with open("temp_preview.mp3", "wb") as f:
                    f.write(response.content)
                
                pygame.mixer.music.load("temp_preview.mp3")
                pygame.mixer.music.play()
                self.current_preview = preview_url
                play_button.configure(text="⏹")
            except Exception as e:
                print(f"Error playing preview: {e}")
                messagebox.showerror("Hata", "Önizleme oynatılamadı.")
        else:
            messagebox.showinfo("Bilgi", "Bu şarkı için önizleme mevcut değil.")

    def refresh_recommendations(self):
        # Mevcut şarkı widgetlarını temizle
        for widget in self.songs_frame.winfo_children():
            widget.destroy()

        # Yeni önerileri al
        self.current_recommendations = get_random_tracks(10)

        # Her şarkı için bir çerçeve oluştur
        for i, track in enumerate(self.current_recommendations):
            song_frame = ttk.Frame(self.songs_frame, style="Custom.TFrame")
            song_frame.pack(fill=tk.X, pady=10, padx=5)

            # Albüm kapağı
            if track.album_image_url:
                img = self.load_album_image(track.album_image_url)
                if img:
                    img_label = tk.Label(song_frame, image=img, bg="#282828")
                    img_label.image = img
                    img_label.pack(side=tk.LEFT, padx=5)

            # Şarkı bilgileri çerçevesi
            info_frame = ttk.Frame(song_frame, style="Custom.TFrame")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

            # Şarkı numarası ve adı
            title_frame = ttk.Frame(info_frame, style="Custom.TFrame")
            title_frame.pack(fill=tk.X)

            num_label = ttk.Label(title_frame,
                                text=f"{i+1}.",
                                style="Custom.TLabel")
            num_label.pack(side=tk.LEFT)

            song_label = ttk.Label(title_frame,
                                 text=track.name,
                                 style="Custom.TLabel",
                                 font=('Helvetica', 14, 'bold'))
            song_label.pack(side=tk.LEFT, padx=5)

            # Sanatçı ve albüm bilgisi
            artists_label = ttk.Label(info_frame,
                                    text=f"Sanatçı: {', '.join(track.artists)}",
                                    style="Custom.TLabel")
            artists_label.pack(anchor=tk.W)

            album_label = ttk.Label(info_frame,
                                  text=f"Albüm: {track.album_name}",
                                  style="Custom.TLabel")
            album_label.pack(anchor=tk.W)

            # Butonlar çerçevesi
            buttons_frame = ttk.Frame(song_frame, style="Custom.TFrame")
            buttons_frame.pack(side=tk.RIGHT, padx=5)

            # Önizleme butonu
            preview_button = ttk.Button(buttons_frame,
                                      text="▶",
                                      style="Custom.TButton",
                                      width=3,
                                      command=lambda u=track.preview_url, b=None: self.play_preview(u, b))
            preview_button.pack(side=tk.LEFT, padx=2)
            # Command'i güncellemek için button referansını ekle
            preview_button.configure(command=lambda u=track.preview_url, b=preview_button: self.play_preview(u, b))

            # Beğen butonu
            like_button = ttk.Button(buttons_frame,
                                   text="♥",
                                   style="Custom.TButton",
                                   width=3,
                                   command=lambda t=track: self.like_song(t))
            like_button.pack(side=tk.LEFT, padx=2)

    def like_song(self, track):
        save_liked_song(track.format_display())
        messagebox.showinfo("Başarılı", "Şarkı beğenilenler listesine eklendi!")

    def show_liked_songs(self):
        liked_songs = load_liked_songs()
        if not liked_songs:
            messagebox.showinfo("Beğenilen Şarkılar", "Henüz beğenilen şarkı yok.")
            return

        # Yeni pencere oluştur
        liked_window = tk.Toplevel(self.root)
        liked_window.title("Beğenilen Şarkılar")
        liked_window.geometry("600x400")
        liked_window.configure(bg="#282828")

        # Şarkıları listele
        for i, song in enumerate(liked_songs, 1):
            song_label = ttk.Label(liked_window,
                                 text=f"{i}. {song}",
                                 style="Custom.TLabel")
            song_label.pack(pady=5)

    def create_new_playlist(self):
        if not self.current_recommendations:
            messagebox.showinfo("Bilgi", "Önce şarkı önerileri alın.")
            return

        playlist_name = tk.simpledialog.askstring("Playlist Oluştur",
                                                "Playlist adını girin:",
                                                parent=self.root)
        if playlist_name:
            track_uris = [track.uri for track in self.current_recommendations]
            create_playlist(playlist_name, track_uris)
            messagebox.showinfo("Başarılı",
                              f"'{playlist_name}' adlı playlist oluşturuldu!")

    def on_closing(self):
        if self.current_preview:
            pygame.mixer.music.stop()
        if os.path.exists("temp_preview.mp3"):
            try:
                os.remove("temp_preview.mp3")
            except:
                pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MusicSuggestionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
