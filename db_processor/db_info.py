# -*- coding: utf-8 -*-

from colored import fg, attr
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import requests
import regex

"""
    Color definition.
"""
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

style = style_from_dict({
    Token.QuestionMark: '#B54653 bold',
    Token.Selected: '#86DEB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#46B1C9 bold',
    Token.Question: '',
})


class NotEmpty(Validator):
    def validate(self, document):
        ok = document.text != "" and document.text != None
        if not ok:
            raise ValidationError(
                message='Please enter something',
                cursor_position=len(document.text))  # Move cursor to end


class AddressValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'(\d{1,3}\.){3}\d{1,3}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid IP address.',
                cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'\d+', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid port number.',
                cursor_position=len(document.text))  # Move cursor to end


def db_specification():
    """
    Asks the user to enter the necessary information (server address, port number and repository name) to access the database.

    Returns
    -------
    dict
        The database information (server address, port number and repository name).

    """
    db_specification_question = [
        {
            'type': 'input',
            'message': 'Enter the IP address of the GraphDB server (use format yyx.yyx.yyx.yyx where \'y\' is optional):',
            'name': 'server',
            'validate': AddressValidator
        },
        {
            'type': 'input',
            'message': 'Enter the port number where GraphDB is running:',
            'name': 'port',
            'validate': NumberValidator
        },
        {
            'type': 'input',
            'message': 'Enter the name of the GraphDB repository:',
            'name': 'repository',
            'validate': NotEmpty
        }
    ]

    db_specification_answer = prompt(db_specification_question, style=style)
    return db_specification_answer


def test_db_connection(server, port, repository):
    """
    Tests the access to the database.

    Parameters
    ----------
    server : string
        The IP address of the database server.

    port : string
        The port where the database is running.

    repository : string
        The name of the database repository.

    Returns
    -------
    boolean
        Returns true if the connection was successful and false otherwise.

    """
    global db_url
    db_url = "http://" + server + ":" + port + "/repositories/" + repository

    try:
        s = requests.Session()
        connection = s.get(db_url)
        unknown = regex.search(r'unknown repository',
                               connection.text, regex.IGNORECASE)
        if unknown != None:
            print(red + "\n>>> " + reset +
                  "Unknown repository. Please verify the connection information.")
            return False
        else:
            print(green + "\n>>> " + reset + "Successfully connected.")
            return True
    except requests.exceptions.RequestException:
        print(red + "\n>>> " + reset +
              "Unable to connect to GraphDB. Please verify the connection information.")
        return False


def get_db_info():
    """
    Processes the phases to obtain the information about the database and to test the connection with it.

    Returns
    -------
    dict
        Returns the information (server address, port number and repository name) about the database.
    """
    db_info = db_specification()

    server = db_info.get("server")
    port = db_info.get("port")
    repository = db_info.get("repository")

    connection = test_db_connection(server, port, repository)
    if connection == False:
        return get_db_info()
    else:
        return db_info
