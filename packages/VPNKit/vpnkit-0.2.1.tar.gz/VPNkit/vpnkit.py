#!/usr/bin/env python
import base64
import requests
import readline
import os
import sys
import tarfile
import subprocess
import platform
import psutil
import threading
import six
import socket
import time
import signal

COMMANDS = ['start', 'accounts', 'new', 'exit', 'help']
username = ''
servername = ''
LIST_PIDS = []

VERSION = sys.version_info.major

DATAPATH = '/usr/share/vpnkit/'

# for stop check internet timer
CHECK_STATUS = True

INTERNET_STATUS = False

CHECK_DEF_EXISTS = 'default'

LIST_ACCOUNTS = []

DEF_IP = ''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if VERSION != 2:
    CHECK_DEF_EXISTS = bytes(CHECK_DEF_EXISTS, 'utf-8')


# start vpnkit client. User can choose action
def start():
    global COMMANDS
    COMMANDS = ['start', 'accounts', 'new', 'exit', 'help']
    global username
    global servername
    global CHECK_STATUS

    get_settings()
    get_list_accounts()
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    unconfirmed_username = ''
    unconfirmed_servername = ''
    print('Current - Username: {} , Servername: {}'.format(username, servername))

    try:
        startChoose = six.moves.input("Choose operations[start|new|accounts|help|exit]: ").replace(" ", "") or 'start'
    except KeyboardInterrupt:
        CHECK_STATUS = False
        print("\nClosing...")
        sys.exit()

    if startChoose == 'new':

        try:
            hex = six.moves.input("Enter personal code: ").replace(" ", "")
        except KeyboardInterrupt:
            CHECK_STATUS = False
            print("\nClosing...")
            sys.exit()
        try:
            decode_result = base64.b64decode(hex).decode('utf-8').split('\n')

            if decode_result[0].isdigit():
                # No check user existing
                unconfirmed_username = decode_result[0]
            else:
                raise ValueError

            if socket.inet_aton(decode_result[1]):
                unconfirmed_servername = decode_result[1]
            else:
                raise socket.error

        except socket.error:
            print(bcolors.FAIL + bcolors.BOLD + 'Incorrect IP in personal code' + bcolors.ENDC)
            start()
        except ValueError:
            print(bcolors.FAIL + bcolors.BOLD + 'Incorrect username in personal code' + bcolors.ENDC)
            start()
        except:
            print(bcolors.FAIL + bcolors.BOLD + 'Incorrect code' + bcolors.ENDC)
            start()

        get_list_accounts()
        result = get_certificate(unconfirmed_username, unconfirmed_servername)
        if result:
            start_openvpn()
        elif not result:
            start()

    elif startChoose == 'start':
        get_list_accounts()
        result = get_certificate(username, servername)
        if result:
            start_openvpn()
        elif not result:
            start()

    elif startChoose == 'accounts':
        accounts_choose()
        # start()

    elif startChoose == 'exit':
        print("Closing...")
        if INTERNET_STATUS:
            CHECK_STATUS
            CHECK_STATUS = False
        sys.exit()

    elif startChoose == 'help':
        print(
                '\nOpenvpn CLI client. Available commands:\n'
                '\n\t' + bcolors.UNDERLINE + 'start' + bcolors.ENDC + ' - default option. Start openvpn service with current parameters.\n'
                '\n\t' + bcolors.UNDERLINE + 'new' + bcolors.ENDC + ' - option to start new connection with new parameters.\n'
                '\n\t' + bcolors.UNDERLINE + 'accounts' + bcolors.ENDC + ' - list of your active server accounts.\n'
                '\n\t' + bcolors.UNDERLINE + 'change' + bcolors.ENDC + ' - option to change accounts.\n'
                '\n\t' + bcolors.UNDERLINE + 'help' + bcolors.ENDC + ' - option to get application helper.\n'
                '\n\t' + bcolors.UNDERLINE + 'exit' + bcolors.ENDC + ' - option to exit from the appliation , kill openvpn process and reestablish default connection.\n'
                '\n After connect options:\n'
                '\n\t' + bcolors.UNDERLINE + 'close' + bcolors.ENDC + ' - close current connection and reestablish default. Exit from the application.\n'
                '\n\t' + bcolors.UNDERLINE + 'other' + bcolors.ENDC + ' - close current connection and reestablish default. You can try reestablish new connection to openvpn server.\n')
        start()

    elif startChoose != ' ':
        print(bcolors.WARNING + bcolors.BOLD + "Operation '" + startChoose + "' not found" + bcolors.ENDC)
        start()


