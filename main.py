import re
import sys
import time

from prettycli import red, blue, yellow, green, color
from simple_term_menu import TerminalMenu
from models import User, Playlist
from sessions import session


class Main():
    
    current_user = None 
    current_playlist = None   

    def start(self):
        self.clear_screen(44)
        options = ["Login", "Exit"]
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()
    
        if options[menu_index] == "Login":
            self.handle_login()
            return 0
            
        if options[menu_index] == "Exit":
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
        
        options = ["View Playlist", "New Playlist", "Logout" ]
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()
        
        print(options[menu_index]) 
        
        if options[menu_index] == "View Playlist":
            self.view_playlist()   
            return 0
         
        elif options[menu_index] == "New Playlist":
            name = input(green("Enter Name of new playlist:\n\n"))
            if name:
                #creates new playlist                 
                pl = Playlist.create_playlist(name,self.current_user.id)
                print (pl)
            
            
            else:
                print(red("Please enter a valid playlist name\n")) 
            
            self.user_menu()
            return 0         
            
        elif options[menu_index] == "Logout":            
            self.start()  
            return 0
            
 
            
    def view_playlist(self):    
        items = []
        playlists = self.current_user.playlist        
        
        if not playlists:
            print(yellow("You have no playlists\n"))
            return 0
        
        else:        
            for pl in playlists:
                items.append(pl.name)
                 
            items.append("❌ Exit")   
                       
            terminal_menu = TerminalMenu(items)
            menu_index = terminal_menu.show()
            
            if items[menu_index] == "❌ Exit":
               
                self.user_menu() 
                return 0           
            
            else:
                print(green(f"✅ You selected {items[menu_index]} playlist\n"))
                playlist = session.query(Playlist).filter_by(user_id = self.current_user.id).filter_by(name=items[menu_index]).first()
                self.current_playlist = playlist
                self.playlist_menu()       
        
  
        
    def playlist_menu(self):
        
        options = ["➕ Add Songs", "➖ Remove Songs","❌ Delete playlist","🔙 Back"]
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()
        
        if options[menu_index] == "➕ Add Songs":
            pass
        if options[menu_index] == "➖ Remove Songs":
            pass
        if options[menu_index] == "❌ Delete playlist":
            pl = session.query(Playlist).get(self.current_playlist.id)
            
            io = input(red(f"Delete {pl.name} Playlist  Y/N :"))         
            
            
            if  io == "y" or io == "Y":
                session.delete(pl)
                session.commit()
                print(red("Deleted playlist...\n"))
                self.playlist_menu()
                return 0
            if io == "n" or io == "N":
                self.playlist_menu()
                return 0
            else:
                print(red("Invalid Option... Aborting...\n"))
                self.playlist_menu()
                return 0
            
        #import ipdb; ipdb.set_trace()
        if options[menu_index] == "🔙 Back":
            self.view_playlist()
            return 0

    
    def exit(self):
        print(red("GoodBye.."))
        sys.exit(0)
        
    def clear_screen(self,lines):
        print("\n" * lines)
        

app = Main()
app.start()
