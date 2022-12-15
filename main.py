import pymssql
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import tkinter.messagebox as messagebox  # 弹窗
# 打包的时候会用到（十进制的一个库）
import decimal

decimal.__version__


class StartPage:
    def __init__(self, parent_window):
        parent_window.update()
        parent_window.destroy()  # 销毁上一个窗口
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('商品信息管理系统')
        self.window.geometry('350x480+550+100')  # 这里的乘是小x，第一个参数表示窗口的长，第二个表示宽，第三个表示的距离屏幕左边界的距离，第三个为距离上边界的距离

        label = Label(self.window, text="商品信息管理系统", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 这个label距离窗口上边界的距离，这里设置为100刚好居中

        # command=lambda:  可以带参数，注意带参数的类不要写括号，否者，这里调用会直接执行(class test:)
        Button(self.window, text="管理员登陆", font=tkFont.Font(size=16), command=lambda: AdminPage(self.window),
               width=30, height=2,
               fg='white', bg='gray', activebackground='black',
               activeforeground='white').pack()  # pack() 方法会使得组件在窗口中自动布局
        Button(self.window, text="普通用户登陆", font=tkFont.Font(size=16), command=lambda: UserLogPage(self.window),
               width=30, height=2,
               fg='white', bg='gray', activebackground='black',
               activeforeground='white').pack()
        Button(self.window, text="数据库初始化", font=tkFont.Font(size=16), command=self.Initialization, width=30,
               height=2,
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="退出系统", height=2, font=tkFont.Font(size=16), width=30, command=self.window.destroy,
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.mainloop()  # 主消息循环

    # 创建数据库
    def Initialization(self):
        db = pymssql.connect('localhost', 'sa', '123456789', 'master')  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立数据库中......')
        sql = """
		-- 创建EMIS数据库
		CREATE DATABASE EMIS ON PRIMARY
		(
			NAME='EMIS_data',--主文件逻辑文件名
			FILENAME='D:\\SQL\\EMIS_data.mdf', --主文件文件名
			SIZE=5mb,--系统默认创建的时候会给主文件分配初始大小
			MAXSIZE=500MB,--主文件的最大值
			filegrowth=15%-- 主文件的增长幅度
		)
		LOG ON
		(
			name='EMIS_log',--日志文件逻辑文件名
			filename='D:\\SQL\\EMIS_log.ldf',--日志文件屋里文件名
			SIZE=5MB,--日志文件初始大小
			filegrowth=0 --启动自动增长
		)
		"""

        try:
            db.autocommit(True)  # 这个句话可以防止python创建数据库的时候报错（python连接数据库机制的问题）
            cursor.execute(sql)
            db.commit()
            self.jianbiao()  # 进行建表操作
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
            cursor.close()  # 关闭游标
            db.close()  # 关闭数据库连接


    # 创建数据表
    def jianbiao(self):
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立数据表中......')
        sql = """
		---创建管理员数据表
		CREATE TABLE t_admin (
		admin_id varchar(255) NOT NULL,
		admin_pass varchar(255) DEFAULT NULL,
		PRIMARY KEY (admin_id)
		);

		---插入管理账户和密码
		INSERT INTO t_admin VALUES ('admin', 'admin');

		CREATE TABLE t_user (
		user_id varchar(255) NOT NULL,
		user_pass varchar(255) DEFAULT NULL,
		PRIMARY KEY (user_id)
		);
		---插入普通用户账户和密码
		INSERT INTO t_user VALUES ('test', 'test');
		
		---插入申请用户账户和密码
		CREATE TABLE t_userRequest (
		userRequest_id varchar(255) NOT NULL,
		userRequest_pass varchar(255) DEFAULT NULL,
		userRequest_tele varchar(255) NOT NULL,
		userRequest_address varchar(255) DEFAULT NULL,
		PRIMARY KEY (userRequest_id)
		);
		
		---创建类型
		CREATE TABLE t_class (
		id varchar(20) DEFAULT NULL,
		attrib varchar(30) DEFAULT NULL,
		PRIMARY KEY (id)
		);
		INSERT INTO t_class VALUES ('foods', 'expiration date;quality');
		INSERT INTO t_class VALUES ('books', 'publisher');
		INSERT INTO t_class VALUES ('tools', 'quality');
		
		---创建商品表
		CREATE TABLE t_goods (
		goods_class varchar(20) NOT NULL,
		id varchar(20) NOT NULL,
		name varchar(20) DEFAULT NULL,
		number varchar(20) DEFAULT NULL,
		price varchar(7) DEFAULT NULL,
		address varchar(30) DEFAULT NULL,
		tele varchar(30) DEFAULT NULL,
		extra_attrib varchar(30) DEFAULT NULL,
		PRIMARY KEY (id)
		);

		---向商品表中插入数据
		INSERT INTO t_goods VALUES ('tools','1001', 'iphone1', '1', '1000','X19','tele12138','good');
		INSERT INTO t_goods VALUES ('foods','2001', 'apples', '4', '15','D16','qq189','good');
		INSERT INTO t_goods VALUES ('foods','2002', 'bananas', '10', '20','D5','qq12138','good');


		"""

        try:
            cursor.execute(sql)
            db.commit()
            messagebox.showinfo('提示！', '数据库建立成功！')
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接


# 管理员登陆页面
class AdminPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员登陆页面')
        self.window.geometry('450x300+500+100')

        # 创建画布，这里可以存放照片等组件
        canvas = tk.Canvas(self.window, height=200, width=500)
        image_file = tk.PhotoImage(file='welcome.gif')
        image = canvas.create_image(0, 0, anchor='nw', image=image_file)  # 前两个参数为画布得坐标，anchor=nw则是把图片的左上角作为锚定点
        canvas.pack(side='top')  # 使用pack将画布进行简单得布局，放到了上半部分

        # 创建提示信息
        tk.Label(self.window, text='登录名: ').place(x=80, y=150)
        tk.Label(self.window, text='登陆密码: ').place(x=80, y=190)

        self.admin_username = tk.Entry(self.window)
        self.admin_username.place(x=160, y=150)
        self.admin_pass = tk.Entry(self.window, show='*')
        self.admin_pass.place(x=160, y=190)
        # 登陆和返回首页得按钮
        btn_login = tk.Button(self.window, text='登陆', width=10, command=self.login)
        btn_login.place(x=120, y=230)
        btn_back = Button(self.window, text="返回首页", width=8, font=tkFont.Font(size=12), command=self.back)
        btn_back.place(x=270, y=230)
        self.window.mainloop()

    # 登陆的函数
    def login(self):
        # 数据库操作 查询管理员表
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_admin where admin_id = '%s'" % (
            self.admin_username.get())  # 这里得user_name即为admin_id，这里是输入的用户名
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表，这里是返回的二元元组，如(('id','title'),('id','title'))
            results = cursor.fetchall()
            for row in results:
                admin_id = row[0]
                admin_pass = row[1]
                # 打印结果
                print("管理员账号为：%s, \n\n管理员密码为：%s" % (admin_id, admin_pass))
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '用户名或密码不正确！')
        db.close()  # 关闭数据库连接

        print("正在登陆管理员管理界面.......")

        # 判断输入的账号密码与数据库中的信息是否一致a
        if self.admin_pass.get() == admin_pass:
            All_admin(self.window)  # 进入管理员子菜单操作界面
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    # 使得系统点击关闭的x号上返回指定页面，而不是关闭
    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