# getting certificates for openvpn from the server by username
def get_certificate(unconfirmed_username, unconfirmed_servername):
    global username
    global servername
    SERVER_STATUS = '500'
    if VERSION != 2:
        SERVER_STATUS = bytes(SERVER_STATUS, 'utf-8')

    if unconfirmed_servername != '' and unconfirmed_username != '':
        try:
            headers = {'client-request': 'True'}
            req = requests.get('http://' + unconfirmed_servername + '/download/' + unconfirmed_username + '/',
                               headers=headers)
            # print(req.content)
            if req.status_code == 200:
                # Approving username and servername if successful response
                # change global variable
                username = unconfirmed_username
                servername = unconfirmed_servername
                # Add account to settings file
                check_account = False
                for line in LIST_ACCOUNTS:
                    if line[0] == username:
                        check_account = True
                if not check_account:
                    save_settings()

                print(bcolors.OKGREEN + 'You have ' + req.headers[
                    'Days-left'] + ' days yet.' + bcolors.ENDC)
                open(username + '.tar.gz', 'wb').write(req.content)
                tar = tarfile.open(username + '.tar.gz', "r")
                tar.extractall()
                print(bcolors.OKGREEN + 'Certificates received' + bcolors.ENDC)
                return True
            else:
                if req.status_code == 404:
                    print (bcolors.FAIL + bcolors.BOLD +
                           'Page not found. Please, check your settings (Server IP: {}. Username: {})'.format(
                               unconfirmed_servername, unconfirmed_username)
                           + bcolors.ENDC)
                elif req.json()['response'] == 'User not exists':
                    print(bcolors.FAIL + bcolors.BOLD + "User not exists on the server" + bcolors.ENDC)
                    del_account(unconfirmed_username)
                elif SERVER_STATUS not in req.content:
                    print(bcolors.FAIL + bcolors.BOLD + 'Server response: ' + req.json()['response'] + bcolors.ENDC)
                else:
                    print (bcolors.FAIL + bcolors.BOLD + 'Error download certificates.' + bcolors.ENDC)
                return False
        except Exception as e:
            print (
                        bcolors.FAIL + bcolors.BOLD + 'Server connection error. Please, check your settings (Server IP: {}. Username: {}).'.format(
                    unconfirmed_servername, unconfirmed_username)
                        + bcolors.ENDC)
            return False

    else:
        print(bcolors.WARNING + bcolors.BOLD + 'Please, enter connection parameters by typing \'new\' ' + bcolors.ENDC)
        return False


# start openvpn and delete default route  from ip route table
def start_openvpn():
    global servername
    global CHECK_STATUS
    global LIST_PIDS
    check_up = 'Initialization Sequence Completed'

    if VERSION != 2:
        check_up = bytes(check_up, 'utf-8')

    print (bcolors.OKGREEN + "Your config must be in :" + DATAPATH + bcolors.ENDC)
    s = subprocess.Popen(
        ['ss-local', '-s', servername, '-p', '443', '-k', 'phuu3faiGh', '-m', 'aes-256-cfb', '-l', '1080', '-t',
         '60'], stdout=subprocess.PIPE)
    p = subprocess.Popen(['sudo', 'openvpn', '--config', DATAPATH + 'client.conf'], stdout=subprocess.PIPE, shell=False)

    # Getting pids of all openvpn processes
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    LIST_PIDS.append(p.pid)
    LIST_PIDS.append(s.pid)
    for child in children:
        c = psutil.Process(child.pid)
        cc = c.children(recursive=True)
        for c in cc:
            LIST_PIDS.append(c.pid)

    # Add main script pid for
    # LIST_PIDS.append(os.getpid())
    with open(DATAPATH + 'pids.txt', 'w+') as file:
        for pid in LIST_PIDS:
            pid = str(pid) + '\n'
            file.write(pid)

    CHECK_STATUS = True
    internet_on(servername)
    while True:
        output = p.stdout.readline()

        if output == '' and p.poll() is not None:
            break

        if output:
            print (output.strip().decode('utf-8'))

        if check_up in output:
            next_choose()
            break


