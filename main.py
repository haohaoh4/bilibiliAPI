import video
import MySQLdb

def main():
	db = MySQLdb.Connect("127.0.0.1", "root", "root", "python")
	cur = db.cursor()
	sql = "INSERT into bilibili (av,view,coin,comment,favorite,points) VALUES (%s,%s,%s,%s,%s,%s)"
	#cur.execute("delete from bilibili")

	for i in range(2000,5000):
		data = video.video_data().set_av(i).info
		view, coin, comment, favorite = data.view, data.coins, data.comment, data.favorite
		if view <= 0:
			continue
		a = (200000 + view) / (2 * view)
		if a > 1:
			a = 1
		b = (favorite * 20 + coin * 10)
		b = b / (view + coin * 10 + comment * 50)
		point = view * a + comment * b * 50
		point = point + coin * b *10 +favorite * 20
		cur.execute(sql % (i, view, coin, comment, favorite, point))

main()