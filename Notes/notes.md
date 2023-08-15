## Project Requirements

- [Phase 3 - Project Requirements](https://my.learn.co/courses/653/pages/phase-3-project-cli?module_item_id=95439)


### the minimum requirements

- A CLI application
  -that solves a real-world problem
  -adheres to best practices
-A database created with SQLAlchemy
  -modified with SQLAlchemy ORM
  -2+ related tables
- A well-maintained virtual environment using Pipenv
- Proper package structure in your application
- Use of lists
- Use of dictionaries.

### stretch goals

- A database created and modified with SQLAlchemy ORM with 3+ related tables.
- Use of many-to-many relationships with SQLAlchemy ORM.
- Use of additional data structures, such as ranges and tuples.

## Project Proposals

### Main idea 

- Project Playlist Creator App
Users can search for songs or artists within the database, add songs to a playlist, view the current playlist, and save the playlist to a file. 

#### User story
The app presents a main menu with options:
"Search song"
"Display playlist"
"Create playlist"
"Exit"

Searching for Songs:
The app prompts the user to enter a song or artist name they want to search for.
The app searches the music database for songs or artists that match the query and displays the search results.

Adding Songs to Playlist:
The user is asked to enter the number of the song they want to add to their playlist

Displaying Playlist:
The app shows the current contents of the playlist, listing the title and artist of each song.

Saving Playlist:
The app saves the playlist to a text file named "playlist.txt" in the same directory as the app's files.

Exiting the App:
The app displays a message and terminates.

#### How I will use the concepts I recently learned to meet the project requirements

### Potential Classes 

class Songs:
class Playlists:

A Song class will represent individual songs with attributes like title, artist, and genre. Objects of the Song class can be used to store song information and interact with the song data.
The Playlist class will manage the user's playlist. Objects of the Playlist class can store a list of Song objects and provide methods to add, display, and save songs.


### Database Tables:
Songs Table:
id
title
artist
genre

Playlist Table:
id
name
songs

Song and Playlist: relationship Many-to-Many, a song can be in multiple playlists, and a playlist can contain multiple songs.

### Potential methods:

Query Songs by Genre:
This method queries the database to retrieve songs based on a specific genre.

Query Playlists with Songs:
This method queries the database to retrieve playlists along with the songs in each playlist.

Create a Playlist:
This method creates a new playlist in the database.

Add Song to Playlist:
This method adds a song to a specific playlist.

Get Playlist by Name:
This method retrieves a playlist by its name.

Delete Playlist:
This method deletes a playlist from the database.

### Data Structure:
list to store instances of the Song class, representing the songs in the app. This list can be used to display search results, manage the playlist, and perform various operations involving songs.
Also a list to represent the playlist. The list would contain references to the Song objects that are added to the playlist.

### What area I think will be most challenging 

- Migrations