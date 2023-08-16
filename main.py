import re
import time
from prettycli import red, blue, yellow, green, color
from simple_term_menu import TerminalMenu
from models import User, Playlist
from sessions import session


class Main():
    
    current_user = None
    

    def start(self):
        self.clear_screen(44)
        options = ["Login", "Exit"]
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()
    
        if options[menu_index] == "Login":
            self.handle_login()
        else:
            self.exit()
    
    def clear_screen(self,lines):
        print("\n" * lines)
           
    def handle_login(self):
        email = input("Enter Email:\n\n")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):            
            user = User.find_or_create_by(email)
            self.clear_screen(44) 
            
            print(f"Welcome {user.email}\n")                       
            self.current_user = user
            self.user_menu()
        else:
            print(yellow("Invalid!!, Try Again!"))
            time.sleep(2)
            self.start()
            
    def user_menu(self):
        
        options = ["View Playlist", "New Playlist", "Exit" ]
        terminal_menu = TerminalMenu(options)
        menu_index = terminal_menu.show()
        
        print(options[menu_index]) 
        
        if options[menu_index] == "View Playlist":
            self.view_playlist()                
            
         
        if options[menu_index] == "New Playlist":
            name = input("Enter Name of new playlist:\n\n")            
            play = Playlist( name = name , user_id = self.current_user.id)
            session.add(play)
            session.commit() 
            
        else:
            self.exit()  
            
    def view_playlist(self):    
        playlists = self.current_user.playlist
        items = []
            
        for pl in playlists:
            items.append(pl.name) 
                           
        terminal_menu = TerminalMenu(items)
        menu_index = terminal_menu.show()

    
    def exit(self):
        print(red("Bye.."))
        

app = Main()
app.start()
