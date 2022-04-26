# Macro Prototype

This project demonstrates a simple macro prototype that allows the user to create a list of instructions for the program to execute. Each action can be configured.

## Installation

Create a Python 3 virtual environment (preferably 3.8+) and install the `requirements.txt` file's contents.
```bash
pip install -r requirements.txt
```

## Usage

Just run the `main.py` file. You will be greeted with the user-interface.

![The GUI](https://i.imgur.com/F1oNhTr.png)

The "Add / Edit Action" section allows the user to create an action and add it to the sequence of actions that the program will execute. Once the parameters are defined, the user can add the action or reset to default field values. In this section, the user can also save/load sequences, as well as configurable shortcut keys.

The "List of Action(s) to Execute in Sequence" section allows the user to see which actions will be executed by the program. The user can start the execution, re-order the actions in the sequence by moving them up or down, or completely deleting the action from the sequence.

The "Configurable Global Shortcut Keys for this Script" section allows user to set shortcuts for getting the mouse position and starting/stopping the script's execution. The first one is super useful, since we cannot expect the user to accurately estimate the co-ordinates on the screen.

## Future plans
Might need to consider making the project more structured. Currently, all classes and functions lie in the same `main.py` file, which is hard to debug/improve upon in the future. Other than that, might also consider adding more actions to the list, such as double-click or action-parameters, such as key-hold duration.

## Contributing
If you face any issues or would like to improve on something, feel free to open an issue and create a pull request.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