# Choosing action when  vpn tunnel up (exit or try new connection)
def next_choose():
    global COMMANDS
    COMMANDS = ['close', 'other']
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    global INTERNET_STATUS, CHECK_STATUS, LIST_PIDS

    try:
        choose = six.moves.input("Choose [close|other]: ").replace(" ", "") or 'other'
    except KeyboardInterrupt:
        CHECK_STATUS = False
        print("\nClosing...")
        del_route(servername)
        sys.exit()

    if choose == 'close':
        print("Closing...")
        if INTERNET_STATUS:
            CHECK_STATUS = False
        del_route(servername)
        sys.exit()

    elif choose == 'other':
        CHECK_STATUS = False
        del_route(servername)
        kill_proc()
        clear_pids_file()
        start()

    elif choose != ' ':
        print(bcolors.WARNING + bcolors.BOLD + "Operation '" + choose + "' not found" + bcolors.ENDC)
        next_choose()


# Choosing action when  vpn tunnel up (exit or try new connection)
def accounts_choose():
    global COMMANDS
    COMMANDS = ['change', 'delete', 'back']
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    global INTERNET_STATUS, CHECK_STATUS, LIST_PIDS

    if len(LIST_ACCOUNTS) > 1:
        print (bcolors.OKGREEN + "Your accounts:" + bcolors.ENDC)
        line_number = 0
        line_count = file_len(DATAPATH + 'settings.ini')
        for line in LIST_ACCOUNTS:
            if line_number != 0 and line_number != line_count - 1:
                if line[0] == username:
                    print (bcolors.OKGREEN + '*{} Username:{} , server: {}'.format(line_number, line[0],
                                                                                   line[1]) + bcolors.ENDC)
                else:
                    print (' {} Username:{} , server: {}'.format(line_number, line[0], line[1]))
            line_number += 1
        try:
            choose = six.moves.input("Choose [change|delete|back]: ").replace(" ", "") or 'back'
        except KeyboardInterrupt:
            CHECK_STATUS = False
            print("\nClosing...")
            sys.exit()

        if choose == 'back':
            start()

        elif choose == 'change':
            check_len = len(LIST_ACCOUNTS) - 2
            if check_len > 1:
                text = 'Enter account number 1-{}: '.format(check_len)
                try:
                    choose = six.moves.input(text)
                except KeyboardInterrupt:
                    CHECK_STATUS = False
                    print("\nClosing...")
                    sys.exit()
                if choose.isdigit():
                    if int(choose) > check_len:
                        print(bcolors.WARNING + bcolors.BOLD + "Enter correct number" + bcolors.ENDC)
                        start()
                    else:
                        acc = int(choose)
                        set_account(acc)
                        result = get_certificate(username, servername)
                        if result:
                            start_openvpn()
                        else:
                            start()
                else:
                    print(bcolors.FAIL + bcolors.BOLD + 'Invalid number' + bcolors.ENDC)
                    start()
            else:
                print(bcolors.WARNING + bcolors.BOLD + "You don't have accounts to change" + bcolors.ENDC)
                start()
        elif choose == 'delete':
            check_len = len(LIST_ACCOUNTS) - 2
            if check_len > 0:
                if check_len == 1:
                    text = 'Enter account number 1: '.format(check_len)
                else:
                    text = 'Enter account number 1-{}: '.format(check_len)
                try:
                    choose = six.moves.input(text)
                except KeyboardInterrupt:
                    CHECK_STATUS = False
                    print("\nClosing...")
                    sys.exit()
                if choose.isdigit():
                    if int(choose) > check_len or int(choose) <= 0:
                        print(bcolors.WARNING + bcolors.BOLD + "Enter correct number" + bcolors.ENDC)
                        start()
                    else:
                        acc = LIST_ACCOUNTS[int(choose)][0]
                        del_account(acc)
                        start()
                else:
                    print(bcolors.FAIL + bcolors.BOLD + 'Invalid number' + bcolors.ENDC)
                    start()
            else:
                print(bcolors.WARNING + bcolors.BOLD + "You don't have accounts for deleting" + bcolors.ENDC)
                start()

        elif choose != ' ':
            print(bcolors.WARNING + bcolors.BOLD + "Operation '" + choose + "' not found" + bcolors.ENDC)
            accounts_choose()
    else:
        print(bcolors.WARNING + bcolors.BOLD + "You don't have accounts" + bcolors.ENDC)
        start()


