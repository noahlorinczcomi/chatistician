import os
import subprocess
from server import utils as server_utils

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for running simulations

def parse_simulation(msg):
    """figure out which simulation user wants from their message"""
    clean_msg = msg.lstrip()
    
    # if message does not indicate simulation type, end
    if '{' not in clean_msg:
        return None
        
    script_start = clean_msg.index('{') + 1
    script_end = clean_msg.index('}')
    sim_type = clean_msg[script_start:script_end]
    script = server_utils.match_sim_to_script(sim_type)
    args = clean_msg[(script_end + 2):]
    
    return script, args

# function to read simulation description and return R script name
def match_sim_to_script(sim_name):
    sim_name = sim_name.lower()
    # T-tests
    ttest_subs = ['t-test', 't test', ' t']
    is_ttest = any(s in sim_name for s in ttest_subs)
    paired_subs = ['paired', 'pair', 'repeated', 'matched']
    is_paired = any(s in sim_name for s in paired_subs)
    
    # other simulation types ...
    available_scripts = os.listdir('power_analysis')
    script = f"ERROR: simulation type not found. Options are: {', '.join(available_scripts)}"
    if is_ttest and not is_paired:
        script = 'independent_t-test.R'
    elif is_ttest and is_paired:
        script = 'paired_t-test.R'
    return script

# function to run simulation (R script) from within chat
def run_simulation(script, args):
    cmd = f"Rscript {script} {args}"
    run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return run.stdout

