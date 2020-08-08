import urx
import time
import sys
import math3d as m3d


if __name__ == '__main__':
        v = 0.05
        a = 0.01
        home_pos = (-0.11431887416707531, 0.3814339111789867, 0.16166744365529034, 1.5820121817451451, -0.951245384542397, -0.6958983653950617)
        rob = urx.Robot("192.168.1.105")
        rob.set_tcp((0, 0, 0.18, 0, 0, 0))
        time.sleep(0.2)
        p1 = rob.getl()
        print ("Original pose is: ",  p1)
        #rob.movel((0, 0, 0, 0, 0, 0), a, v, relative=True)
        #p2 = rob.getl()
        #print ("Current tool pose is: ",  p2)

        rob.stopl()
        sys.exit(0)
