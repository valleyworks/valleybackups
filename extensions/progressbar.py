import sys
import time
import threading

class progress_bar_loading(threading.Thread):

    def __enter__(self):
        self.stop = False
        self.kill = False

    def run(self):
            print 'Loading....  ',
            sys.stdout.flush()
            i = 0
            while self.stop != True:
                    if (i%4) == 0:
                    	sys.stdout.write('\b/')
                    elif (i%4) == 1:
                    	sys.stdout.write('\b-')
                    elif (i%4) == 2:
                    	sys.stdout.write('\b\\')
                    elif (i%4) == 3:
                    	sys.stdout.write('\b|')

                    sys.stdout.flush()
                    time.sleep(0.2)
                    i+=1
    def stop(self):
        self.stop = True
    	print '\b\b done!',

    def kill(self):
        self.stop = True
    	print '\b\b\b\b ABORT!',
