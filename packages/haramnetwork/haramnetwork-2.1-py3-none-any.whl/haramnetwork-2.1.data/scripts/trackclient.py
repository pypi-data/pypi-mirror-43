import socket
from threading import Thread
import time
from netutils import read_line as rl

TCP_IP = '192.168.43.121'
TCP_PORT = 1234
BUFFER_SIZE = 20


def main(): # called at the end of the file

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_IP, TCP_PORT))
        #t = Thread(target=rl, args=s)

        while True:
            msg = input("Enter your message \n")
            s.sendall(bytes(msg+"\r\n","utf8"))
            time.sleep(.1)
            ans = rl(s)
            print(ans)
            if ans == "SOL":
                iplist = []
                while True:
                    ans = rl(s)
                    iplist.append(ans)
                    print(ans)
                    if ans == "EOL":
                        break
            if ans == "Goodbye!":
                break
        s.close()


if __name__== "__main__":
    main()