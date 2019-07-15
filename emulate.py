import subprocess

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
            raise Exception("Option not found")
    except subprocess.CalledProcessError as e:
            print(e.output)
            return False