def del_account(account):
    # If user not exists on the server delete his accounts from client accounts list
    with open(DATAPATH + 'settings.ini', 'r') as file:
        lines = file.readlines()
    # If file has several lines (Accounts, 1 line by default with def ip  )
    if len(lines) > 1:
        for line in lines:
            # delete account from list
            if account in line:
                lines.remove(line)

        # lines = lines[:-1]
        if servername == account:
            if len(lines) > 1:
                lines.append(lines[len(lines) - 1])
        with open(DATAPATH + 'settings.ini', 'w') as new_file:
            new_file.truncate(0)
            for line in lines:
                new_file.write(line)
    print(bcolors.OKGREEN + "Account " + account + " deleted" + bcolors.ENDC)
    get_settings()


def set_account(account):
    global servername
    global username
    servername = LIST_ACCOUNTS[account][1]
    username = LIST_ACCOUNTS[account][0]

    with open(DATAPATH + 'settings.ini', 'r+b') as myfile:
        # Read the last 1kiB of the file
        # we could make this be dynamic, but chances are there's
        # a number like 1kiB that'll work 100% of the time for you
        myfile.seek(0, 2)
        filesize = myfile.tell()
        blocksize = min(1024, filesize)
        myfile.seek(-blocksize, 2)
        # search backwards for a newline (excluding very last byte
        # in case the file ends with a newline)
        index = myfile.read().rindex(b'\n', 0, blocksize - 1)
        # seek to the character just after the newline
        myfile.seek(index + 1 - blocksize, 2)

        # modify last_line
        lastline = username + ',' + servername + ',' + DEF_IP.decode("utf-8") + '\n'
        # seek back to the start of the last line
        myfile.seek(index + 1 - blocksize, 2)
        # write out new version of the last line
        if VERSION == 2:
            lastline = lastline.encode('utf-8')
        else:
            lastline = bytes(lastline, 'utf-8')
        myfile.write(lastline)
        myfile.truncate()


def get_list_accounts():
    global LIST_ACCOUNTS
    LIST_ACCOUNTS = []
    with open(DATAPATH + 'settings.ini') as fp:
        line = fp.readline()
        while line:
            lines = line.replace('\n', '').split(',')
            LIST_ACCOUNTS.append(lines)
            line = fp.readline()


def save_settings():
    settings = username + ',' + servername + ',' + DEF_IP.decode("utf-8") + '\n'
    with open(DATAPATH + 'settings.ini', 'r') as file:
        # read a list of lines into data
        data = file.readlines()
    if len(data) == 1:
        data.append(settings)
    else:
        data[len(data) - 1] = settings

    with open(DATAPATH + 'settings.ini', 'a') as fs:
        fs.truncate(0)
        fs.writelines(data)
        fs.write(settings)


def get_settings():
    global username
    global servername
    global DEF_IP
    global LIST_ACCOUNTS
    settings_file = DATAPATH + 'settings.ini'

    pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
    for line in pl.splitlines():
        if CHECK_DEF_EXISTS in line:
            fields = line.strip().split()
            DEF_IP = fields[2]

    # check if file exists and it's empty
    if os.path.isfile(settings_file) and os.stat(settings_file).st_size != 0:
        get_list_accounts()
        username = LIST_ACCOUNTS[len(LIST_ACCOUNTS) - 1][0]
        servername = LIST_ACCOUNTS[len(LIST_ACCOUNTS) - 1][1]
    else:
        with open(DATAPATH + 'settings.ini', 'w') as file:
            file.write(username + ',' + servername + ',' + DEF_IP.decode("utf-8") + '\n')


def complete(text, state):
    for cmd in COMMANDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def internet_enter_on():
    #  check internet connection on start vpnkit
    try:
        requests.get('http://216.58.192.142', timeout=3)
        global INTERNET_STATUS
        INTERNET_STATUS = True
        return True
    except Exception as err:
        pass


