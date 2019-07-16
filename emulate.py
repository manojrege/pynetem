import subprocess
import jinja2

from functools import wraps

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
        if type == 'incoming':
            CONFIGURE_IN_ANCHOR = 'echo "dummynet in all pipe 1" | sudo pfctl -a '+anchor_name+' -f -'
            output = subprocess.check_output(CONFIGURE_IN_ANCHOR, shell=True)
            print(output)
        elif type == 'outgoing':
            CONFIGURE_OUT_ANCHOR = 'echo "dummynet out all pipe 1" | sudo pfctl -a '+anchor_name+' -f -'
            output = subprocess.check_output(CONFIGURE_OUT_ANCHOR, shell=True)
            print(output)
        elif type == 'duplex':
            CONFIGURE_IN_ANCHOR = 'echo "dummynet in all pipe 1" | pfctl -a '+anchor_name+' -f -'
            CONFIGURE_OUT_ANCHOR = 'echo "dummynet out all pipe 2" | pfctl -a '+anchor_name+' -f -'
            output1 = subprocess.check_output(CONFIGURE_IN_ANCHOR, shell=True)
            output2 = subprocess.check_output(CONFIGURE_OUT_ANCHOR, shell=True)
            print(output1)
            print(output2)
        else:
            raise Exception(type + " option not found. Valid options include: incoming, outgoing, duplex")
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
        output=subprocess.check_output("dnctl <<< echo \""+rule+"\"", shell=True)
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


def emulate(type, bandwidth_in = None, delay_in = None, plr_in = None, bandwidth_out = None, delay_out = None, plr_out = None):
    """

    :param type: "incoming", "outgoing", or "duplex"
    :param bandwidth_in: Outgoing bandwidth in Mbits/s
    :param delay_in: Outgoing delay in milliseconds
    :param plr_in: Outgoing packet loss rate percentage
    :param bandwidth_out: Outgoing bandwidth in Mbits/s
    :param delay_out: Outgoing delay in milliseconds
    :param plr_out: Outgoing packet loss rate percentage
    :return:
    """
    def decorate(f):
        @wraps(f)
        def func_emulate(*args, **kwargs):

            # Set all rules
            print("Flush all existing dnctl rules")
            flush_dnctl()
            print("Create a anchor pynetem")
            create_anchor("pynetem")
            print("Configuring anchor pynetem")
            configure_anchor("pynetem", type)
            print("Creating dummynet queue")
            if type == "incoming":
                incoming = generate_dnctl_rules("1", bandwidth = bandwidth_in, delay = delay_in, plr = plr_in)
                apply_dnctl_rules(incoming)
            elif type == "outgoing":
                outgoing = generate_dnctl_rules("1", bandwidth = bandwidth_out, delay = delay_out, plr = plr_out)
                apply_dnctl_rules(outgoing)
            elif type == "duplex":
                incoming = generate_dnctl_rules("1", bandwidth = bandwidth_out, delay = delay_out, plr = plr_out)
                apply_dnctl_rules(incoming)
                outgoing = generate_dnctl_rules("2", bandwidth = bandwidth_out, delay = delay_out, plr = plr_out)
                apply_dnctl_rules(outgoing)
            else:
                raise Exception(type + "Valid options include: incoming, outgoing, duplex")
            print("Activating Packet Filter")
            activate_pf()

            # Call the decorated function
            value = f(*args, **kwargs)

            # Flush all the dnctl rules
            #flush_dnctl()

            # Flush all firewall rules
            #flush_pf()

            return value
        return func_emulate
    return decorate