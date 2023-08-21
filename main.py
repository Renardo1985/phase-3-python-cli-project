import re
import sys
import time
from prettycli import red, blue, yellow, green, color
from simple_term_menu import TerminalMenu
from models import User, Playlist, Songs
from sessions import session


class Main():
    
    current_user = None 
    current_playlist = None   

    def start(self):
        self.clear_screen(44)
        options = self.terminal_cli(["Login","Exit"])    
        if options == "Login":
            self.handle_login()
            return 0            
        if options == "Exit":
            self.exit()           
     
                       
    def handle_login(self):
        email = input("Enter Email: ")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):            
            user = User.find_or_create_by(email)
            self.clear_screen(44) 
            
            print(f"Welcome {user.email}\n")                       
            self.current_user = user
            self.user_menu()
            return 0
        else:
            print(yellow("Invalid email address!!, Please try Again!"))
            time.sleep(2)
            self.start()
            
 
            
    def user_menu(self):        
        
        options = self.terminal_cli(["View Playlist", "New Playlist", "Logout", "Exit" ]) 
        
        if options == "View Playlist":
            self.view_playlist()   
            return 0
         
        if options == "New Playlist":
            name = input(green("Enter Name of new playlist:\n\n"))
            if name:
                #creates new playlist                 
                pl = Playlist.create_playlist(name,self.current_user.id)
                print (pl)         
            
            else:
                print(red("Please enter a valid playlist name\n")) 
            
            self.user_menu()
            return 0         
            
        if options == "Logout":            
            self.start()  
            return 0
        
        if options == "Exit":
            self.exit()
            
    def view_playlist(self):    
        items = []
        playlists = self.current_user.playlist        
        
        if not playlists:
            print(yellow("You have no playlists\n"))
            return 0
        
        else:        
            for pl in playlists:
                items.append(pl.name)
                 
            items.append("🔙 Back")        
            options = self.terminal_cli(items)
            
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
        
        options1 = self.terminal_cli(["➕ Add Song", "➖ Remove Song","❌ Delete playlist","🔙 Back"])
                
        if options1 == "➕ Add Song":
            self.add_songs()    
            
        if options1 == "➖ Remove Song":
            self.remove_song()
            
        if options1 == "❌ Delete playlist":                     
            pl = session.query(Playlist).get(self.current_playlist.id)
            
            print(red(f"Delete {pl.name} Playlist")) 
                       
            io = self.terminal_cli(["✅ Yes","❌ No"])         
            
            if  io == "✅ Yes":
                session.delete(pl)
                session.commit()
                print(red("Deleted playlist...\n"))
                self.user_menu()
                return 0
            
            if io == "❌ No":
                self.playlist_menu()
                return 0            
       
        if options1 == "🔙 Back":
            self.view_playlist()
            return 0

    def add_songs(self):
        
        all_tracks = session.query(Songs).all()
        print(all_tracks) 
        print("\n")
            
        options = self.terminal_cli(["Search Track","Search Artist","🔙 Back"])
        
        if options == "Search Track":            
            title = input(green("\nEnter title: "))
            
            if title:
                song = Songs.find_song_by_title(title) 
                 
                if song is None:
                    print(red("Track Not found!")) 
                    time.sleep(2)
                    self.playlist_menu()  
                    return 0
                
                if song: 
                    print(song)               
                    print(yellow("-- Add Song? --"))
                    opt = self.terminal_cli(["✅ Yes","❌ No"])
                                
                    if opt == "✅ Yes":
                        self.current_playlist.songs.append(song)
                        session.commit()
                
                        print(green(f"\n{song.title} added!..."))
                        time.sleep(2)
                        self.playlist_menu() 
                        return 0 
                
                    if opt == "❌ No":
                        self.playlist_menu()  
                        return 0 
            
            else:
                print(red("Enter valid Title"))
                time.sleep(2)
                self.playlist_menu()  
                return 0
            
        if options == "Search Artist":   
            artist = input(green("\nEnter Artist: "))
            
            if artist:
                s_list = Songs.songs_by_artist(artist) 
                
                if s_list is None:
                    print(red("Track Not found!")) 
                    time.sleep(2)
                    self.playlist_menu()  
                    return 0
                
                if s_list: 
                    print(s_list) 
                    print("\n")  
                    opt = self.terminal_cli(["Add All","Add One"])
                                
                    if opt == "Add All":
                        for track in s_list:
                            self.current_playlist.songs.append(track)
                         
                        session.commit()
                
                        print(green("\nSongs added!..."))
                        time.sleep(2)
                        self.playlist_menu() 
                        return 0  
                
                    if opt == "Add One":
                        t_name = []
                        for tracks in s_list:
                            t_name.append(tracks.title)
                    
                    opt = self.terminal_cli(t_name)
                                        
                    song = Songs.find_song_by_title(opt) 
                    self.current_playlist.songs.append(song)
                    session.commit()
                
                    print(green(f"\n{song.title} added!..."))
                    time.sleep(2)
                    self.playlist_menu() 
                    return 0 
            
            else:
                print(red("Enter valid Artist"))
                time.sleep(2)
                self.playlist_menu()  
                return 0
        
        if options == "🔙 Back": 
            self.playlist_menu()
            return 0
        
            
            
    def remove_song(self):
       
        track_list = self.current_playlist.songs
        
        if track_list:
            tracks = []
            for t in track_list:
                tracks.append(t.title)
        
            #import ipdb; ipdb.set_trace()
            tracks.append("Remove all")
            selected_track = self.terminal_cli(tracks)
            
            
            if selected_track == "Remove all":
                self.current_playlist.songs.clear()
                session.commit()
                
                self.playlist_menu()
            
            else:
                for ele in track_list:
                    if ele.title == selected_track:
                        del_this = session.query(Songs).get(ele.id)

                self.current_playlist.songs.remove(del_this)
                session.commit()
                print("Removed")
 
                # import ipdb; ipdb.set_trace()
                self.playlist_menu()
                 
                

           
    def exit(self):
        print(red("GoodBye.."))
        sys.exit(0)
        
    def clear_screen(self,lines):
        print("\n" * lines)
        
    def terminal_cli(self,options):
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()
        return options[menu_index]

        

app = Main()
app.start()