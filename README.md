# SoftWareProject_SJTU-EXCHANGE
# Copyright by Cylanx
	1.You can run main.py to open a GUI to exchange item .The Item_data.txt ,where stores the information of all items ,is already created and holds for something i pre-write .
	2.Note that: Source file by Python 3.10, additonal packages including "tkinter" "sql" , you might have to download with pip.
	3.UserGuide: Make sure that after downloading the SQL, after running the main.py, modify filename='D:SQLEMIS_log.ldf' on line 50 and 59 to the folder where you want to store data, the path must exist, otherwise an error will be reported; After the database is created, an error will be reported for the second build, please delete the data file and then re-establish it. The current version of the local database is not yet implemented to connect to the database remotely.
	(确保下载sql后，运行main.py后在第50行，59行修改filename='D:\\SQL\\EMIS_log.ldf'为想要存放数据的文件夹，路径必须要存在，否则会报错；建立数据库后第二次建立也会报错，请删除数据文件后再重新建立。目前是本地数据库版本，还未实现远程连接数据库)