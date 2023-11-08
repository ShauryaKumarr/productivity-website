from drafter import *
from dataclasses import dataclass
# datetime is needed for the timer page
from datetime import datetime, timedelta
from bakery import assert_equal

'''
- www.productivity.com/

- The purpose of this website is to give you three essential tools that are needed during
studying: A to-do list, timer for pomodoro or other study methods, and a note taking sheet
that can be revisited for review. I always had the trouble of pulling up all these different
tools in different locations, so I thought it would be a good idea to have a place where
all three can be used and located on a single webpage.

-Shaurya Kumar, shaurya@udel.edu

-https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
This website was used to help me format the information that was outputted using
the library 'datetime.' Originally, the information was in military time and had no AM/PM
bounds, so using the information I got about strftime(), I used this to format the putput.

-https://www.geeksforgeeks.org/python-datetime-timedelta-function/
I have used datetime before for a previous internship I have done, so I had prior
experience with the library, but I used this website specifically for the timedelta
function. I was not sure how to add the minutes from an input to a datetime method,
so I searched it up and this was the resource I found that helped me tackle this problem.
'''

# Gives the basic headers for the 'view tasks' section
tasklist = [['Task:', 'Due Date:', 'Time Required:', 'Mark Box If Complete']]


@dataclass
class State:
    username: str
    starting_time: str
    ending_time: str
    notes: str


@route
def index(state: State) -> Page:
    ''' First page that greets the user, and asks for their name to be saved
        in state.username (field data). Button on page proceeds you to the
        next page, the selection field.

        Args:
            state(State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.

        Returns:
            Page: introductory page with welcome screen, textbox to enter name,
            and a continue button that leads you to next screen.
    '''
    return Page(state, [
        Header("Welcome.", 1),
        Header("Please enter your name below.", 4),
        TextBox("username", state.username),
        Button("Continue", selection)
    ])


@route
def selection(state: State, username: str) -> Page:
    ''' This is the selection page, a page that contains four buttons:
        A notes area button, a timer button, a to-do list button, and
        a back button. Have to select one of the options to continue.

        Args:
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.
            username (str): takes input from textbox in previous page

        Returns:
            Page: welcome you with your inputted name, and shows you
            four possible options to proceed with.
    '''
    state.username = username
    return Page(state, [
        'Welcome, ' + state.username +
        '. Please select what you would like to use today.',
        Button("Notes Area", note_area),
        Button("Timer", timeselection),
        Button("To-Do List", add_todo_list),
        Button("Back", index)
    ])


@route
def add_todo_list(state: State) -> Page:
    ''' This page is preceded by the selection page. Take you to page
        with three buttons: add task, view task, and back button.

        Args:
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.

        Returns:
            Page: page with three functional buttons, add task, view task, and
            back button.
    '''
    return Page(state, [
        'Please select below on what you want like to do.',
        Button('add task', add_task),
        Button('view tasks', view_task),
        Button('Back', index)])


# where tasks are added
@route
def add_task(state: State) -> Page:
    ''' Preceded by add to-do list page. Page presents three input areas
        for task information, and two buttons: one to add the task, and one
        to go back.

        Args:
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.

        Returns:
            Page: Page with three textboxes to put information into about a task,
            and two buttons that either add a task or go back to a previous page.
    '''
    return Page(state, [
        'What is the task called?',
        TextBox('taskname'),
        'When is the due date?',
        TextBox('taskduedate'),
        'How much time is required? (in mins)',
        TextBox('tasktimereq'),
        # use all references as parameters when creating list
        Button('add this task', finish_add_task),
        Button('Back', add_todo_list)
    ])


@route
def finish_add_task(state: State, taskname: str, taskduedate: str, tasktimereq: str) -> Page:
    ''' function that takes inputs from add_task page, and creates them into a list
        for viewing purposes.

        Args:
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.
            taskname (str): input from the textbox for name
            taskduedate (str): input from the textbox for date
            tasktimereq (str): input for estimated time required to complete activity.

        Returns:
            Page: Takes you back to page with add task & view task button after saving
            data into list.

    '''
    tasklist.append([taskname, taskduedate, tasktimereq + ' mins', CheckBox('taskcomplete')])
    return add_todo_list(state)


