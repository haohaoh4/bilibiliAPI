import time
import bili

def main(f,to):
    print "start"
    max_click = -1
    max_id = -1
    for i in range(f, to):
        try:
            current_click = bili.get_click(i)
        except IOError,reason:
            continue
        if current_click > max_click:
            max_click = current_click
            max_id = i
        if(i % 5 ==0 and i != to - 1):
            print "%s%%" % (100.0 * (i - f) / (to - f))
            print "temp max:av%s\tclicks:%s" % (max_id, max_click)
        time.sleep(0.2)
    print "100.0%%"
    return "max:av%s\tclicks:%s" % (max_id, max_click)

print main(10000,100000)