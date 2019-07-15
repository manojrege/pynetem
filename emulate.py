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