# 管理员子菜单操作界面
class All_admin:
    def __init__(self, parent_window):
        parent_window.destroy()  # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('信息管理界面')
        self.window.geometry('300x480+500+100')
        label = Label(self.window, text="请选择需要进行的操作", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 界面的长度

        Button(self.window, text="商品信息管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: GoodsOfClass(self.window,"admin"),
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="物品类型管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: GoodsClassManage(self.window),
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="用户申请信息管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: User_Request(self.window),
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

class All_user:
    def __init__(self, parent_window):
        parent_window.destroy()  # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('信息管理界面')
        self.window.geometry('300x480+500+100')
        label = Label(self.window, text="请选择需要进行的操作", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 界面的长度

        Button(self.window, text="商品信息", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: GoodsOfClass(self.window,"user"),
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="帮助", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: AboutPage(self.window),
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

#用户登录界面
class UserLogPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('用户登陆页面')
        self.window.geometry('450x300+500+100')

        # 创建画布，这里可以存放照片等组件
        canvas = tk.Canvas(self.window, height=200, width=500)
        image_file = tk.PhotoImage(file='welcome.gif')
        image = canvas.create_image(0, 0, anchor='nw', image=image_file)  # 前两个参数为画布得坐标，anchor=nw则是把图片的左上角作为锚定点
        canvas.pack(side='top')  # 使用pack将画布进行简单得布局，放到了上半部分

        # 创建提示信息
        tk.Label(self.window, text='登录名: ').place(x=80, y=150)
        tk.Label(self.window, text='登陆密码: ').place(x=80, y=190)

        self.username = tk.Entry(self.window)
        self.username.place(x=160, y=150)
        self.userpass = tk.Entry(self.window, show='*')
        self.userpass.place(x=160, y=190)
        # 登陆和返回首页得按钮
        btn_login = tk.Button(self.window, text='登陆', width=10, command=self.login)
        btn_login.place(x=120, y=230)
        btn_register = tk.Button(self.window, text='注册', width=10, command=self.register)
        btn_register.place(x=240, y=230)
        btn_back = Button(self.window, text="返回首页", width=8, font=tkFont.Font(size=13), command=self.back)
        btn_back.place(x=340, y=230)
        self.window.mainloop()

    # 登陆的函数
    def login(self):
        # 数据库操作 查询管理员表
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_user where user_id = '%s'" % (
            self.username.get())  # 这里得user_name即为admin_id，这里是输入的用户名
        user_id = []
        user_pass = []
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表，这里是返回的二元元组，如(('id','title'),('id','title'))
            results = cursor.fetchall()
            for row in results:
                user_id = row[0]
                user_pass = row[1]
                # 打印结果
                print("账号为：%s, \n密码为：%s" % (user_id, user_pass))
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '用户名或密码不正确！')
        db.close()  # 关闭数据库连接

        print("正在登陆.......")
        if user_id == [] :
            messagebox.showinfo('警告！', '用户不存在！')
        # 判断输入的账号密码与数据库中的信息是否一致a
        else:
            if self.userpass.get() == user_pass:
                All_user(self.window)  # 进入管理员子菜单操作界面
            else:
                messagebox.showinfo('警告！', '用户名或密码不正确！')

    def register(self):
        UserRegistPage(self.window)
    # 使得系统点击关闭的x号上返回指定页面，而不是关闭
    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口
class UserRegistPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('用户注册页面')
        self.window.geometry('450x300+500+100')

        # 创建提示信息
        tk.Label(self.window, text='登录名: ').place(x=80, y=60)
        tk.Label(self.window, text='登陆密码: ').place(x=80, y=100)
        tk.Label(self.window, text='电话: ').place(x=80, y=140)
        tk.Label(self.window, text='住址: ').place(x=80, y=180)


        self.username = tk.Entry(self.window)
        self.username.place(x=160, y=60)
        self.userpass = tk.Entry(self.window, show='*')
        self.userpass.place(x=160, y=100)
        self.tele = tk.Entry(self.window)
        self.tele.place(x=160, y=140)
        self.address = tk.Entry(self.window)
        self.address.place(x=160, y=180)

        btn_login = tk.Button(self.window, text='注册', width=10, command=self.register)
        btn_login.place(x=120, y=250)
        btn_register = tk.Button(self.window, text='取消', width=10, command=self.back)
        btn_register.place(x=240, y=250)
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()

    def register(self):
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_userRequest where userRequest_id = '%s'" % (
            self.username.get())
        userRequest_id = []
        user_id = []
        admin_id = []

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表，这里是返回的二元元组，如(('id','title'),('id','title'))
            results = cursor.fetchall()
            for row in results:
                userRequest_id = row[0]

            sql = "SELECT * FROM t_userwhere user_id = '%s'" % (
                self.username.get())
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    user_id = row[0]
            except:
                pass

            sql = "SELECT * FROM t_admin where admin_id = '%s'" % (
                self.username.get())
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    admin_id = row[0]
            except:
                pass

            if str(self.username.get()) in userRequest_id or str(self.username.get()) in user_id or str(self.username.get()) in admin_id:
                messagebox.showinfo('警告！', '该昵称已经提交注册申请！')

            else:
                if self.username.get() != '' and self.userpass.get() != '' :
                    sql = "INSERT INTO t_userRequest(userRequest_id,userRequest_pass,userRequest_tele,userRequest_address) \
                           VALUES ('%s', '%s','%s','%s')" % \
                          (
                          self.username.get(), self.userpass.get(),self.tele.get(), self.address.get())  # SQL 插入语句
                    try:
                        cursor.execute(sql)  # 执行sql语句
                        db.commit()  # 提交到数据库执行
                        messagebox.showinfo('提示！', '申请成功！')
                    except:
                        db.rollback()  # 发生错误时回滚
                        messagebox.showinfo('警告！', '数据库连接失败！')
                else:
                    messagebox.showinfo('警告！', '请填写用户名和密码')
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接
    # 使得系统点击关闭的x号上返回指定页面，而不是关闭
    def back(self):
        UserLogPage(self.window)  # 显示主窗口 销毁本窗口

#管理员
# 商品信息操作界面
class GoodsOfClass:
    def __init__(self, parent_window , pattern):
        parent_window.destroy()  # 销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('查找物品类型')
        self.window.geometry('600x600+500+100')
        self.frame_center = tk.Frame(width=500, height=300)
        self.pattern = pattern


        self.columns = ("物品类型","属性")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        self.tree.column("物品类型", width=200, anchor='center')
        self.tree.column("属性", width=300, anchor='center')

        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)

        # 登陆和返回首页得按钮
        btn_login = tk.Button(self.window, text='确定', width=10, command=self.GoodsInfoManage)
        btn_login.place(x=150, y=430)

        btn_back = Button(self.window, text='取消', width=10, command=self.back)
        btn_back.place(x=350, y=430)

        self.id = []
        self.attrib = []
        self.var_id = []

        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_class "
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.attrib.append(row[1])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接


        for i in range(min(len(self.id), len(self.attrib))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i],self.attrib[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))


        self.var_id = StringVar()  # 声明学号
        self.var_attrib = StringVar()  # 声明姓名


        # 整体区域定位，利用了Frame和grid进行布局
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=40, pady=50)
        # 设置固定组件，(0)就是将组件进行了固定
        self.frame_center.grid_propagate(0)
        self.frame_center.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题


    def back(self):
        if self.pattern == "admin":
            All_admin(self.window)  # 显示主窗口 销毁本窗口
        else :
            All_user(self.window)
    def GoodsInfoManage(self):
        var_id = self.var_id.get()
        if var_id:
            if self.pattern == "admin":
                GoodsInfoManage(self.window, var_id)
            else:
                GoodsInfo(self.window, var_id)
        else:
            messagebox.showinfo('警告！', '请选择类型！')
