import time
import threading

class ThreadingTests:


    
        

    @staticmethod
    def threadingTest():
        FlaskThread = threading.Thread(target=ThreadingTests.runNodeFlask)
        nodeTestThread = threading.Thread(target=ThreadingTests.NodeTestFunc)

        nodeTestThread.start()

        FlaskThread.start()

        time.sleep(1000)




        nodeTestThread.join()

        FlaskThread.join


