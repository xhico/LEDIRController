# -*- coding: utf-8 -*-
# !/usr/bin/python3

import json
import os
import time
import piir
import traceback
import logging
import sys
from Misc import get911, sendEmail


def main():
    """
    The main function for controlling an infrared (IR) remote using a Raspberry Pi.

    This script uses the piir library to send IR codes through a remote control device.
    It expects a command-line argument specifying the button (IR code) to be sent.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Example:
        To send the IR code for a specific button, run the script with the button name as an argument:
        ```
        python script_name.py button_name
        ```

        If the button name is "off," it turns off the IR device (assuming a specific behavior).

    Note:
        Make sure to configure the remote and provide the correct configuration file path.
        The script validates the number of command-line arguments and logs an error if invalid.

    """

    # Setup remote
    remote = piir.Remote(configFile, config["PIN_IR"])

    # Check for valid args
    if len(sys.argv) != 2:
        logger.error("Invalid args")
        return

    # Send IR code -> If btn != off -> make sure the LED is "on" before changing color
    btn = sys.argv[1]
    logger.info("Send IR code: " + btn)
    if btn != "off":
        remote.send("on")

    # Adjust Brightness
    if btn == "light_min" or btn == "light_max":
        for _ in range(50):
            remote.send(btn)
            time.sleep(0.1)
        return

    # Send normal color
    remote.send(btn)

    return


if __name__ == '__main__':
    # Set Logging
    LOG_FILE = f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{os.path.abspath(__file__).replace(".py", ".log")}")}"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    logger.info("----------------------------------------------------")

    # Load configuration from JSON file
    configFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(configFile) as inFile:
        config = json.load(inFile)

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
        sendEmail(os.path.basename(__file__), str(traceback.format_exc()))
    finally:
        logger.info("End")