class GoodsInfoManage:
    def __init__(self, parent_window,goods_class):
        parent_window.destroy()  # 自动销毁上一个界面
        self.window = Tk()  # 初始框的声明
        self.window.title('管理员操作界面')
        self.window.geometry("850x685+300+30")  # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=300, height=200)  # 指定框架，在窗口上可以显示，这里指定四个框架
        self.frame_right_top = tk.Frame(width=200, height=200)
        self.frame_center = tk.Frame(width=800, height=350)
        self.frame_bottom = tk.Frame(width=650, height=70)

        # 定义下方中心列表区域
        self.columns = ("物品id", "物品名称", "物品数量", "物品价格","物品地址","联系电话","额外属性")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0
        self.goods_class = goods_class
        # 表格的标题
        self.tree.column("物品id", width=100, anchor='center')
        self.tree.column("物品名称", width=100, anchor='center')
        self.tree.column("物品数量", width=100, anchor='center')
        self.tree.column("物品价格", width=100, anchor='center')
        self.tree.column("物品地址", width=100, anchor='center')
        self.tree.column("联系电话", width=150, anchor='center')
        self.tree.column("额外属性", width=150, anchor='center')

        # grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 定义几个数组，为中间的那个大表格做一些准备
        self.id = []
        self.name = []
        self.number  = []
        self.price  = []
        self.address  = []
        self.tele   = []
        self.extra_attrib   = []

        # 打开数据库连接
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_goods where goods_class  = '%s'" % (self.goods_class)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[1])
                self.name.append(row[2])
                self.number.append(row[3])
                self.price.append(row[4])
                self.address.append(row[5])
                self.tele.append(row[6])
                self.extra_attrib.append(row[7])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.id), len(self.name), len(self.number), len(self.price),len(self.address), len(self.tele), len(self.extra_attrib))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.number[i], self.price[i],self.address[i], self.tele[i], self.extra_attrib[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="商品信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=5)  # NSEW表示允许组件向4个方向都可以拉伸

        # 定义下方区域
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_name = StringVar()  # 声明姓名
        self.var_number = StringVar()  # 声明性别
        self.var_price= StringVar()  # 声明年龄
        self.var_address = StringVar()  # 声明姓名
        self.var_tele = StringVar()  # 声明性别
        self.var_extra_attrib= StringVar()  # 声明年龄
        # 商品id
        self.right_top_id_label = Label(self.frame_left_top, text="物品id： ", font=('Verdana', 10))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 10))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1,columnspan=2)
        # 商品名称
        self.right_top_name_label = Label(self.frame_left_top, text="物品名称：", font=('Verdana', 10))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 10))
        self.right_top_name_label.grid(row=2, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=2, column=1,columnspan=2)
        # 商品价格
        self.right_top_price_label = Label(self.frame_left_top, text="物品价格：", font=('Verdana', 10))
        self.right_top_price_entry = Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 10))
        self.right_top_price_label.grid(row=3, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=3, column=1,columnspan=2)
        # 销售数量
        self.right_top_number_label = Label(self.frame_left_top, text="物品数量：", font=('Verdana', 10))
        self.right_top_number_entry = Entry(self.frame_left_top, textvariable=self.var_number, font=('Verdana', 10))
        self.right_top_number_label.grid(row=4, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=4, column=1,columnspan=2)

        self.right_top_tele_label = Label(self.frame_left_top, text="联系电话：", font=('Verdana', 10))
        self.right_top_tele_entry = Entry(self.frame_left_top, textvariable=self.var_tele, font=('Verdana', 10))
        self.right_top_tele_label.grid(row=5, column=0)  # 位置设置
        self.right_top_tele_entry.grid(row=5, column=1,columnspan=2)

        self.right_top_address_label = Label(self.frame_left_top, text="物品地址：", font=('Verdana', 10))
        self.right_top_address_entry = Entry(self.frame_left_top, textvariable=self.var_address, font=('Verdana', 10))
        self.right_top_address_label.grid(row=6, column=0)  # 位置设置
        self.right_top_address_entry.grid(row=6, column=1,columnspan=2)

        self.right_top_extra_attrib_label = Label(self.frame_left_top, text="额外属性：", font=('Verdana', 10))
        self.right_top_extra_attrib_entry = Entry(self.frame_left_top, textvariable=self.var_extra_attrib, font=('Verdana', 10))
        self.right_top_extra_attrib_label.grid(row=7, column=0)  # 位置设置
        self.right_top_extra_attrib_entry.grid(row=7, column=1,columnspan=2)


        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 15))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=20,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=20,
                                            command=self.del_row)

        # 定义下方区域，查询功能块
        self.chaxun = StringVar()
        self.right_bottom_id_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='物品id查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_id_entry.grid(row=0, column=1)

        # 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=5)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        # 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        if self.chaxun.get() == '':
            sql = "SELECT * FROM t_goods where goods_class='%s'"% (self.goods_class)
        else:
            sql = "SELECT * FROM t_goods where id='%s'" % (self.chaxun.get())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.name = []
            self.number = []
            self.price = []
            self.address = []
            self.tele = []
            self.extra_attrib = []
            # 向表格中插入数据
            for row in results:
                self.id.append(row[1])
                self.name.append(row[2])
                self.number.append(row[3])
                self.price.append(row[4])
                self.address.append(row[5])
                self.tele.append(row[6])
                self.extra_attrib.append(row[7])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()  # 关闭数据库连接

        for i in range(min(len(self.id), len(self.name), len(self.number), len(self.price),len(self.address), len(self.tele), len(self.extra_attrib))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.number[i], self.price[i],self.address[i], self.tele[i], self.extra_attrib[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    # 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        self.var_name.set(self.row_info[1])
        self.var_number.set(self.row_info[2])
        self.var_price.set(self.row_info[3])
        self.var_address.set(self.row_info[4])
        self.var_tele.set(self.row_info[5])
        self.var_extra_attrib.set(self.row_info[6])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

    # 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def new_row(self):
        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_id.get() != '' and self.var_name.get() != '' and self.var_number.get() != '' and self.var_price.get() != ''and self.var_address.get() != '' and self.var_tele.get() != ''and self.var_extra_attrib.get() != '' :
                # 打开数据库连接
                db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "INSERT INTO t_goods(goods_class,id, name, number , price ,address ,tele,extra_attrib ) \
				       VALUES ('%s','%s', '%s', '%s', '%s','%s', '%s', '%s')" % \
                      (self.goods_class,self.var_id.get(), self.var_name.get(), self.var_number.get(), self.var_price.get(),self.var_address.get(), self.var_tele.get(),self.var_extra_attrib.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                db.close()  # 关闭数据库连接

                self.id.append(self.var_id.get())
                self.name.append(self.var_name.get())
                self.number.append(self.var_number.get())
                self.price.append(self.var_price.get())
                self.address.append(self.var_address.get())
                self.tele.append(self.var_tele.get())
                self.extra_attrib.append(self.var_extra_attrib.get())

                self.tree.insert('', len(self.id) - 1, values=(
                    self.id[len(self.id) - 1], self.name[len(self.id) - 1], self.number[len(self.id) - 1],
                    self.price[len(self.id) - 1],self.address[len(self.id) - 1], self.tele[len(self.id) - 1], self.extra_attrib[len(self.id) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')

    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            # 打开数据库连接
            db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "UPDATE t_goods SET id = '%s', goods_class='%s',name = '%s', number = '%s', price = '%s', address = '%s', tele = '%s', extra_attrib = '%s' where id = '%s'" % (
            self.var_id.get(), self.goods_class,self.var_name.get(), self.var_number.get(), self.var_price.get(),self.var_address.get(), self.var_tele.get(), self.var_extra_attrib.get(), self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            self.name[id_index] = self.var_name.get()
            self.number[id_index] = self.var_number.get()
            self.price[id_index] = self.var_price.get()
            self.address[id_index] = self.var_address.get()
            self.tele[id_index] = self.var_tele.get()
            self.extra_attrib[id_index] = self.var_extra_attrib.get()

            self.tree.item(self.tree.selection()[0], values=(
                self.var_id.get(), self.var_name.get(), self.var_number.get(),
                self.var_price.get(),self.var_address.get(), self.var_tele.get(), self.var_extra_attrib.get()))  # 修改对于行信息

    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "DELETE FROM t_goods where id = '%s'" % (self.row_info[0])  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            print(id_index)
            del self.id[id_index]
            del self.name[id_index]
            del self.number[id_index]
            del self.price[id_index]
            del self.address[id_index]
            del self.tele[id_index]
            del self.extra_attrib[id_index]
            print(self.id)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

    def back(self):
        All_admin(self.window)  # 进入管理员子菜单操作界面


class GoodsInfo:
    def __init__(self, parent_window, goods_class):
        parent_window.destroy()  # 自动销毁上一个界面
        self.window = Tk()  # 初始框的声明
        self.window.title('管理员操作界面')
        self.window.geometry("850x685+300+30")  # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=300, height=200)  # 指定框架，在窗口上可以显示，这里指定四个框架
        self.frame_right_top = tk.Frame(width=200, height=200)
        self.frame_center = tk.Frame(width=800, height=350)
        self.frame_bottom = tk.Frame(width=650, height=70)

        # 定义下方中心列表区域
        self.columns = ("物品id", "物品名称", "物品数量", "物品价格", "物品地址", "联系电话", "额外属性")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0
        self.goods_class = goods_class
        # 表格的标题
        self.tree.column("物品id", width=100, anchor='center')
        self.tree.column("物品名称", width=100, anchor='center')
        self.tree.column("物品数量", width=100, anchor='center')
        self.tree.column("物品价格", width=100, anchor='center')
        self.tree.column("物品地址", width=100, anchor='center')
        self.tree.column("联系电话", width=150, anchor='center')
        self.tree.column("额外属性", width=150, anchor='center')

        # grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 定义几个数组，为中间的那个大表格做一些准备
        self.id = []
        self.name = []
        self.number = []
        self.price = []
        self.address = []
        self.tele = []
        self.extra_attrib = []

        # 打开数据库连接
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_goods where goods_class  = '%s'" % (self.goods_class)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[1])
                self.name.append(row[2])
                self.number.append(row[3])
                self.price.append(row[4])
                self.address.append(row[5])
                self.tele.append(row[6])
                self.extra_attrib.append(row[7])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(
                min(len(self.id), len(self.name), len(self.number), len(self.price), len(self.address), len(self.tele),
                    len(self.extra_attrib))):  # 写入数据
            self.tree.insert('', i, values=(
            self.id[i], self.name[i], self.number[i], self.price[i], self.address[i], self.tele[i],
            self.extra_attrib[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="商品信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=5)  # NSEW表示允许组件向4个方向都可以拉伸

        # 定义下方区域
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_name = StringVar()  # 声明姓名
        self.var_number = StringVar()  # 声明性别
        self.var_price = StringVar()  # 声明年龄
        self.var_address = StringVar()  # 声明姓名
        self.var_tele = StringVar()  # 声明性别
        self.var_extra_attrib = StringVar()  # 声明年龄
        # 商品id
        self.right_top_id_label = Label(self.frame_left_top, text="物品id： ", font=('Verdana', 10))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 10))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1, columnspan=2)
        # 商品名称
        self.right_top_name_label = Label(self.frame_left_top, text="物品名称：", font=('Verdana', 10))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 10))
        self.right_top_name_label.grid(row=2, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=2, column=1, columnspan=2)
        # 商品价格
        self.right_top_price_label = Label(self.frame_left_top, text="物品价格：", font=('Verdana', 10))
        self.right_top_price_entry = Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 10))
        self.right_top_price_label.grid(row=3, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=3, column=1, columnspan=2)
        # 销售数量
        self.right_top_number_label = Label(self.frame_left_top, text="物品数量：", font=('Verdana', 10))
        self.right_top_number_entry = Entry(self.frame_left_top, textvariable=self.var_number, font=('Verdana', 10))
        self.right_top_number_label.grid(row=4, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=4, column=1, columnspan=2)

        self.right_top_tele_label = Label(self.frame_left_top, text="联系电话：", font=('Verdana', 10))
        self.right_top_tele_entry = Entry(self.frame_left_top, textvariable=self.var_tele, font=('Verdana', 10))
        self.right_top_tele_label.grid(row=5, column=0)  # 位置设置
        self.right_top_tele_entry.grid(row=5, column=1, columnspan=2)

        self.right_top_address_label = Label(self.frame_left_top, text="物品地址：", font=('Verdana', 10))
        self.right_top_address_entry = Entry(self.frame_left_top, textvariable=self.var_address, font=('Verdana', 10))
        self.right_top_address_label.grid(row=6, column=0)  # 位置设置
        self.right_top_address_entry.grid(row=6, column=1, columnspan=2)

        self.right_top_extra_attrib_label = Label(self.frame_left_top, text="额外属性：", font=('Verdana', 10))
        self.right_top_extra_attrib_entry = Entry(self.frame_left_top, textvariable=self.var_extra_attrib,
                                                  font=('Verdana', 10))
        self.right_top_extra_attrib_label.grid(row=7, column=0)  # 位置设置
        self.right_top_extra_attrib_entry.grid(row=7, column=1, columnspan=2)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 15))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=20, command=self.new_row)

        # 定义下方区域，查询功能块
        self.chaxun = StringVar()
        self.right_bottom_id_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='物品id查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_id_entry.grid(row=0, column=1)

        # 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=5)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)

        # 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        # 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        if self.chaxun.get() == '':
            sql = "SELECT * FROM t_goods where goods_class='%s'" % (self.goods_class)
        else:
            sql = "SELECT * FROM t_goods where id='%s'" % (self.chaxun.get())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.name = []
            self.number = []
            self.price = []
            self.address = []
            self.tele = []
            self.extra_attrib = []
            # 向表格中插入数据
            for row in results:
                self.id.append(row[1])
                self.name.append(row[2])
                self.number.append(row[3])
                self.price.append(row[4])
                self.address.append(row[5])
                self.tele.append(row[6])
                self.extra_attrib.append(row[7])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()  # 关闭数据库连接

        for i in range(
                min(len(self.id), len(self.name), len(self.number), len(self.price), len(self.address), len(self.tele),
                    len(self.extra_attrib))):  # 写入数据
            self.tree.insert('', i, values=(
            self.id[i], self.name[i], self.number[i], self.price[i], self.address[i], self.tele[i],
            self.extra_attrib[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    # 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        self.var_name.set(self.row_info[1])
        self.var_number.set(self.row_info[2])
        self.var_price.set(self.row_info[3])
        self.var_address.set(self.row_info[4])
        self.var_tele.set(self.row_info[5])
        self.var_extra_attrib.set(self.row_info[6])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

    # 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def new_row(self):
        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_id.get() != '' and self.var_name.get() != '' and self.var_number.get() != '' and self.var_price.get() != '' and self.var_address.get() != '' and self.var_tele.get() != '' and self.var_extra_attrib.get() != '':
                # 打开数据库连接
                db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "INSERT INTO t_goods(goods_class,id, name, number , price ,address ,tele,extra_attrib ) \
    				       VALUES ('%s','%s', '%s', '%s', '%s','%s', '%s', '%s')" % \
                      (self.goods_class, self.var_id.get(), self.var_name.get(), self.var_number.get(),
                       self.var_price.get(), self.var_address.get(), self.var_tele.get(),
                       self.var_extra_attrib.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                db.close()  # 关闭数据库连接

                self.id.append(self.var_id.get())
                self.name.append(self.var_name.get())
                self.number.append(self.var_number.get())
                self.price.append(self.var_price.get())
                self.address.append(self.var_address.get())
                self.tele.append(self.var_tele.get())
                self.extra_attrib.append(self.var_extra_attrib.get())

                self.tree.insert('', len(self.id) - 1, values=(
                    self.id[len(self.id) - 1], self.name[len(self.id) - 1], self.number[len(self.id) - 1],
                    self.price[len(self.id) - 1], self.address[len(self.id) - 1], self.tele[len(self.id) - 1],
                    self.extra_attrib[len(self.id) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')

    # def updata_row(self):
    #     res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
    #     if res == True:
    #         # 打开数据库连接
    #         db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
    #         cursor = db.cursor()  # 使用cursor()方法获取操作游标
    #         sql = "UPDATE t_goods SET id = '%s', goods_class='%s',name = '%s', number = '%s', price = '%s', address = '%s', tele = '%s', extra_attrib = '%s' where id = '%s'" % (
    #             self.var_id.get(), self.goods_class, self.var_name.get(), self.var_number.get(), self.var_price.get(),
    #             self.var_address.get(), self.var_tele.get(), self.var_extra_attrib.get(), self.id1)  # SQL 插入语句
    #         try:
    #             cursor.execute(sql)  # 执行sql语句
    #             db.commit()  # 提交到数据库执行
    #             messagebox.showinfo('提示！', '更新成功！')
    #         except:
    #             db.rollback()  # 发生错误时回滚
    #             messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
    #         db.close()  # 关闭数据库连接
    #
    #         id_index = self.id.index(self.row_info[0])
    #         self.name[id_index] = self.var_name.get()
    #         self.number[id_index] = self.var_number.get()
    #         self.price[id_index] = self.var_price.get()
    #         self.address[id_index] = self.var_address.get()
    #         self.tele[id_index] = self.var_tele.get()
    #         self.extra_attrib[id_index] = self.var_extra_attrib.get()
    #
    #         self.tree.item(self.tree.selection()[0], values=(
    #             self.var_id.get(), self.var_name.get(), self.var_number.get(),
    #             self.var_price.get(), self.var_address.get(), self.var_tele.get(),
    #             self.var_extra_attrib.get()))  # 修改对于行信息
    #
    # # 删除行
    # def del_row(self):
    #     res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
    #     if res == True:
    #         print(self.row_info[0])  # 鼠标选中的学号
    #         print(self.tree.selection()[0])  # 行号
    #         print(self.tree.get_children())  # 所有行
    #         # 打开数据库连接
    #         db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
    #         cursor = db.cursor()  # 使用cursor()方法获取操作游标
    #         sql = "DELETE FROM t_goods where id = '%s'" % (self.row_info[0])  # SQL 插入语句
    #         try:
    #             cursor.execute(sql)  # 执行sql语句
    #             db.commit()  # 提交到数据库执行
    #             messagebox.showinfo('提示！', '删除成功！')
    #         except:
    #             db.rollback()  # 发生错误时回滚
    #             messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
    #         db.close()  # 关闭数据库连接
    #
    #         id_index = self.id.index(self.row_info[0])
    #         print(id_index)
    #         del self.id[id_index]
    #         del self.name[id_index]
    #         del self.number[id_index]
    #         del self.price[id_index]
    #         del self.address[id_index]
    #         del self.tele[id_index]
    #         del self.extra_attrib[id_index]
    #         print(self.id)
    #         self.tree.delete(self.tree.selection()[0])  # 删除所选行
    #         print(self.tree.get_children())

    def back(self):
        All_user(self.window)  # 进入管理员子菜单操作界面



# 物品类型操作界面
class GoodsClassManage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 自动销毁上一个界面
        self.window = Tk()  # 初始框的声明
        self.window.title('物品类型管理界面')
        self.window.geometry("650x685+300+30")  # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=300, height=200)  # 指定框架，在窗口上可以显示，这里指定四个框架
        self.frame_right_top = tk.Frame(width=200, height=200)
        self.frame_center = tk.Frame(width=500, height=350)
        self.frame_bottom = tk.Frame(width=650, height=70)

        # 定义下方中心列表区域
        self.columns = ("物品类型", "额外属性")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0

        # 表格的标题
        self.tree.column("物品类型", width=200, anchor='center')
        self.tree.column("额外属性", width=200, anchor='center')


        # grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 定义几个数组，为中间的那个大表格做一些准备
        self.id = []
        self.attrib = []


        # 打开数据库连接
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_class"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.attrib.append(row[1])

        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.id), len(self.attrib))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.attrib[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="物品类型信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)  # NSEW表示允许组件向4个方向都可以拉伸

        # 定义下方区域
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='类型查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_attrib = StringVar()  # 声明姓名

        # 商品id
        self.right_top_id_label = Label(self.frame_left_top, text="物品类型： ", font=('Verdana', 10))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 10))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
        # 商品名称
        self.right_top_name_label = Label(self.frame_left_top, text="属性：", font=('Verdana', 10))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_attrib, font=('Verdana', 10))
        self.right_top_name_label.grid(row=2, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=2, column=1)


        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建物品类型', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中选中类型信息', width=20,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中类型信息', width=20,
                                            command=self.del_row)

        # 定义下方区域，查询功能块
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='类型查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        # 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        # 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        if self.chaxun.get() == '':
            sql = "SELECT * FROM t_class "
        else:
            sql = "SELECT * FROM t_class where id = '%s'" % (self.chaxun.get())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.attrib = []

            # 向表格中插入数据
            for row in results:
                self.id.append(row[0])
                self.attrib.append(row[1])


        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()  # 关闭数据库连接

        print("进行数据的插入")
        for i in range(min(len(self.id), len(self.attrib))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.attrib[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    # 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        self.var_attrib.set(self.row_info[1])

        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

    # 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def new_row(self):

        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_id.get() != '' and self.var_attrib.get() != '' :
                # 打开数据库连接
                db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "INSERT INTO t_class(id, attrib) \
    				       VALUES ('%s', '%s')" % \
                      (self.var_id.get(), self.var_attrib.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                db.close()  # 关闭数据库连接

                self.id.append(self.var_id.get())
                self.attrib.append(self.var_attrib.get())

                self.tree.insert('', len(self.id) - 1, values=(
                    self.id[len(self.id) - 1], self.attrib[len(self.id) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')

    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            # 打开数据库连接
            db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "UPDATE t_class SET id = '%s', attrib = '%s' where id = '%s'" % (
                self.var_id.get(), self.var_attrib.get(), self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            self.attrib[id_index] = self.var_attrib.get()


            self.tree.item(self.tree.selection()[0], values=(
                self.var_id.get(), self.var_attrib.get()))  # 修改对于行信息

    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "DELETE FROM t_class where id = '%s'" % (self.row_info[0])
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            print(id_index)
            del self.id[id_index]
            del self.attrib[id_index]
            print(self.id)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

    def back(self):
        All_admin(self.window)  # 进入管理员子菜单操作界面
#用户管理
class User_Request:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = Tk()  # 初始框的声明
        self.window.geometry("650x720+300+30")  # 初始窗口在屏幕中的位置
        self.window.title('用户管理界面')

        self.frame_right_top = tk.Frame(width=300, height=230)
        self.frame_center = tk.Frame(width=600, height=360)
        self.frame_bottom = tk.Frame(width=650, height=60)

        self.id1 = 0

        # 定义下方中心列表区域
        self.columns = ("用户昵称", "用户密码","用户电话","用户住址")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("用户昵称", width=150, anchor='center')  # 表示列,不显示
        self.tree.column("用户密码", width=150, anchor='center')
        self.tree.column("用户电话", width=150, anchor='center')  # 表示列,不显示
        self.tree.column("用户住址", width=150, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.userRequest_id = []
        self.userRequest_pass = []
        self.userRequest_tele = []
        self.userRequest_address = []
        self.var_name= StringVar()
        self.var_pass= StringVar()
        # 打开数据库连接
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_userRequest"  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.userRequest_id.append(row[0])
                self.userRequest_pass.append(row[1])
                self.userRequest_tele.append(row[2])
                self.userRequest_address.append(row[3])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.userRequest_id), len(self.userRequest_pass),len(self.userRequest_tele), len(self.userRequest_address))):  # 写入数据
            self.tree.insert('', i, values=(self.userRequest_id[i], self.userRequest_pass[i],self.userRequest_tele[i], self.userRequest_address[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='更新申请信息', width=20,
                                            command=self.updata_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='接受申请', width=20,
                                            command=self.accept_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='拒绝申请', width=20,
                                            command=self.del_row)
        # 定义下方区域
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='id查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frame_right_top.grid(row=0, column=1, columnspan=2, padx=60, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=30, pady=5)
        self.frame_bottom.grid(row=2, column=1, columnspan=2)

        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        All_admin(self.window)  # 进入管理员子菜单操作界面

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        if self.chaxun.get() == '':
            sql = "SELECT * FROM t_userRequest "
        else:
            sql = "SELECT * FROM t_userRequest where userRequest_id = '%s'" % (self.chaxun.get())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.userRequest_id = []
            self.userRequest_pass = []
            self.userRequest_tele = []
            self.userRequest_address = []
            # 向表格中插入数据
            for row in results:
                self.userRequest_id.append(row[0])
                self.userRequest_pass.append(row[1])
                self.userRequest_tele.append(row[2])
                self.userRequest_address.append(row[3])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()  # 关闭数据库连接

        for i in range(min(len(self.userRequest_id), len(self.userRequest_pass))):  # 写入数据
            self.tree.insert('', i, values=(self.userRequest_id[i], self.userRequest_pass[i], self.userRequest_tele[i], self.userRequest_address[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_name.set(self.row_info[0])
        self.id1 = self.var_name.get()
        print(self.id1)
        self.var_pass.set(self.row_info[1])

        print('')

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def updata_row(self):
        self.delButton()
        self.userRequest_id = []
        self.userRequest_pass = []
        self.userRequest_tele = []
        self.userRequest_address = []
        db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_userRequest"  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.userRequest_id.append(row[0])
                self.userRequest_pass.append(row[1])
                self.userRequest_tele.append(row[2])
                self.userRequest_address.append(row[3])
            for i in range(min(len(self.userRequest_id), len(self.userRequest_pass))):  # 写入数据
                self.tree.insert('', i, values=(self.userRequest_id[i], self.userRequest_pass[i], self.userRequest_tele[i], self.userRequest_address[i]))

            for col in self.columns:  # 绑定函数，使表头可排序
                self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            messagebox.showinfo('提示！', '更新成功！')
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接
    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "DELETE FROM t_userRequest WHERE userRequest_id = '%s'" % (self.row_info[0])
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            id_index = self.userRequest_id.index(self.row_info[0])
            print(id_index)
            del self.userRequest_id[id_index]
            del self.userRequest_pass[id_index]
            del self.userRequest_tele[id_index]
            del self.userRequest_address[id_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())



    def accept_row(self):
        res = messagebox.askyesnocancel('警告！', '是否接受所选申请？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = pymssql.connect('localhost', 'sa', '123456789', 'EMIS')
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "INSERT INTO t_user(user_id,user_pass) \
                   VALUES ('%s', '%s')" % \
                  (
                      self.row_info[0], self.row_info[1])  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行

                sql = "DELETE FROM t_userRequest WHERE userRequest_id = '%s'" % (self.row_info[0])
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                    messagebox.showinfo('提示！', '接受成功！')

                    id_index = self.userRequest_id.index(self.row_info[0])
                    print(id_index)
                    del self.userRequest_id[id_index]
                    del self.userRequest_pass[id_index]
                    del self.userRequest_tele[id_index]
                    del self.userRequest_address[id_index]
                    self.tree.delete(self.tree.selection()[0])  # 删除所选行
                    print(self.tree.get_children())

                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '删除失败,数据库连接失败！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '接受失败，数据库连接失败！')

            db.close()  # 关闭数据库连接


# About页面
class AboutPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('关于')
        self.window.geometry('400x450+500+100')  # 这里的乘是小x

        label = tk.Label(self.window, text='商品信息管理系统', bg='green', font=('Verdana', 20), width=30, height=2)
        label.pack()

        Label(self.window, text='作者：Cylanx', font=('Verdana', 18)).pack(pady=30)
        Label(self.window, text='联系方式：1418561186@qq.com', font=('Verdana', 18)).pack(pady=5)

        Button(self.window, text="返回", width=8, font=tkFont.Font(size=12), command=self.back).pack(pady=100)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        All_user(self.window)  # 显示主窗口 销毁本窗口


if __name__ == '__main__':
    # 实例化Application
    window = tk.Tk()
    StartPage(window)
