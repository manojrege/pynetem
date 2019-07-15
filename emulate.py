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