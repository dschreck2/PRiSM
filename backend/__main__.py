"""
The main file to store PRiSM data in the database
"""

from core import generate_log as logger
from core import read_config
from services import host  # cpu, disk, process, ram


@logger.wrap(logger.enter, logger.exit)
def main():
    if read_config.config["is_running"]:
        host.run()
        """
        cpu.run()
        disk.run()
        process.run()
        ram.run()
        """

        """
        print("numCores")
        print(process_command.run("sysctl -n hw.logicalcpu"))
        print()
        print("OS Version")
        print(process_command.run("sw_vers -productVersion"))
        print()
        print("Total Disk")
        print(process_command.run("df | grep '/$' | awk '{s=$2} END {print s}'"))
        print()
        print("Total RAM")
        print(process_command.run("sysctl hw.memsize"))
        print()
        print("Used Disk")
        print(process_command.run("df | tail +2 | awk '{s+=$3} END {print s}'"))
        print()
        print("Process Information")
        print(
            process_command.run(
                "ps -arcwwwxo 'command pid ppid %mem %cpu user etime time'"
            )
        )
        print()
        # Thread information will require a loop over pid.
        # For now, I will call it on just 1 pid for proof of concept
        # Note: This will
        print("Threads")
        print(process_command.run("ps -M 1 | grep 1 | wc -l"))
        print()
        # Used Ram requires App Memory + Wired Memory + Compressed Memory
        # App Memory is Internal Page Count - Purgeable Pages
        print("Internal Page Count")
        print(
            process_command.run(
                "sysctl vm.page_pageable_internal_count | awk '{s=$2} END {print s}'"
            )
        )
        print()
        print("Purgeable Pages")
        print(
            process_command.run(
                "vm_stat | grep 'Pages purgeable:'' | awk '{s+=$3} END {print s}'"
            )
        )
        print()
        print("Wired Memory")
        print(
            process_command.run(
                "vm_stat | grep 'Pages wired down:'' | awk '{s+=$4} END {print s}'"
            )
        )
        print()
        print("Compressed Memory")
        print(
            process_command.run(
                "vm_stat | grep 'Pages occupied by compressor:' | awk '{s+=$5} END {print s}'"
            )
        )
        print()
        print("Used CPU")
        print(process_command.run("ps -A -o %cpu | awk '{s+=$1} END {print s}'"))
        print()
        """


if __name__ == "__main__":
    main()
