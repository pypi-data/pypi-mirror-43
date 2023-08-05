# To run the job:
# pyats run job $VIRTUAL_ENV/examples/connection/job/connection_example_job.py \
#               --testbed-file $VIRTUAL_ENV/examples/connection/etc/connection_example_conf.yaml
#
# Description: This example uses a sample testbed, connects to a device
#              which name is passed from the job file,
#              and executes some commands. The goal is to show
#              how devices can be chosen dynamically and passed to the script.

import os
from pyats.easypy import run

def main():
    # Find the location of the script in relation to the job file
    test_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testscript = os.path.join(test_path, 'connection_example_script.py')

    # Do some logic here to determine which devices to use
    # and pass these device names as script arguments
    # ...
    chosen_uut_device = 'ott-tb1-n7k3'
    stdby_device = 'notreallyadevice'

    run(testscript=testscript,
        uut_name=chosen_uut_device,
        stdby_name=stdby_device)
