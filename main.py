import  os
import  threading
import  time
import  tkinter.messagebox
import  tkinter as Tkinter

from    tkinter import filedialog
from    tkinter import ttk
from    ttkthemes import ThemedTk
from    mutagen.mp3 import MP3
from    pygame import mixer
from    PIL import ImageTk, Image
from    mutagen.id3 import ID3
from    mutagen.easyid3 import EasyID3
from    io import BytesIO

class MusicPlayerApplication:
    def __init__(self, tkApp, **kwargs):
        
        self.playlist = []
        self.filename_path = ''
        self.paused = False
        self.tkApp = tkApp
        self.album_art_size = (256, 256)
        self.base_elem_row = 0

        tkApp.title("Python Music Player")

        # initializing the mixer
        mixer.init()

        # Calculate Window Size and Pose
        # WindowWidth = 300
        # WindowHeight = 200
        # WindowHorizontalPos = int( mainWindow.winfo_screenwidth()/2 - WindowWidth/2)
        # WindowVerticalPos = int( mainWindow.winfo_screenheight()/2 - WindowHeight/2)

        # Set Window Size and Pose
        # mainWindow.geometry(f'{ WindowWidth }x{ WindowHeight }+{ WindowHorizontalPos }+{ WindowVerticalPos }')

        # Bottom Statusbar Style
        StatusbarStyle = ttk.Style()
        StatusbarStyle.configure("BW.TLabel", foreground="black", font='Roboto 10 italic')
        self.Statusbar = ttk.Label(tkApp, text="Welcome To My Music Player", style="BW.TLabel")
        self.Statusbar.grid(row=self.base_elem_row+3, column=1, columnspan=2)
        # self.Statusbar.pack(side="bottom", fill="x")

        # Create the Menubar
        # Create Application Main Label
        ApplicationMenu = Tkinter.Menu(tkApp)

        # Create Play List Box as Frame
        self.play_list_box = Tkinter.Listbox(tkApp)
        self.play_list_box.grid(row=self.base_elem_row, column=1, columnspan=2)
        
        # Create Application SubMenu
        filemenu = Tkinter.Menu(ApplicationMenu, tearoff=0)
        filemenu.add_command(label="Open", command = self.browse_file)
        filemenu.add_separator()
        filemenu.add_command(label="Close", command = tkApp.destroy )
        
        # Submit Application Menu
        ApplicationMenu.add_cascade(label="File", menu = filemenu)
        tkApp.config( menu=ApplicationMenu )

        img = ImageTk.PhotoImage(  Image.open("poster.jpg").resize( self.album_art_size ) )
        self.panel = ttk.Label( self.tkApp, image = img)
        self.panel.grid(row=self.base_elem_row+1, column=1, columnspan=2)
        # self.panel.pack(side = "bottom", fill = "both", expand = "yes")

        # Create Stop Buttons
        stop_button = Tkinter.Button(tkApp, text='Stop', width=15, command=tkApp.destroy)
        stop_button.grid(row=self.base_elem_row+2, column=1)

        # Create Play Buttons
        stop_button = Tkinter.Button(tkApp, text='Play', width=15, command=self.play_music)
        stop_button.grid(row=self.base_elem_row+2, column=2)
        # stop_button.pack()

        # Show App Window
        self.tkApp.bind("<Return>", self.change_music_cover)
        self.tkApp.protocol("WM_DELETE_WINDOW", self.on_closing)
        tkApp.mainloop()

    # Extract Album Art as New File And Save it in Same Directory  
    def save_album_art(self, msg):
        im = Image.open( BytesIO( msg ) )
        im.save("Cover.png")
        self.change_music_cover("Cover.png")
        

    # Change the Music Player Album Art in Main App Window
    def change_music_cover(self, img):
        img2 = ImageTk.PhotoImage( Image.open(img).resize( self.album_art_size ) )
        self.panel.configure(image=img2)
        self.panel.image = img2

    # playlist - contains the full path + filename
    # playlistbox - contains just the filename
    # Fullpath + filename is required to play the music inside play_music load function
    def browse_file(self):
        self.filename_path = filedialog.askopenfilename()
        self.add_to_playlist( self.filename_path )

        mixer.music.queue( self.filename_path )

    # Add New Selected Song To Playlist
    def add_to_playlist(self, file_path):
        filename = os.path.basename(file_path)
        music_tag = EasyID3(file_path)
        play_list_file_name =  str( music_tag['artist'][0] ) + ' - ' + str( music_tag['title'][0] )
        index = 0
        self.play_list_box.insert(index, play_list_file_name)
        self.playlist.insert(index, self.filename_path)
        index += 1

    # Play The Music And Read MP3 Tags
    def play_music(self):

        if self.paused:
            mixer.music.unpause()
            self.paused = False
        else:
            try:
                time.sleep(1)
                selected_song = self.play_list_box.curselection()
                selected_song = int(selected_song[0])
                play_it = self.playlist[ selected_song ]
                try:
                    music_tag = EasyID3(play_it)
                    music_tag_id3 = ID3(play_it)
                    pict = music_tag_id3.get("APIC:").data
                    self.save_album_art( pict )
                    self.Statusbar['text'] = str( music_tag['artist'][0] ) + ' - ' + str( music_tag['title'][0] )
                except Exception as err:
                    print( err )
                mixer.music.load(play_it)
                mixer.music.play()
            except:
                tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')

    def stop_music(self):
        mixer.music.stop()

    # Stop Music Before Application Closed
    # Destroy Application Window
    def on_closing(self):
        self.stop_music()
        self.tkApp.destroy()


if __name__ == '__main__':
    mainWindow = Tkinter.Tk()
    MusicPlayerApplication( mainWindow )
else:
    print(__name__)
