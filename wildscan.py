import pyfiglet
import socket
import threading
from queue import Queue
import time

ascii_banner = pyfiglet.figlet_format("WILDSCAN")
print(ascii_banner)
print ("by SeranoxLabs")

socket.setdefaulttimeout(0.6) #if no response in 0.6 seconds it moves on
print_lock = threading.Lock()
q = Queue()


def portscan(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        connection = s.connect((host,port))
        
        with print_lock:
            print('{} port is open'.format(port))
            
        connection.close()  
    except:
        pass
        
def thread(h):
    while True:
        port_to_scan = q.get()
        portscan(h,port_to_scan)
        q.task_done()

def main():
    target = input('Enter the website or ip: ')
    host = socket.gethostbyname(target)
    amount_of_threads = input("Enter the amount of threads to use (recommended is 200): ")
    num_ports = input('Enter the max number of the port range: ')
    starttime = time.time()
    
    
    for i in range(int(amount_of_threads)):
        t = threading.Thread(target=thread, args=(host,))
        t.daemon = True
        
        t.start()
        
    for ports in range(1,int(num_ports)):
        q.put(ports)
    
    q.join()
    
    totalrun = float('%0.2f' %(time.time() - starttime))
    print('Total run time is {}'.format(totalrun))
    
if __name__=="__main__":
    main()
        
    