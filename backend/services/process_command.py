"""
A service to get return the output of a command
"""
import subprocess

from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def run(command):
    """
    The method to run a terminal command
    command: (String) A terminal command
    return: macOS version
    """
    command = command.split()

    if "|" in command:
        size = len(command)
        pipe_indices = [index + 1 for index, val in enumerate(command) if val == "|"]

        commands = [
            command[i:j]
            for i, j in zip(
                [0] + pipe_indices,
                pipe_indices + ([size] if pipe_indices[-1] != size else []),
            )
        ]

        for list in commands:
            if "|" in list:
                list.remove("|")
            quote_indices = [index + 1 for index, val in enumerate(list) if "'" in val]
            if len(quote_indices) == 2:
                list[quote_indices[0] - 1 : quote_indices[1]] = [
                    " ".join(list[quote_indices[0] - 1 : quote_indices[1]])
                ]
            i = commands.index(list)
            list = [s.replace("'", "") for s in list]
            commands[i] = list

        p = subprocess.run(commands[0], capture_output=True)
        for command in commands[1:-1]:
            p = subprocess.run(command, input=p.stdout, capture_output=True)
        p = subprocess.run(commands[-1], input=p.stdout, capture_output=True)
        out = p.stdout.decode("utf-8")

    else:
        quote_indices = [index + 1 for index, val in enumerate(command) if "'" in val]
        if len(quote_indices) == 2:
            command[quote_indices[0] - 1 : quote_indices[1]] = [
                " ".join(command[quote_indices[0] - 1 : quote_indices[1]])
            ]
        command = [s.replace("'", "") for s in command]

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.stdout.read().decode("utf-8")

    return out

    numCores = -1
    return numCores
