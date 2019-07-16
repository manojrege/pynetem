import subprocess
import jinja2

def flush_dnctl():
    try:
        FLUSH_COMMAND='dnctl -f flush'
        output = subprocess.check_output(FLUSH_COMMAND.split())
        print(output)
        return True
    except subprocess.CalledProcessError as e:
        print(e.output)
        return False

def create_anchor(anchor_name):
    CREATE_ANCHOR_COMMAND = '(cat /etc/pf.conf && echo \'dummynet-anchor "'+anchor_name+'"\' && echo \'anchor "'+anchor_name+'"\') | pfctl -q -f -'
    try:
        output = subprocess.check_output(CREATE_ANCHOR_COMMAND, shell=True)
        print(output)
        return True
    except subprocess.CalledProcessError as e:
        print(e.output)
        return False

def configure_anchor(anchor_name, type):
    try:
        if type == 'simplex':
            CONFIGURE_ANCHOR = 'echo "dummynet in all pipe 1" | sudo pfctl -a '+anchor_name+' -f -'
            output = subprocess.check_output(CONFIGURE_ANCHOR, shell=True)
            print(output)
        elif type == 'duplex':
            CONFIGURE_IN_ANCHOR = 'echo "dummynet in all pipe 1" | pfctl -a '+anchor_name+' -f -'
            CONFIGURE_OUT_ANCHOR = 'echo "dummynet out all pipe 2" | pfctl -a '+anchor_name+' -f -'
            output1 = subprocess.check_output(CONFIGURE_IN_ANCHOR, shell=True)
            output2 = subprocess.check_output(CONFIGURE_OUT_ANCHOR, shell=True)
            print(output1)
            print(output2)
        else:
            raise Exception(type + " option not found")
    except subprocess.CalledProcessError as e:
            print(e.output)
            return False

def generate_dnctl_rules(pipe_number, bandwidth = None, delay = None, plr = None):
    j2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(['.']), trim_blocks=True, lstrip_blocks=True)
    try:
        template = j2_env.get_template('dnctl.conf.j2')
        rules = template.render(number = pipe_number, bandwidth = bandwidth, delay = delay, plr = plr)
        if 'None' in rules:
            raise Exception("All Bandwidth, delay, and Packet Loss rate cannot be None")
        return rules
    except Exception as e:
        print(e)
        return

def apply_dnctl_rules(rule):
    try:
        print("Applying dnctl rules")
        output=subprocess.check_output("dnctl <<< echo\""+rule+"\"")
        print(output)
        return True
    except subprocess.CalledProcessError as e:
        print(e.output)
        return False

def activate_pf():
    try:
        ACTIVATE_PF_COMMAND="pfctl -E"
        output=subprocess.check_output(ACTIVATE_PF_COMMAND.split())
        print(output)
        return True
    except subprocess.CalledProcessError as e:
        print(e.output)
        return False

def flush_pf():
    try:
        FLUSH_PF_COMMAND="pfctl -F all"
        output=subprocess.check_output(FLUSH_PF_COMMAND.split())
        print(output)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False