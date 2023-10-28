"""This module contains functions that ask the user for input and return the corresponding value"""
import inspect

from minmax.bokuagent import ABNMBokuAgent, BokuAgent

def get_player_agent(color) :
    """This function asks the user if the player is an AI and returns the corresponding agent"""

    agent = None
    agent_choice = ""

    agent_dict = {}
    for subclass in BokuAgent.__subclasses__():
        agent_dict[subclass.__name__] = subclass

    for subclass in ABNMBokuAgent.__subclasses__():
        agent_dict[subclass.__name__] = subclass

    agent_list = list(agent_dict.keys())

    # get agent type
    while agent_choice not in agent_dict:
        agent_choice = input(f"Available agents are: {str(agent_list)}.\nwhat agent is {color}? ")

        if agent_choice not in agent_dict:
            print(f"{agent_choice} is not a valid agent")

    # get additional parameters, then initialize the agent
    if issubclass(agent_dict[agent_choice], ABNMBokuAgent):
        depth = get_int(f"to what depth should {color} search? ", 1, 10)
        agent = agent_dict[agent_choice](color, depth)
    else:
        agent = agent_dict[agent_choice](color)

    return agent

def get_int(prompt: str, min_val: int, max_val: int) -> int:
    """This function asks the user for an integer between min_val and max_val"""

    int_val = None
    error_str = f"please enter an integer between {min_val} and {max_val}"
    while int_val is None:
        try:
            int_val = int(input(prompt))
            if int_val < min_val or int_val > max_val:
                print(error_str)
                int_val = None
        except ValueError:
            print(error_str)

    return int_val

def get_y_or_n(prompt: str) -> bool:
    """This function asks the user for a yes or no answer and returns a bool"""

    y_or_n = None
    while y_or_n is None:
        answer = input(prompt)
        if answer == "y":
            y_or_n = True
        elif answer == "n":
            y_or_n = False
        else:
            print("please enter y or n")

    return y_or_n

def get_inputs_for_function(func):
    """This function asks the user for the parameters of a function.
       it returns a dictionary of the parameters and their values"""
    parameters = inspect.signature(func)
    user_inputs = {}

    for param,  in parameters:
        user_input = input(f"Please enter {param}: ")
        user_inputs[param] = user_input

    return user_inputs
