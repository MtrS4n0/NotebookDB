from model_note import Note, NoteDAO
from kirje import Kirje, KirjeDetails

NOTES = []

class MenuNote:
    def __init__(self, user_id: int, username: str) -> None:
        self.user_id = user_id
        self.username = username
    def showOptions(self) -> None:
        print(f"User '{self.username}' options:")
        print("1 - List notes")
        print("2 - View note")
        print("3 - Add note")
        print("4 - Edit note")
        print("5 - Delete note")
        print("0 - Logout")
        return None
    def askChoice(self) -> int:
        choice: int = -1
        feed = input("Your choice: ")
        if feed.isdigit():
            choice = int(feed)
        return choice
    def activate(self) -> None:
        while True:
            self.showOptions()
            choice = self.askChoice()
            if choice == 0:
                print("")
                break
            elif choice == 1: # Amount of options?
                self.listNotes()
            elif choice == 2:
                self.viewNotes()
            elif choice == 3:
                self.addNote()
            elif choice == 4:
                self.editNote()
            elif choice == 5:
                self.deleteNote()
            else:
                print("Unknown option.")
        return None
    
    def listNotes(self) -> None:
        notes = NoteDAO.getNotes(self.user_id)
        if len(notes) == 0:
            print("There are no notes.")
            print("")
            return
        else:
            rows: list[str] = []
            for note in notes:
                rows.append(f"{note.id} - {note.title}")
                content = '\n'.join(rows)
        kirje_details = KirjeDetails(
            content = content,
            header_separation= " - ",
            headers = {
                "ID": "Title  ",
                "title": " notes "
            },
        )
        memo_list = Kirje(kirje_details)
        memo_list.display(style="streamlined")
        print("")
        rows: list[str] = []
        return None
    def viewNotes(self) -> None:
        ask_title = input("Search note by title: ")
        note = NoteDAO.getOneNote(self.user_id, ask_title)
        if note is None:
            print("Not found.")
            print("")
        else:
            memo_details = KirjeDetails(
                content = note.content,
                headers = {
                    "title": note.title, 
                    "ID": note.id,
                    }, 
                header_separation = " - "
            )
            current_memo = Kirje(memo_details)
            current_memo.display(style="default")
            print("")
        return None
    def addNote(self) -> None:
        ask_title = input("Insert title: ")
        feed = input("Insert the amount of rows: ")
        try:
            ask_rows = int(feed)
        except ValueError:
            print("Invalid number of rows.")
            return
        rows: list[str] = []
        for row in range(ask_rows):
            feed = input(f"Insert row {row + 1}: ")
            rows.append(feed)
        separator = "\n"
        note = separator.join(rows)
        memo = Note(len(NOTES) + 1, ask_title, note)
        NoteDAO.addNote(self.user_id, memo.title, memo.content)
        rows: list[str] = []
        print("Note stored!\n")
        return None
    def editNote(self) -> None:
        ask_title = input("Insert note title: ")
        note = NoteDAO.getOneNote(self.user_id, ask_title)
        if note is None:
            print(f"'{ask_title}' not found.")
            print("")
        else:
            rows = note.content.split("\n")
            ask_row = int(input(f"Insert row number to edit 1-{len(rows)}, 0 to cancel: "))
            index = ask_row - 1
            if index == -1:
                print("Cancelled.")
                return
            elif 1<= ask_row <= len(rows):
                replace_row = input("Insert replacement row: ")
                rows[index] = replace_row
                note.content = "\n".join(rows)
                NoteDAO.editNote(self.user_id, note)
                print("Edit completed!")
                print("")
            else:
                print("Invalid row number.")
                print("")
        rows: list[str] = []
        return None
    def deleteNote(self) -> None:
        ask_title = input("Delete note (insert title): ")
        deleted_rows = NoteDAO.deleteNote(self.user_id, ask_title)
        if deleted_rows == 1:
            print("Note deleted.")
            print("")
        else:
            print(f"'{ask_title}' not found.")
            print("")
        return None

