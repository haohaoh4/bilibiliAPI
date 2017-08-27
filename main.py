import video

def com():
    max_av = 0
    max_points = 0
    for i in range(1,100000):
        data = video.video_data().set_av(i).info
        if(data.view < 0):
            print 'av%s is none' % i
            continue
        try:
            a = (200000 + data.view)/(2 * data.view)
            b = (data.favorite * 20 + data.coins *10)
            b = b / (data.view + data.coins +1)
            points = data.view * a + data.coins * b
            points = points + data.favorite *20
        except:
            print "av%s is error" % i
            continue
        if points > max_points:
            max_av = i
            max_points = points
            print "new best:av%s\tpoints:%s" % (i,points)


com()