@route
def view_task(state: State) -> Page:
    ''' Page that shows a table of the tasks you added. Preceded by add_todo_list
        page.

        Args:
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.
        Returns:
            Page: Page that displays your tasks in a table format with all of
            the information inputted, plus an additional checkbox with a
            mark for completion.
    '''
    return Page(state, [
        'Here are your tasks.',
        # make sure to format table
        Table(tasklist),
        Button('Back', add_todo_list)
    ])


@route
def note_area(state: State) -> Page:
    ''' Takes input from the textbox, and depending on what button is clicked,
        will either save the input, or delete the input.

        Args:
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.
        Returns:
            Page: Page that displays your saved notes or general input that was
            put into the text area.

    '''
    return Page(state, [
        'This is the notes section, and below, you can begin to take your notes.',
        TextArea('notes_entered', state.notes),
        # create gateway to helper function
        Button('Save', save),
        Button("Back", index)
    ])


@route
def save(state: State, notes_entered: str) -> Page:
    '''The save function is used to save the notes that are written down onto a field
        of the class State (state.notes). It takes the notes that are entered within the
        TextArea as an argument, and saves them into state.notes so it is within the class.

        Args:
            notes_entered (str): body that is entered within the TextBox.
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.
        Returns:
            Page: takes you to the note_area page with your information (notes) stored

    '''
    state.notes = notes_entered
    return note_area(state)


@route
def timeselection(state: State) -> Page:
    ''' Function takes input in a textbox, and using the datetime library, displays
        the starting time and ending time that comes from timer input.

        Args:
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.

        Returns:
            Page: page that displays input box and continue button and eventually
            formulates a start and end time using the datetime library.

    '''
    return Page(state, [
        'Please set your timer below in minutes.',
        TextBox("minutes"),
        Button("Continue", timer_page),
        'Your start time:', state.starting_time,
        'Your end time:', state.ending_time,
        Button("Back", index)
    ])


@route
def timer_page(state: State, minutes: str) -> Page:
    ''' The timer page takes the input from the time selection page,
        and based on the validity of the input, uses the datetime
        library to display the current time, and the end time
        (current time + time entered).

        Args:
            minutes(str): input that comes from the TextBox in timeselection
            state (State): gives us the necessary fields to input information
            into, and allows for the functionality of the website as the first
            parameter of start_server should match with every first parameter.

        Returns:
            Page: takes you to timeselection page, with your current time and
            endtime projected. Different output for invalid inputs.
    '''
    if int(minutes) > 0 and minutes.isdigit():
        # minutes is str
        minutes = int(minutes)
        current_time = datetime.now()
        end_time = current_time + timedelta(minutes=minutes)
        state.starting_time = current_time.strftime('%Y-%m-%d %I:%M:%S %p')
        state.ending_time = end_time.strftime('%Y-%m-%d %I:%M:%S %p')
    else:
        state.starting_time = 'Please enter a valid input of time.'
        state.ending_time = 'Please enter a valid input of time.'

        # take route to adjacent page
    return timeselection(state)


# tests if invalid inputs create alternate output with the timer.
assert_equal(timer_page(State('', '', '', ''), '-2'),
             Page(State('', 'Please enter a valid input of time.', 'Please enter a valid input of time.', ''), [
                 'Please set your timer below in minutes.',
                 TextBox("minutes"),
                 Button("Continue", timer_page),
                 'Your start time:', 'Please enter a valid input of time.',
                 'Your end time:', 'Please enter a valid input of time.',
                 Button("Back", index)
             ]))

'''As timer_page uses datetime, I cannot unit test the correct outputs as the
information that is outputted is real-time. However, in the program, the outputted
information is very visibly correct through the use of simple numbers.'''

# makes sure that the inputted argument gets saved into dataclass field.
assert_equal(save(State('', '', '', ''), 'I love computer science'),
             Page(State('', '', '', 'I love computer science'), [
                 'This is the notes section, and below, you can begin to take your notes.',
                 TextArea('notes_entered', 'I love computer science'),
                 Button('Save', save),
                 Button("Back", index)
             ]))

# tests if username gets saved in selection page for proper introduction.
assert_equal(selection(State('', '', '', ''), "Shaurya"),
             Page(State('Shaurya', '', '', ''), [
                 'Welcome, ' + 'Shaurya' + '. Please select what you would like to use today.',
                 Button("Notes Area", note_area),
                 Button("Timer", timeselection),
                 Button("To-Do List", add_todo_list),
                 Button("Back", index)
             ]))

# no needed arguments to start the program.
start_server(State('', '', '', ''))
