'''
This module provides the presentation layer and can be consdired "the program."

This module facilitates an infinite loop that:
1. Clears the screen
2. Prints the menu options
    (A) Add a bookmark
    (B) List bookmarks by date
    (T) List bookmarks by title
    (D) Delete a bookmark
    (Q) Quit
3. Gets the user’s choice
    When chosen, use an Option class to match selection to command to
    1. Run the specified preparation step, if any.
    2. Pass the return value from the preparation step, if any, to the specified command’s execute method.
    3. Print the result of the execution. These are the success messages or bookmark results returned from the business logic.
4. Clears the screen and executes the command corresponding to the user’s choice
5. Waits for the user to review the result, pressing Enter when they’re done

Room to grow.  

This modular design, which separates concerns, provides opportunities for extensibility, making it possible to:
1. Add any new database manipulation methods you may need to database.py.
2. Add a command class that performs the business logic you need in commands.py.
3. Hook up the new command to a new menu option in barky.py.

'''
import os

import commands

class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.name


def print_options(options):
    '''
    1. Print the keyboard key for the user to enter to choose the option.
    2. Print the option text.
    3. Check if the user’s input matches an option and, if so, choose it.    
    '''
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    '''
    1. Prompt the user to enter a choice, using Python’s built-in input function.
    2. If the user’s choice matches one of those listed, call that option’s choose method.
    3. Otherwise, repeat.    
    '''
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
        choice = input('Choose an option: ')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False),
    }


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete')


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)

def loop():
    # All steps for showing and selecting options
    # https://www.w3schools.com/python/python_dictionaries.asp
    options = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion),
        'Q': Option('Quit', commands.QuitCommand()),
    }
    clear_screen()
    print_options(options)    
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()
    _ = input('Press ENTER to return to menu')


# this ensures that this module runs first 
if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()

    # endless program loop
    while True:
        loop()

