import re
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
        else:
            print(yellow("Invalid email address!!, Please try Again!"))
            time.sleep(2)
            self.start()
            
 
            
    def user_menu(self):        
        self.clear_screen(44)
        options = ["View Playlist", "New Playlist", "Logout" ]
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()
        
        print(options[menu_index]) 
        
        if options[menu_index] == "View Playlist":
            self.view_playlist()   
         
        elif options[menu_index] == "New Playlist":
            name = input(green("Enter Name of new playlist:\n\n"))
            if name:
                #creates new playlist                 
                pl = Playlist.create_playlist(name,self.current_user.id)
                print (pl)
            else:
                print(red("Please enter a valid playlist name\n"))          
            
        elif options[menu_index] == "Logout":            
            self.start()  
            
 
            
    def view_playlist(self):    
        items = []
        playlists = self.current_user.playlist        
        
        if not playlists:
            print(yellow("You have no playlists\n"))
        
        else:        
            for pl in playlists:
                items.append(pl.name)
                 
            items.append("❌ Exit")   
                       
            terminal_menu = TerminalMenu(items)
            menu_index = terminal_menu.show()
            
            if items[menu_index] == "❌ Exit":
                self.user_menu()
            
            
            else:
                print(green(f"✅ You selected {items[menu_index]} playlist\n"))
                playlist = session.query(Playlist).filter_by(user_id = self.current_user.id).filter_by(name=items[menu_index]).first()
                self.current_playlist = playlist
                self.playlist_menu()       
        
  
        
    def playlist_menu(self):
        
        options = ["Add Songs", "Remove Songs", "Rename playlist","Delete playlist"]
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()

    
    def exit(self):
        print(red("GoodBye.."))
        
    def clear_screen(self,lines):
        print("\n" * lines)
        

app = Main()
app.start()