def internet_on(servername):
    #  check internet connection
    global INTERNET_STATUS
    global CHECK_STATUS

    check_servername = servername
    if VERSION != 2:
        check_servername = bytes(servername, 'utf-8')

    t = threading.Timer(5, internet_on, [servername])
    t.start()

    if not CHECK_STATUS:
        t.cancel()
    else:
        try:
            requests.get('http://216.58.192.142', timeout=3)
            INTERNET_STATUS = True
            return True
        except socket.timeout as e:
            print(bcolors.FAIL + bcolors.BOLD + "Socket error" + bcolors.ENDC)
        except Exception as err:
            def_exists = False
            servername_exists = False
            pl = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE).communicate()[0]
            for line in pl.splitlines():
                # if check_servername in line:
                #     print(bcolors.FAIL + bcolors.BOLD + "\nYou were been diactivated or lost internet" + bcolors.ENDC)
                #     CHECK_STATUS = False
                #     exit.main()
                if CHECK_DEF_EXISTS in line:
                    def_exists = True
                if check_servername in line:
                    servername_exists = True
            if def_exists and not servername_exists:
                try:
                    subprocess.call(['sudo', 'ip', 'route', 'add', servername, 'via', DEF_IP])
                except:
                    pass
            if def_exists and servername_exists:
                print(bcolors.FAIL + bcolors.BOLD + "\nYou were been deactivated or lost connection" + bcolors.ENDC)
                del_route(check_servername)
                CHECK_STATUS = False
                try:
                    os.kill(os.getppid(), signal.SIGTERM)
                    os.kill(os.getppid() + 1, signal.SIGTERM)
                except:
                    pass
                sys.exit()
            INTERNET_STATUS = False
            return False


def del_route(route):
    dp = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE)
    dp.wait()

    if VERSION != 2:
        route = bytes(route, 'utf-8')

    res = dp.communicate()[0]
    for line in res.splitlines():
        if route in line:
            d = subprocess.call(
                ['sudo', 'ip', 'route', 'del', route],
                stdout=subprocess.PIPE)
            break


# get pid of necessary process
def get_proc_pid(p):
    pid = p.pid
    return str(pid)


def get_procs_by_pid(pids, include_self=True):
    procs = []
    for p in psutil.process_iter():
        if (int(get_proc_pid(p)) in pids and
                (os.getpid() != p.pid or include_self)):
            procs.append(p)
    return procs


def kill_proc():
    global LIST_PIDS
    kill_status = False
    if len(LIST_PIDS) != 0:
        procs = get_procs_by_pid(LIST_PIDS, include_self=False)
        if len(procs) > 0:
            for p in procs:
                p.kill()
            _, procs = psutil.wait_procs(procs)
            kill_status = True

        if len(procs) > 0:
            print('Failed')
        else:
            if kill_status:
                print(bcolors.OKGREEN + 'Process openvpn kill' + bcolors.ENDC)
    LIST_PIDS = []
    # else:
    #     print(bcolors.WARNING+ "Openvpn process not exists" + bcolors.ENDC)


# check vpnkit already starts  or not
def check_start_status():
    proc_name = '/usr/bin/vpnkit'
    count_proc = get_proc_count(proc_name)
    # this vpnkit already started and will be in processes list
    if count_proc > 1:
        print ("VpnKit is already started")
        sys.exit()


def get_proc_count(name):
    count_proc = 0
    ps = subprocess.Popen(('ps', '-aux'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', name), stdin=ps.stdout)
    ps.wait()
    if VERSION != 2:
        name = bytes(name, 'utf-8')

    for line in output.splitlines():
        if name in line:
            count_proc += 1
    return count_proc


def clear_pids_file():
    with open(DATAPATH + 'pids.txt', 'a+') as file:
        file.truncate(0)


def main():
    clear_pids_file()

    # check vpnkit already starts  or not
    #check_start_status()

    # check internet connection status for start openvpn
    result = internet_enter_on()

    if result:
        get_settings()
        # change dir . Openvpn can find certificates.
        os.chdir(DATAPATH)
        start()
    else:
        print(bcolors.FAIL + bcolors.BOLD + "No internet connection!" + bcolors.ENDC)
        sys.exit()


if __name__ == '__main__':
    main()
