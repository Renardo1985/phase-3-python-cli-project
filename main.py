import re
import sys
import time
import pwinput
from prettycli import red, blue, yellow, green, color
from simple_term_menu import TerminalMenu
from models import User, Playlist, Songs
from api_search import find_by_artist, find_by_title
from sessions import session



class Main():
    
    def __init__(self) -> None:
        self.current_user = None 
        self.current_playlist = None   

    def start(self):
        # self.clear_screen(44)
        options = self.terminal_cli(["Login","Register","Exit"],True)    
        
        if options == "Login":
            self.handle_login()
            return 0
        if options == "Register":
            self.reg_user()
            return 0           
        if options == "Exit" or options is None:
            self.exit() 
        
                      
    
    def reg_user(self):
        print(blue("Register New User\n"))
        email = input("Enter Email: ")
        if self.verify_email(email):            
            password = input("Enter Password: ")
            
            if password:
                User.register_user(email,password)
                user = session.query(User).filter(User.email == email).first()
                print(f"Created {user.email}")
                time.sleep(2)
                self.handle_login() 
            else:
                print(red("You must enter a password!"))
                time.sleep(2)
                self.start() 
        else:
            print(yellow("Invalid email address!!, Please try Again!"))
            time.sleep(2)
            self.start()        
            
            
                       
    def handle_login(self):
        self.clear_screen(2)
        print(blue("Login\n"))
        email = input("Enter Email: ")
        if self.verify_email(email):            
            user = User.find_user(email)
            if user:
                pass_input = pwinput.pwinput("Enter Password: ")
                auth = User.authenticate_user(email,pass_input)
                if auth:
                    self.clear_screen(44) 
                    print(f"Welcome {auth.email}\n")                       
                    self.current_user = auth
                    time.sleep(2)
                    self.user_menu()
                    return 0
                else:
                    print(red("Authentication failed."))
                    time.sleep(2)
                    self.start()
            else:
                print(red("User does not exist."))
                time.sleep(2)
                self.start()
        else:
            print(yellow("Invalid email address!!, Please try Again!"))
            time.sleep(2)
            self.start()
            
 
            
    def user_menu(self):        
        
        # self.clear_screen(50)
        options = self.terminal_cli(["View Playlist", "New Playlist", "Logout", "Exit" ],True)         
        if options == "View Playlist":
            self.view_playlist()   
            return 0
         
        if options == "New Playlist":
            name = input(green("Enter Name of new playlist:\n\n"))
            if name:                 
                pl = Playlist.create_playlist(name,self.current_user.id) #creates new playlist
                print (pl)         
            
            else:
                print(red("Please enter a valid playlist name\n")) 
            
            self.user_menu()
            return 0         
            
        if options == "Logout":            
            self.start()  
            return 0
        
        if options == "Exit" or options is None:
            self.exit()
            
    def view_playlist(self):    
        items = []
        playlists = self.current_user.playlist #all playlists for current user   
        
        if not playlists:
            print(yellow("You have no playlists\n"))
            time.sleep(1)
            self.user_menu()
        
        else:        
            for pl in playlists:
                items.append(pl.name)
                 
            items.append("🔙 Back")        
            options = self.terminal_cli(items,False)
            
            if options == "🔙 Back":               
                self.user_menu() 
                return 0           
            
            else:
                
                playlist = session.query(Playlist).filter_by(user_id = self.current_user.id).filter_by(name=options).first()
                self.current_playlist = playlist
                self.playlist_menu()       
        
  
        
    def playlist_menu(self):
        
        self.clear_screen(50)
        print(green(f"✅ You selected {self.current_playlist.name} playlist"))
        print(blue("Tracks:"))
        if self.current_playlist.songs:
            print(f"{self.current_playlist.songs}\n")
        else:
            print(yellow("No tracks added yet!\n"))
        
        options = self.terminal_cli(["➕ Add Song", "➖ Remove Song","❌ Delete playlist","🔙 Back"],False)
                
        if options == "➕ Add Song":
            self.add_songs_menu() 
            return 0   
            
        if options == "➖ Remove Song":
            self.remove_song()
            return 0 
            
        if options == "❌ Delete playlist":                     
            pl = session.query(Playlist).get(self.current_playlist.id)            
            print(red(f"Delete {pl.name} Playlist"))                        
            io = self.terminal_cli(["✅ Yes","❌ No"])         
            
            if  io == "✅ Yes":
                session.delete(pl)
                session.commit()
                self.current_playlist = None
                print(red("Deleted playlist...\n"))
                self.user_menu()
                return 0
            
            if io == "❌ No":
                self.playlist_menu()
                return 0            
       
        if options == "🔙 Back" or options is None:
            self.view_playlist()
            return 0

    def add_songs_menu(self):
        
        options = self.terminal_cli(["Search Title","Search Artist","🔙 Back"],False)
        
        if options == "Search Title":            
            title = input(green("\nEnter title: "))
            
            if title:
                # songs = Songs.find_song_by_title(title)
                songs = find_by_title(title) #search itunes music API
                self.add_songs(songs)
            
            else:
                print(red("Enter valid Title"))
                time.sleep(2)
                self.playlist_menu()  
                return 0
        
        if options == "Search Artist":   
            artist = input(green("\nEnter Artist: "))
            
            if artist:
                # songs = Songs.songs_by_artist(artist) 
                songs = find_by_artist(artist) #search itunes music API
                self.add_songs(songs)
            
            else:
                print(red("Enter valid artist"))
                time.sleep(2)
                self.playlist_menu()  
                return 0
        
        if options == "🔙 Back" or options is None: 
            self.playlist_menu()
            return 0
        
    def add_songs(self,song_list):
         
        if song_list: 
            tracks = []
            for track in song_list:
                tracks.append(str(track))
            
            terminal_menu = TerminalMenu(tracks,multi_select=True,show_multi_select_hint=True)
            selected_track = terminal_menu.show() 
                    
            if selected_track: 
                for index in selected_track:
                    test = Songs.song_exists(song_list[index]) #tests if the song(s) selected to be added to the playlist exists in the Songs DB
                    if test:
                        self.current_playlist.songs.append(test) #appends song to playlist from the DB if it exists
                    else:
                        session.add(song_list[index]) #adds song to the DB if it does not exist.
                        self.current_playlist.songs.append(song_list[index]) #adds songs to playlist
                        
                print(green("\nSong(s) added!..."))
                session.commit()
                time.sleep(2)
                self.playlist_menu() 
                return 0 
                
            else:
                print(red("No selection"))
                self.playlist_menu()  
                return 0 
                    
        else:
            print(red("Track Not found!")) 
            time.sleep(2)
            self.playlist_menu()  
            return 0
            
                   
            
    def remove_song(self):
       
        track_list = self.current_playlist.songs        
        
        if track_list:
            tracks = []
            for t in track_list:
                tracks.append(str(t))
                
            terminal_menu = TerminalMenu(tracks,multi_select=True,show_multi_select_hint=True)
            selected_track_indices = terminal_menu.show() 

            if selected_track_indices:                
                del_this = []
                # this part took me hours to figure out....
                for i in selected_track_indices:
                    del_this.append(track_list[i])
                    # print(del_this)
 
                for song in del_this:
                    self.current_playlist.songs.remove(song)
                
                print(yellow("Track(s) Removed"))
                session.commit()  
                time.sleep(2)
                self.playlist_menu()
                
            else:
                print(red("No selections"))  
                time.sleep(2)
                self.playlist_menu()
                return 0
        else:
            print(red("\nNo tracks"))
            time.sleep(2)
            self.playlist_menu()
                
            
    def exit(self):
        print(red("GoodBye.."))
        sys.exit(0)
        
    def clear_screen(self,lines):
        print("\n" * lines)
        
    def terminal_cli(self,options,clear = False):
        terminal_menu = TerminalMenu(options,clear_screen = clear)
        menu_index = terminal_menu.show()
        if options[menu_index]:
            return options[menu_index]
        else:
            return None    
    
    def verify_email(self,email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #email verification
        if re.fullmatch(regex, email):
            return True

app = Main()
app.start()