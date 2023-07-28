import os
from DoS_Nmap import dos_attack
from SubscriberBomb import SubscriberBombAttack


def print_options(msg):
    print('\n----------------------------------------------------------')
    print(msg)
    print("Enter a number to select that option")
    print("1) Run a scan of the system ")
    print("2) Display current detected rosgraph")
    print("3) Kill a node")
    print("4) Run a DOS against a selected host")
    print("5) Run a DOS against a selected publisher")
    print("6) Run a DOS against a selected subscriber")
    print("7) Run a DOS against only Master")
    print("8) Exhaust all open ports on a selected host")
    print("9) List all the parameters on the parameter server")
    print("10) List all the parameters on the parameter server AND read one param value")
    print("11) Change a parameter on the parameter server")
    print("12) Inject data onto a given topic (Subscriber)")
    print("13) Replace a node with a copy under your control")
    print("14) Perform a Man in the Middle(MITM) attack against two nodes over a topic ")
    print("0) Exit")


def choice(option):
    if option == 1:
        return 'TODO'
    elif option == 2:
        try:
            os.system('rosrun rqt_graph rqt_graph')
            return 'ROSGRAPH terminated.'
        except:
            return "ROS is NOT installed properly!"
    elif option == 3:
        try:
            print("Active ROS nodes:")
            os.system('rosnode list')
            nodename = input('Enter a node name to kill it. EG. gazebo \n>>>')
            os.system('rosnode kill /' + nodename)
            input('Press Enter to return Main Menu.')
            return '---ROSATK---'

        except:
            return "ROS is NOT installed properly!"
        
    elif option == 4:
        try:
            ip = input('Enter local ip address of the target device. EG. 192.168.1.1\n>>>')
            print('Attack started. CTRL+C\'to stop.')
            dos_attack(ip)
        except:
            return 'DOS ATTACK FAIL'

    elif option == 5:
        try:
            count = int(input('Enter count of attacker nodes. (Max: 1000 recommended.)\n>>>'))
            print('Attack started. CTRL+C\'to stop.')
            SubscriberBombAttack(count)
        except:
            return 'DOS ATTACK FAIL'
    elif option == 6:
        return 'DOS SUBS'
    elif option == 7:
        return 'DOS MASTER'
    elif option == 8:
        return 'port exhaust'
    elif option == 9:
        try:
            print("Active ROS params:")
            os.system('rosparam list')
            input('Press Enter to return Main Menu.')
            return '---ROSATK---'

        except:
            return "ROS is NOT installed properly!"
    elif option == 10:
        try:
            print("Active ROS params:")
            os.system('rosparam list')
            paramname = input('Enter a param name to read it. EG. rosversion \n>>>')
            os.system('rosparam get /' + paramname)
            input('Press Enter to return Main Menu.')
            return '---ROSATK---'

        except:
            return "ROS is NOT installed properly!"
    elif option == 11:
        try:
            print("Active ROS params:")
            paramname = input('Enter a param name and value to set it. EG. gazebo/gravity_x \n>>>')
            os.system('rosparam set /' + paramname)
            input('Press Enter to return Main Menu.')
            return '---ROSATK---'

        except:
            return "ROS is NOT installed properly!"
    elif option == 12:
        return 'TODO'
    elif option == 13:
        return 'TODO'



if __name__ == "__main__":
    option = -1
    msg = "Welcome to ROSATK"
    while option != 0:
        print_options(msg)
        try:
            option = int(input('>>>'))
        except:
            print('Wrong input type!')
            msg = "---ROSATK---"
        
        if option == 0:
            print("ROSATK is terminated!")
        elif option > 0 and option < 15:
            msg = choice(option)
        else:
            msg = print(option, ": command does NOT exist!")

