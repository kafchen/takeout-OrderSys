import pymysql
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox  # 弹窗
from ttkbootstrap import Style


# 开始页面
class StartPage:
    def __init__(self, parent_window):
        parent_window.update()
        parent_window.destroy()  # 销毁子界面

        self.style = Style(theme='cjp')
        self.window = self.style.master
        # self.window = tk.Tk() # 初始框的声明
        self.window.title('餐饮外卖销售系统')
        self.window.geometry('800x600+350+100')  # 这里的乘是小x
        self.photo = PhotoImage(file=r"head.gif")
        self.label_photo = Label(self.window, image=self.photo).pack()

        label = Label(self.window, text="餐饮外卖销售系统",fg='green',font=("Verdana", 20))
        label.pack(pady=30)  # pady=100 界面的长度

        Button(self.window, text="我是商家", font=tkFont.Font(size=16), command=lambda: sellerPage(self.window), width=30,
               height=2,
               fg='white', bg='green', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="我是客户", font=tkFont.Font(size=16), command=lambda: CustomerPage(self.window), width=30,
               height=2, fg='white', bg='green', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="关于", font=tkFont.Font(size=16), command=lambda: AboutPage(self.window), width=30,
               height=2,
               fg='white', bg='green', activebackground='black', activeforeground='white').pack()
        Button(self.window, text='退出系统', height=2, font=tkFont.Font(size=16), width=30, command=self.window.destroy,
               fg='white', bg='green', activebackground='black', activeforeground='white').pack()

        self.window.mainloop()  # 主消息循环


# 商家登陆页面
class sellerPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        # self.window = tk.Tk()  # 初始框的声明
        self.style = Style(theme='cjp')
        self.window = self.style.master
        self.window.title('商家登陆页面')
        self.window.geometry('400x450+550+150')  # 这里的乘是小x

        label = tk.Label(self.window, text='商家登陆',fg='white', bg='green', font=('Verdana', 20), width=50, height=2)
        label.pack()

        Label(self.window, text='商家账号：', font=tkFont.Font(size=14)).pack(pady=25)
        self.seller_username = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory')  #创建文本框
        self.seller_username.pack()

        Label(self.window, text='商家密码：', font=tkFont.Font(size=14)).pack(pady=25)
        self.seller_pass = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory', show='*')
        self.seller_pass.pack(pady=10)

        Button(self.window, text="登 陆", width=16, fg='white', bg='green', font=tkFont.Font(size=12), command=self.login).pack(pady=10)
        Button(self.window, text="注 册", width=16, fg='white', bg='green', font=tkFont.Font(size=12), command=lambda: RegisterPage(1)).pack()
        Button(self.window, text="返回首页", width=16, fg='white', bg='green', font=tkFont.Font(size=12), command=self.back).pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        print(str(self.seller_username.get()))  # 打印获取到的文本框收到内容
        print(str(self.seller_pass.get()))
        global user_id
        global user_pwd
        user_id = self.seller_username.get()
        user_pwd = self.seller_pass.get()
        seller_pass = None

        # 数据库操作 查询商家表
        db = pymysql.connect(host ='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM seller_info WHERE seller_id = '%s'" % (user_id )  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                seller_id = row[0]
                seller_pass = row[1]
                # 打印结果
                print("seller_id=%s,seller_pass=%s" % (seller_id, seller_pass))
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '用户名或密码不正确！')
        db.close()  # 关闭数据库连接

        print("正在登陆商家管理界面")
        print("输入", str((self.seller_pass).get()))
        print("pwd", seller_pass)

        if self.seller_pass.get() == seller_pass:
            sellerManage(self.window,self.seller_username.get())  # 进入商家操作界面
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口


# 客户登陆页面
class CustomerPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        # self.window = tk.Tk()  # 初始框的声明
        self.style = Style(theme='cjp')
        self.window = self.style.master
        self.window.title('客户登陆')
        self.window.geometry('400x450+550+150')  # 这里的乘是小x

        label = tk.Label(self.window, text='客户登陆',fg='white', bg='green', font=('Verdana', 20), width=30, height=2)
        label.pack()

        Label(self.window, text='客户账号：', font=tkFont.Font(size=14)).pack(pady=25)
        self.customer_id = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory')
        self.customer_id.pack()

        Label(self.window, text='客户密码：', font=tkFont.Font(size=14)).pack(pady=25)
        self.customer_pass = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory', show='*')
        self.customer_pass.pack(pady=10)

        Button(self.window, text="登 陆", width=16,fg='white', bg='green', font=tkFont.Font(size=12), command=self.login).pack(pady=10)
        Button(self.window, text="注 册", width=16,fg='white', bg='green', font=tkFont.Font(size=12), command=lambda: RegisterPage(0)).pack()
        Button(self.window, text="返回首页", width=16,fg='white', bg='green', font=tkFont.Font(size=12), command=self.back).pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        global user_id
        global user_pwd
        user_id = self.customer_id.get()
        user_pwd = self.customer_pass.get()
        print(user_id)
        print(user_pwd)
        customer_pass = None

        # 数据库操作 查询
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM customer_info WHERE customer_id = '%s'" % (user_id)  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                customer_id = row[0]
                customer_pass = row[1]
                # 打印结果
                print("customer_id=%s,customer_pass=%s" % (customer_id, customer_pass))
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '用户名或密码不正确！')
        db.close()  # 关闭数据库连接

        print("正在登陆客户界面")
        print("self", self.customer_pass.get())
        print("pwd", customer_pass)

        if self.customer_pass.get() == customer_pass:
           customerView(self.window, self.customer_id.get())  # 进入客户信息查看界面
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口





# 商家操作界面
class sellerManage:
    def __init__(self, parent_window, seller_id):
        parent_window.destroy()  # 销毁主界面
        print(seller_id)
        # self.main_window = tk.Tk()
        self.style = Style(theme='cjp')
        self.main_window = self.style.master
        self.main_window.title('商家界面')
        self.main_window.geometry('800x550')
        self.order_list = set()  # 当前购买的
        self.user_id = seller_id  # 登录的用户ID
        self.left_index = 620  # 保证控件左边对齐
        # 标签 用户名密码
        tk.Label(self.main_window, text='店铺名: ').place(x=self.left_index + 20, y=30)
        tk.Label(self.main_window, text='营业额: ').place(x=self.left_index + 20, y=60)
        tk.Label(self.main_window, text='已选:').place(x=40, y=480)
        self.total_cost_show = tk.StringVar()  # 用于展示已选数量
        tk.Label(self.main_window, textvariable=self.total_cost_show).place(x=70, y=480)
        self.total_cost_show.set("当前为0")

        self.total_wallet_show = tk.StringVar()  # 用于展示营业额
        tk.Label(self.main_window, textvariable=self.total_wallet_show).place(x=self.left_index + 70, y=60)

        self.total_username_show = tk.StringVar()  # 用于展示用户名
        tk.Label(self.main_window, textvariable=self.total_username_show).place(x=self.left_index + 70, y=30)

        bt_charge = tk.Button(self.main_window, text='提现金额', height=1, width=16,fg='white', bg='green', command=lambda: charge_money(1))
        bt_charge.place(x=self.left_index, y=180)
        bt_user_info = tk.Button(self.main_window, text='查询修改店铺信息', height=1, width=16,fg='white', bg='green', command=lambda: alter_info(1))
        bt_user_info.place(x=self.left_index, y=150)
        bt_food = tk.Button(self.main_window, text='商品管理', height=1, width=16,fg='white', bg='green', command=lambda: manage_food())
        bt_food.place(x=self.left_index, y=120)
        bt_submit = tk.Button(self.main_window, text='完成订单', height=1, width=10,fg='white', bg='green', command=lambda: self.finish_order())
        bt_submit.place(x=240, y=480)
        bt_flush_order = tk.Button(self.main_window, text='刷  新', height=1, width=16,fg='white', bg='green', command=lambda: self.flush_info())
        bt_flush_order.place(x=self.left_index, y=240)
        bt_check_order = tk.Button(self.main_window, text='查看我的订单', height=1, width=16,fg='white', bg='green', command=lambda: check_order(1))
        bt_check_order.place(x=self.left_index, y=210)
        bt_back = tk.Button(self.main_window, text='返回首页', height=1, width=16,fg='white', bg='green', command=lambda: self.back())
        bt_back.place(x=self.left_index, y=400)

        self.orm = {}
        self.create_heading()
        self.create_tv()
        self.insert_tv()  # 进入时 刷新一次
        self.flush_info()


    def create_heading(self, ):
        '''重新做一个treeview的头，不然滚动滚动条，看不标题'''
        heading_frame = Frame(self.main_window)
        heading_frame.place(x=15, y=30)

        # 填充用
        button_frame = Label(heading_frame, width=1)
        button_frame.place(x=10, y=60)
        # 全选按钮
        self.all_buttonvar = IntVar()
        self.all_button = Checkbutton(heading_frame, text='', variable=self.all_buttonvar, command=self.select_all)
        self.all_button.pack(side=LEFT)
        self.all_buttonvar.set(0)

        self.columns = ['订单号', '客户', '客户地址', '客户电话', '订单总额']
        self.widths = [50, 80, 140, 100, 80]

        # 重建tree的头
        for i in range(len(self.columns)):
            Label(heading_frame, text=self.columns[i], width=int(self.widths[i]*0.16),fg='white', bg='green', anchor='center',
                  relief=GROOVE).pack(side=LEFT)

    def create_tv(self):
        # 放置 canvas、滚动条的frame
        canvas_frame = Frame(self.main_window, width=550, height=400)
        canvas_frame.place(x=10, y=60)

        # 只剩Canvas可以放置treeview和按钮，并且跟滚动条配合
        self.canvas = Canvas(canvas_frame, width=550, height=400, scrollregion=(0, 0, 550, 400))
        # self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.pack(side=LEFT)
        # 滚动条
        ysb = Scrollbar(canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=ysb.set)
        ysb.pack(side=RIGHT, fill=Y)
        # ysb.place(x=500, height=400)  # 滚动条的位置
        # 鼠标滚轮滚动时，改变的页面是canvas 而不是treeview
        self.canvas.bind_all("<MouseWheel>",
                             lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # 想要滚动条起效，得在canvas创建一个windows(frame)！！
        tv_frame = Frame(self.canvas)
        self.tv_frame = self.canvas.create_window(0, 0, window=tv_frame, anchor='nw', width=550,
                                                  height=400)  # anchor该窗口在左上方

        # 放置button的frame
        self.button_frame = Frame(tv_frame)
        self.button_frame.pack(side=LEFT, fill=Y)
        Label(self.button_frame, width=3).pack()  # 填充用

        # 创建treeview
        self.tv = ttk.Treeview(tv_frame, height=10, columns=self.columns, show='headings')  # height好像设定不了行数，实际由插入的行数决定
        self.tv.Scrollable = True
        self.tv.pack(expand=1, side=LEFT, fill=BOTH)
        # self.tv.place()
        # 设定每一列的属性
        width = [50, 80, 140, 100, 80]
        for i in range(len(self.columns)):
            self.tv.column(self.columns[i], width=width[i], minwidth=0, anchor='center', stretch=True)

        # 设定treeview格式
        self.tv.tag_configure('oddrow', font='Arial 12')  # 设定treeview里字体格式font=ft
        self.tv.tag_configure('select', background='SkyBlue', font='Arial 12')  # 当对应的按钮被打勾，那么对于的行背景颜色改变
        self.rowheight = 27  # tkinter里只能用整数
        ttk.Style().configure('Treeview', rowheight=self.rowheight)  # 设定每一行的高度

        # 设定选中的每一行字体颜色、背景颜色 (被选中时，没有变化)
        ttk.Style().map("Treeview",
                    foreground=[('focus', 'black'), ],
                    background=[('active', 'white')]
                    )
        self.tv.bind('<<TreeviewSelect>>', self.select_tree)  # 绑定tree选中时的回调函数

    def insert_tv(self):
        # 清空tree、checkbutton
        items = self.tv.get_children()
        [self.tv.delete(item) for item in items]
        self.tv.update()
        for child in self.button_frame.winfo_children()[1:]:  # 第一个构件是label，所以忽略
            child.destroy()

        # 重设tree、button对应关系
        self.orm = {}

        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        global cur_menu  # 使用全局的菜单变量
        cur_menu = []
        sql = "SELECT view_sell.订单号,view_sell.客户姓名,view_sell.客户地址,view_sell.客户电话,view_sell.订单总额 FROM %s %s;" % \
              ("view_sell , order_details", 'WHERE view_sell.订单号 = order_details.订单编号 AND  order_details.商家账号 = ' + user_id)
        try:  ###
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            cur_menu = cursor.fetchall()

            data_dict = []
            # 打印出标题
            for field in cursor.description:
                data_dict.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")

        i = 0
        for row in cur_menu:  # 格式：店名、商品、价格
            i += 1
            tv_item = self.tv.insert('', i, value=row, tags=('oddrow'))  # item默认状态tags
            ck_button = tk.Checkbutton(self.button_frame, variable=IntVar())
            ck_button['command'] = lambda item=tv_item: self.select_button(item)
            ck_button.pack()
            self.orm[tv_item] = [ck_button]

        # 每次点击插入tree，先设定全选按钮不打勾，接着打勾并且调用其函数
        self.all_buttonvar.set(1)
        self.all_button.invoke()
        self.order_list.clear()

        # 更新canvas的高度
        height = (len(self.tv.get_children()) + 1) * self.rowheight  # treeview实际高度
        self.canvas.itemconfigure(self.tv_frame, height=height)  # 设定窗口tv_frame的高度
        self.main_window.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # 滚动指定的范围

    def select_all(self):
        print("全选按钮")
        '''全选按钮的回调函数
           作用：所有多选按钮打勾、tree所有行都改变底色(被选中)'''
        for item, [button] in self.orm.items():
            a = eval("0x" + str(item[1:]))
            if self.all_buttonvar.get() == 1:
                button.select()
                self.tv.item(item, tags='select')
                self.order_list.add(a)
                # print("___全选")
            else:
                button.deselect()
                self.tv.item(item, tags='oddrow')
                if len(self.order_list) != 0:
                    self.order_list.remove(a)
                # print("___全不选")
        self.total_cost_show.set(len(self.order_list))
        # print(self.order_list)

    def select_button(self, item):
        print("单 选 ", end="")
        print(item)
        a = eval("0x" + str(item[1:]))
        print(a)
        a = a % len(cur_menu)
        if a in self.order_list:
            self.order_list.remove(a)
        else:
            self.order_list.add(a)
        print(self.order_list)
        self.total_cost_show.set(len(self.order_list))
        '''多选按钮的回调函数 作用：1.改变底色 2.修改all_button的状态'''
        button = self.orm[item][0]
        button_value = button.getvar(button['variable'])
        if button_value == '1':
            self.tv.item(item, tags='select')
        else:
            self.tv.item(item, tags='oddrow')
        self.all_button_select()  # 根据所有按钮改变 全选按钮状态

    def select_tree(self, event):
        '''tree绑定的回调函数
           作用：根据所点击的item改变 对应的按钮'''
        select_item = self.tv.focus()
        button = self.orm[select_item][0]
        button.invoke()  # 改变对应按钮的状态，而且调用其函数

    def all_button_select(self):
        '''根据所有按钮改变 全选按钮状态
            循环所有按钮，当有一个按钮没有被打勾时，全选按钮取消打勾'''
        for [button] in self.orm.values():
            button_value = button.getvar(button['variable'])
            if button_value == '0':
                self.all_buttonvar.set(0)
                break
        else:
            self.all_buttonvar.set(1)

    def flush_info(self):
        """从数据库查询最新消息并显示在控件上"""
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        self.flush_in = []
        sql = "SELECT * FROM %s %s;" % \
              (" seller_info", 'WHERE seller_id=' + user_id)
        try:  ###
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            self.flush_in = cursor.fetchall()

            self.flush_dict = []
            # 打印出标题
            for field in cursor.description:
                self.flush_dict.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")

        if len(self.flush_in) == 0:
            tk.messagebox.showerror(message='未从数据库获得消息，请检查')
        # print("从数据库查询到", end="")
        # print(self.flush_in)
        print("刷新成功")
        # 刷新用户名
        self.total_username_show.set(self.flush_in[0][3])
        # 刷新余额
        global rest_money
        rest_money = 0
        rest_money = self.flush_in[0][5]
        self.total_wallet_show.set(rest_money)

    def finish_order(self):
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标

        total_cost = 0  # 该订单总金额
        if len(self.order_list) == 0:
            tk.messagebox.showerror(message='空订单')
            return 0

        for i in self.order_list:
            total_cost += cur_menu[i - 1][4]

        print("本次获得金额：" + str(total_cost))

        global rest_money
        rest_money += total_cost
        # 修改数据库余额
        cursor.callproc('alter_seller_money', args=(user_id, rest_money))
        db.commit()

        print(self.order_list)

        for i in self.order_list:
            finish_sql = 'UPDATE order_info SET order_state = \'已完成\' WHERE order_id = ' + str(cur_menu[i - 1][0])
            cursor.execute(finish_sql)
            db.commit()

        # 更新控件上显示的数字
        self.flush_info()
        # 已选列表清空
        self.order_list.clear()
        self.total_cost_show.set(len(self.order_list))
        self.insert_tv()
        tk.messagebox.showinfo(title="通知", message="订单已完成！")

    def back(self):
        StartPage(self.main_window)  # 显示主窗口 销毁本窗口



# 客户查看信息界面
class customerView:
    def __init__(self, parent_window, customer_id):
        parent_window.destroy()  # 销毁主界面
        print(customer_id)
        # self.main_window = tk.Tk()
        self.style = Style(theme='cjp')
        self.main_window = self.style.master
        self.main_window.title('客户界面')
        self.main_window.geometry('700x550')
        # self. main_window.withdraw()  # 实现主窗口隐藏
        self.order_list = set()  # 当前购买的
        self.user_id = customer_id  # 登录的用户ID
        self.left_index = 520  # 保证控件左边对齐
        # 标签 用户名密码
        tk.Label(self.main_window, text='用户名:').place(x=self.left_index + 20, y=30)
        tk.Label(self.main_window, text='余  额:').place(x=self.left_index + 20, y=60)
        tk.Label(self.main_window, text='已选:').place(x=40, y=480)
        # tk.Label(self.main_window, text='最近购买的订单：').place(x=440, y=180)
        self.total_cost_show = tk.StringVar()  # 用于展示已选商品数量
        tk.Label(self.main_window, textvariable=self.total_cost_show).place(x=70, y=480)
        self.total_cost_show.set("当前为0")

        self.total_wallet_show = tk.StringVar()  # 用于展示余额
        tk.Label(self.main_window, textvariable=self.total_wallet_show).place(x=self.left_index + 70, y=60)

        self.total_username_show = tk.StringVar()  # 用于展示用户名
        tk.Label(self.main_window, textvariable=self.total_username_show).place(x=self.left_index + 70, y=30)

        bt_charge = tk.Button(self.main_window, text='充值余额', height=1, width=16,fg='white', bg='green', command=lambda: charge_money(0))
        bt_charge.place(x=self.left_index, y=180)
        bt_user_info = tk.Button(self.main_window, text='查询修改个人信息', height=1,fg='white', bg='green', width=16, command=lambda: alter_info(0))
        bt_user_info.place(x=self.left_index, y=150)
        bt_submit = tk.Button(self.main_window, text='提交订单', height=1, width=10,fg='white', bg='green', command=lambda: self.submit_order())
        bt_submit.place(x=380, y=480)
        bt_flush_order = tk.Button(self.main_window, text='刷  新', height=1, width=16,fg='white', bg='green', command=lambda: self.flush_info())
        bt_flush_order.place(x=self.left_index, y=240)
        bt_check_order = tk.Button(self.main_window, text='查看我的订单', height=1, width=16,fg='white', bg='green', command=lambda: check_order(0))
        bt_check_order.place(x=self.left_index, y=210)
        bt_back = tk.Button(self.main_window, text='返回首页', height=1, width=16,fg='white', bg='green', command=lambda: self.back())
        bt_back.place(x=self.left_index, y=400)

        self.orm = {}
        self.create_heading()
        self.create_tv()
        self.insert_tv()  # 进入时 刷新一次
        self.flush_info()

    def create_heading(self, ):
        '''重新做一个treeview的头，不然滚动滚动条，看不标题'''
        heading_frame = Frame(self.main_window)
        heading_frame.place(x=15, y=30)

        # 填充用
        button_frame = Label(heading_frame, width=1)
        button_frame.place(x=10, y=60)
        # 全选按钮
        self.all_buttonvar = IntVar()
        self.all_button = Checkbutton(heading_frame, text='', variable=self.all_buttonvar, command=self.select_all)
        self.all_button.pack(side=LEFT)
        self.all_buttonvar.set(0)

        self.columns = ['店铺', '商品', '价格', '种类']
        self.widths = [90,  90, 90, 90]

        # 重建tree的头
        for i in range(len(self.columns)):
            Label(heading_frame, text=self.columns[i], width=int(self.widths[i] * 0.16),fg='white', bg='green', anchor='center',
                  relief=GROOVE).pack(side=LEFT)

    def create_tv(self):
        # 放置 canvas、滚动条的frame
        canvas_frame = Frame(self.main_window, width=450, height=400)
        canvas_frame.place(x=10, y=60)

        # 只剩Canvas可以放置treeview和按钮，并且跟滚动条配合
        self.canvas = Canvas(canvas_frame, width=450, height=400, scrollregion=(0, 0, 400, 400))
        # self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.pack(side=LEFT)
        # 滚动条
        ysb = Scrollbar(canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=ysb.set)
        ysb.pack(side=RIGHT, fill=Y)
        # ysb.place(x=500, height=400)  # 滚动条的位置
        # 鼠标滚轮滚动时，改变的页面是canvas 而不是treeview
        self.canvas.bind_all("<MouseWheel>",
                             lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # 想要滚动条起效，得在canvas创建一个windows(frame)！！
        tv_frame = Frame(self.canvas)
        self.tv_frame = self.canvas.create_window(0, 0, window=tv_frame, anchor='nw', width=450,
                                                  height=400)  # anchor该窗口在左上方

        # 放置button的frame
        self.button_frame = Frame(tv_frame)
        self.button_frame.pack(side=LEFT, fill=Y)
        Label(self.button_frame, width=3).pack()  # 填充用

        # 创建treeview
        self.tv = ttk.Treeview(tv_frame, height=10, columns=self.columns, show='headings')  # height好像设定不了行数，实际由插入的行数决定
        self.tv.pack(expand=1, side=LEFT, fill=BOTH)
        # self.tv.place()
        # 设定每一列的属性
        widt = [90, 90, 90, 90,0]
        for i in range(len(self.columns)):
            self.tv.column(self.columns[i], width=widt[i], minwidth=0, anchor='center', stretch=True)

        # 设定treeview格式
        self.tv.tag_configure('oddrow', font='Arial 12')  # 设定treeview里字体格式font=ft
        self.tv.tag_configure('select', background='SkyBlue', font='Arial 12')  # 当对应的按钮被打勾，那么对于的行背景颜色改变
        self.rowheight = 27  # tkinter里只能用整数
        ttk.Style().configure('Treeview', rowheight=self.rowheight)  # 设定每一行的高度

        # 设定选中的每一行字体颜色、背景颜色 (被选中时，没有变化)
        ttk.Style().map("Treeview",
                    foreground=[('focus', 'black'), ],
                    background=[('active', 'white')]
                    )
        self.tv.bind('<<TreeviewSelect>>', self.select_tree)  # 绑定tree选中时的回调函数

    def insert_tv(self):
        # 清空tree、checkbutton
        items = self.tv.get_children()
        [self.tv.delete(item) for item in items]
        self.tv.update()
        for child in self.button_frame.winfo_children()[1:]:  # 第一个构件是label，所以忽略
            child.destroy()

        # 重设tree、button对应关系
        self.orm = {}

        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        global cur_menu  # 使用全局的菜单变量
        cur_menu = []
        sql = "SELECT * FROM %s %s;" % \
              ("view_buy", "")
        try:  ###
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            cur_menu = cursor.fetchall()

            data_dict = []
            # 打印出标题
            for field in cursor.description:
                data_dict.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")
        i = 0
        for row in cur_menu:  # 格式：店名、商品、价格
            i += 1
            tv_item = self.tv.insert('', i, value=row, tags=('oddrow'))  # item默认状态tags

            ck_button = tk.Checkbutton(self.button_frame, variable=IntVar())
            ck_button['command'] = lambda item=tv_item: self.select_button(item)
            ck_button.pack()
            self.orm[tv_item] = [ck_button]

        # 每次点击插入tree，先设定全选按钮不打勾，接着打勾并且调用其函数
        self.all_buttonvar.set(1)
        self.all_button.invoke()
        self.order_list.clear()

        # 更新canvas的高度
        height = (len(self.tv.get_children()) + 1) * self.rowheight  # treeview实际高度
        self.canvas.itemconfigure(self.tv_frame, height=height)  # 设定窗口tv_frame的高度
        self.main_window.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # 滚动指定的范围

    def select_all(self):
        print("全选按钮")
        '''全选按钮的回调函数
           作用：所有多选按钮打勾、tree所有行都改变底色(被选中)'''
        for item, [button] in self.orm.items():
            a = eval("0x" + str(item[1:]))
            if self.all_buttonvar.get() == 1:
                button.select()
                self.tv.item(item, tags='select')
                self.order_list.add(a)
                # print("___全选")
            else:
                button.deselect()
                self.tv.item(item, tags='oddrow')
                if len(self.order_list) != 0:
                    self.order_list.remove(a)
                # print("___全不选")
        self.total_cost_show.set(len(self.order_list))
        # print(self.order_list)

    def select_button(self, item):
        print("单 选 ", end="")
        print(item)
        a = eval("0x" + str(item[1:]))
        print(a)
        a = a % len(cur_menu)
        if a in self.order_list:
            self.order_list.remove(a)
        else:
            self.order_list.add(a)
        print(self.order_list)
        self.total_cost_show.set(len(self.order_list))
        '''多选按钮的回调函数 作用：1.改变底色 2.修改all_button的状态'''
        button = self.orm[item][0]
        button_value = button.getvar(button['variable'])
        if button_value == '1':
            self.tv.item(item, tags='select')
        else:
            self.tv.item(item, tags='oddrow')
        self.all_button_select()  # 根据所有按钮改变 全选按钮状态

    def select_tree(self, event):
        '''tree绑定的回调函数
           作用：根据所点击的item改变 对应的按钮'''
        select_item = self.tv.focus()
        button = self.orm[select_item][0]
        button.invoke()  # 改变对应按钮的状态，而且调用其函数

    def all_button_select(self):
        '''根据所有按钮改变 全选按钮状态
            循环所有按钮，当有一个按钮没有被打勾时，全选按钮取消打勾'''
        for [button] in self.orm.values():
            button_value = button.getvar(button['variable'])
            if button_value == '0':
                self.all_buttonvar.set(0)
                break
        else:
            self.all_buttonvar.set(1)

    def flush_info(self):
        """从数据库查询最新消息并显示在控件上"""
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        self.flush_in = []
        sql = "SELECT * FROM %s %s;" % \
              ("customer_info", 'WHERE customer_id=' + user_id)
        try:  ###
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            self.flush_in = cursor.fetchall()

            self.flush_dict = []
            # 打印出标题
            for field in cursor.description:
                self.flush_dict.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")

        if len(self.flush_in) == 0:
            tk.messagebox.showerror(message='未从数据库获得消息，请检查')
        # print("从数据库查询到", end="")
        # print(self.flush_in)
        print("刷新成功")
        # 刷新用户名
        self.total_username_show.set(self.flush_in[0][3])
        # 刷新余额
        global rest_money
        rest_money = 0
        rest_money = self.flush_in[0][5]
        self.total_wallet_show.set(rest_money)

    def submit_order(self):
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        total_cost = 0  # 该订单总金额
        if len(self.order_list) == 0:
            tk.messagebox.showerror(message='空订单')
            return 0
        for i in self.order_list:
            total_cost += cur_menu[i - 1][2]

        print("提交的订单总价为" + str(total_cost))

        global rest_money
        if rest_money < total_cost:  # 如果余额不足
            tk.messagebox.showerror(message='余额不足，提交订单失败')
            return 0

        rest_money -= total_cost
        # 修改数据库余额
        cursor.callproc('alter_cus_money', args=(user_id, rest_money))
        db.commit()
        print(cur_menu)
        print(self.order_list)

        seller=[]
        food_l=[]
        for i in self.order_list:
            seller = cur_menu[i - 1][4]
        for i in self.order_list:
            food_l += cur_menu[i - 1][1]
            food_l += ';'
        print(str(seller))
        food=''.join(food_l)
        print(str(food))

        sql = """
                insert into order_info values (null,{},'{}','{}','{}',{},'{}')
                """.format('NOW()', user_id, str(seller), str(food), total_cost, '正在出餐')
        cursor.execute(sql)
        try:
            db.commit()
        except:
            db.rollback()
        print('完成')

        # 更新控件上显示的数字
        self.flush_info()

        # 已选列表清空
        self.order_list.clear()
        self.total_cost_show.set(len(self.order_list))
        self.insert_tv()
        self.order_list.clear()
        tk.messagebox.showinfo(title="通知", message="订单提交成功！")

    def back(self):
        StartPage(self.main_window)  # 显示主窗口 销毁本窗口

# About页面
class AboutPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        # self.window = tk.Tk()  # 初始框的声明
        self.style = Style(theme='cjp')
        self.window = self.style.master
        self.window.title('关于')
        self.window.geometry('400x450+550+150')  # 这里的乘是小x

        label = tk.Label(self.window, text='餐饮外卖销售系统', bg='green', font=('Verdana', 20), width=30, height=2)
        label.pack()

        Label(self.window, text='华南理工大学', font=('Verdana', 18)).pack(pady=10)
        Label(self.window, text='自动化科学与工程学院', font=('Verdana', 18)).pack(pady=10)
        Label(self.window, text='智能科学与技术专业', font=('Verdana', 18)).pack(pady=10)
        Label(self.window, text='陈杰沛', font=('Verdana', 18)).pack(pady=10)
        Label(self.window, text='仅供学习使用', font=('Verdana', 18)).pack(pady=10)

        Button(self.window, text="返回首页", width=16, font=tkFont.Font(size=12), command=self.back).pack(pady=40)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口



class RegisterPage:            #注册页面
    def __init__(self,role):
        self.window = tk.Toplevel()   #新窗口顶上来
        self.window.title("注册界面")
        self.window.geometry('800x600+300+100')
        self.role = role   #注册角色 ，1是商家，0是客户
        # 添加图片   800x150
        self.photo = PhotoImage(file=r"head1.gif")
        self.label_photo = Label(self.window, image=self.photo).pack()

        #注册界面这几个字的放置
        self.label_title = Label(self.window, text="注册界面", fg="#FE9300", bg="#10DF74", font=("微软雅黑", 25, "bold"))
        self.label_title.place(x=550, y=40)

        # 创建添加的容器
        self.frame_login_num = Frame(self.window, width=800, height=350)
        self.frame_login_num.place(x=0, y=200)

        # 创建全局变量 这个可以跟踪变量值的变化，普通的python变量不能即时地显示在屏幕上面
        self.var_login_name = StringVar()
        self.var_login_passwd = StringVar()
        self.var_login_again_passwd = StringVar()
        self.var_login_phone = StringVar()

        self.id = []
        self.pwd = []
        # 打开数据库连接
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        if self.role == 1:
            sql = "SELECT * FROM seller_info"  # SQL 查询语句
        else:
            sql = "SELECT * FROM customer_info"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.pwd.append(row[1])

            print(self.id)
            print(self.pwd)

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接



        # 新用户名
        self.label_old_passwd = Label(self.frame_login_num, text="新账号:", font=("Verdana", 18), fg="#FE9300")
        self.label_old_passwd.place(x=210, y=70)
        self.entry_old_passwd = Entry(self.frame_login_num, font=('Verdana', 18), width=12,
                                      textvariable=self.var_login_name)
        self.entry_old_passwd.place(x=400, y=70)

        # 电话号码
        self.label_phone = Label(self.frame_login_num, text="电话号码:", font=("Verdana", 18), fg="#FE9300")
        self.label_phone.place(x=210, y=140)
        self.entry_phone = Entry(self.frame_login_num, font=('Verdana', 18), width=12,
                                      textvariable=self.var_login_phone)
        self.entry_phone.place(x=400, y=140)

        # 新用户密码
        self.label_new_passwd = Label(self.frame_login_num, text="新密码:", font=("Verdana", 18), fg="#FE9300")
        self.label_new_passwd.place(x=210, y=210)
        self.entry_new_passwd = Entry(self.frame_login_num, font=('Verdana', 18), width=12,
                                      textvariable=self.var_login_passwd,show="*")
        self.entry_new_passwd.place(x=400, y=210)

        # 确认新用户密码
        self.label_new_passwd = Label(self.frame_login_num, text="确认新密码:", font=("Verdana", 18), fg="#FE9300")
        self.label_new_passwd.place(x=210, y=280)
        self.entry_new_passwd = Entry(self.frame_login_num, font=('Verdana', 18), width=12,
                                      textvariable=self.var_login_again_passwd,show="*")
        self.entry_new_passwd.place(x=400, y=280)

        # 按钮组
        self.button_add = Button(self.window, text="注册", font=("Verdana", 15), width=8,fg='white', bg='green', command=self.alter)
        self.button_add.place(x=520, y=550)

        self.button_close = Button(self.window, text="关闭", font=("Verdana", 15), width=8,fg='white', bg='green', command=self.close)
        self.button_close.place(x=670, y=550)

        self.window.mainloop()



    def alter(self):
        login_name = self.var_login_name.get()
        login_passwd = self.var_login_passwd.get()
        login_again_passwd = self.var_login_again_passwd.get()
        login_phone = self.var_login_phone.get()
        print(str(self.var_login_name.get()))
        print(self.id)
        if str(self.var_login_name.get()) in self.id:
            messagebox.showinfo('警告！', '该账号已存在！')
            print(len(login_passwd))
        elif len(login_passwd) < 4:
            messagebox.showinfo("系统提示", "密码长度不能少于4")
        elif len(login_phone) < 11:
            messagebox.showinfo("系统提示", "电话号码位数有误")
        elif login_passwd !=  login_again_passwd:
            messagebox.showinfo("系统提示", "两次新密码不一致！")

        else:

            db = pymysql.connect(host ='localhost', port=3306, db='foodsys', user='root', password='5286')
            cursor = db.cursor()
            if self.role == 0:
                sql = "insert into seller_info (seller_id, seller_pass, seller_phone) values ('{}','{}',{})".format(login_name,login_passwd,login_phone)  #定义sql语句
            else:
                sql = "insert into customer_info (customer_id, customer_pass, customer_phone) values ('{}','{}',{})".format(login_name, login_passwd,login_phone)
            cursor.execute(sql) #执行sql语句
            try:
                db.commit()
                cursor.close()
                db.close()
                self.window.destroy()
                system_pop("用户注册成功")
            except:
                db.rollback()
                system_pop("用户注册失败")

    def close(self):
        self.window.destroy()


class system_pop:                 #弹窗页面
    def __init__(self,accept):
        self.accept=accept
        self.win = tk.Toplevel()
        self.win.geometry("220x180+500+350")
        self.win.title("系统提示")
        self.photo = PhotoImage(file=r"tip.gif")
        self.win_frame = Frame(self.win, width=220, height=130, bg="white")
        self.win_frame.place(x=0, y=0)
        Label(self.win_frame, image=self.photo, bg="white").place(x=22, y=45)
        Label(self.win_frame, text=self.accept, font=("Verdana", 13), bg="white").place(x=80, y=60)
        Button(self.win, text="确定", width=11,command=self.close).place(x=110, y=140)
        self.win.mainloop()
    def close(self):
        self.win.destroy()


class alter_info:  # 修改个人信息
    def __init__(self,role):
        self.alter_info_dict = []
        self.alter_pre_info = []
        self.role = role
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')
        cursor = db.cursor()
        if self.role == 1:
            sql = "SELECT * FROM %s %s;" % \
                  ('seller_info', 'WHERE seller_id=' + '\'' + user_id + '\'')
        else:
            sql = "SELECT * FROM %s %s;" % \
                  ('customer_info', 'WHERE customer_id=' + '\'' + user_id + '\'')

        try:  ###
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            self.alter_pre_info = cursor.fetchall()

            self.alter_info_dict = []
            # 打印出标题
            for field in cursor.description:
                self.alter_info_dict.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")

        info = self.alter_pre_info[0]
        print(self.alter_pre_info)

        # 新建修改信息界面
        self.window_alter_info = tk.Toplevel()
        self.window_alter_info.geometry('450x350+300+200')
        self.window_alter_info.title('查询/修改信息')
        # 用户名变量及标签、输入框
        self.alter_new_id = tk.StringVar()
        tk.Label(self.window_alter_info, text='账号：').place(x=10, y=10)
        tk.Label(self.window_alter_info, text=info[0] + ' ' * 30 + '不可更改').place(x=110, y=10)
        # tk.Entry(window_alter_info, textvariable=alter_new_id).place(x=250, y=10)
        # 老密码变量及标签、输入框
        self.alter_pwd_old = tk.StringVar()
        tk.Label(self.window_alter_info, text='老密码：').place(x=10, y=50)
        tk.Label(self.window_alter_info, text='****').place(x=110, y=50)
        tk.Entry(self.window_alter_info, textvariable=self.alter_pwd_old, show='*').place(x=250, y=50)
        # 新密码变量及标签、输入框
        self.alter_new_pwd_confirm = tk.StringVar()
        tk.Label(self.window_alter_info, text='新密码：').place(x=10, y=90)
        tk.Label(self.window_alter_info, text='****').place(x=110, y=90)
        tk.Entry(self.window_alter_info, textvariable=self.alter_new_pwd_confirm, show='*').place(x=250, y=90)
        # 姓名
        self.alter_new_name = tk.StringVar()
        if self.role == 0 :
            tk.Label(self.window_alter_info, text='姓名：').place(x=10, y=130)
        else:
            tk.Label(self.window_alter_info, text='商店名称：').place(x=10, y=130)
        tk.Label(self.window_alter_info, text=info[3]).place(x=110, y=130)
        tk.Entry(self.window_alter_info, textvariable=self.alter_new_name).place(x=250, y=130)
        # 电话
        self.alter_new_tel = tk.StringVar()
        tk.Label(self.window_alter_info, text='电话：').place(x=10, y=170)
        tk.Label(self.window_alter_info, text=info[2]).place(x=110, y=170)
        tk.Entry(self.window_alter_info, textvariable=self.alter_new_tel).place(x=250, y=170)
        # 住址
        self.alter_new_addr = tk.StringVar()
        tk.Label(self.window_alter_info, text='地址：').place(x=10, y=210)
        tk.Label(self.window_alter_info, text=info[4]).place(x=110, y=210)
        tk.Entry(self.window_alter_info, textvariable=self.alter_new_addr).place(x=250, y=210)

        tk.Label(self.window_alter_info, text='注意 :   请输入当前账号密码以确认修改').place(x=10, y=270)
        # 确认注册按钮及位置
        tk.Button(self.window_alter_info, text='确认修改', command=self.commit_info_change).place(x=250, y=310)

    def commit_info_change(self):
        identify_pwd = self.alter_pwd_old.get()
        global user_pwd
        if user_pwd != identify_pwd:
            tk.messagebox.showerror('错误', '密码错误')
            return

        # 从控件获取用户的输入
        altered_id = self.alter_new_id.get()
        altered_addr = self.alter_new_addr.get()
        altered_tel = self.alter_new_tel.get()
        altered_pwd = self.alter_new_pwd_confirm.get()
        altered_name = self.alter_new_name.get()

        # 将新信息提交到数据库
        changed = 0
        if self.role == 1:
            sql_alt = 'UPDATE seller_info SET '
            if altered_pwd != "":
                sql_alt += " seller_pass=\'" + altered_pwd + "\'"
                changed = 1
            if altered_addr != "":
                if changed == 1:
                    sql_alt += ','
                sql_alt += " seller_address=\'" + altered_addr + "\'"
                changed = 1
            if altered_tel != "":
                if changed == 1:
                    sql_alt += ','
                sql_alt += " seller_phone=\'" + altered_tel + "\'"
                changed = 1
            if altered_name != "":
                if changed == 1:
                    sql_alt += ','
                sql_alt += " seller_name=\'" + altered_name + "\'"
            sql_alt += "WHERE seller_id=\'" + user_id + "\';"

        else:
            sql_alt = 'UPDATE customer_info SET '
            if altered_pwd != "":
                sql_alt += " customer_pass=\'" + altered_pwd + "\'"
                changed = 1
            if altered_addr != "":
                if changed == 1:
                    sql_alt += ','
                sql_alt += " customer_address=\'" + altered_addr + "\'"
                changed = 1
            if altered_tel != "":
                if changed == 1:
                    sql_alt += ','
                sql_alt += " customer_phone=\'" + altered_tel + "\'"
                changed = 1
            if altered_name != "":
                if changed == 1:
                    sql_alt += ','
                sql_alt += " customer_name=\'" + altered_name + "\'"
            sql_alt += "WHERE customer_id=\'" + user_id + "\';"

        try:  # 执行SQL语句
            cursor.execute(sql_alt)
            db.commit()
            user_pwd = identify_pwd  # 修改本地缓存的密码
            tk.messagebox.showinfo(title="通知", message="修改成功！")
        except:
            db.rollback()
            print(sql_alt + "_失败")
        window_alter_info.withdraw()

    def close(self):
            self.window_alter_info.destroy()
    # 从数据库查询个人信息

class manage_food:
    def __init__(self):
        self.window_manage_food = tk.Toplevel()
        self.window_manage_food.geometry('800x520')
        self.window_manage_food.title('商品管理模块')

        self.left_index_m = 500
        # 商品名输入模块
        self.food_id = tk.StringVar()
        tk.Label(self.window_manage_food, text='商品ID').place(x=self.left_index_m, y=10)
        tk.Entry(self.window_manage_food, textvariable=self.food_id).place(x=self.left_index_m + 100, y=10)
        # 商品名输入模块
        self.food_name = tk.StringVar()
        tk.Label(self.window_manage_food, text='商品名称').place(x=self.left_index_m, y=50)
        tk.Entry(self.window_manage_food, textvariable=self.food_name).place(x=self.left_index_m + 100, y=50)
        # 商品名输入模块
        self.food_price = tk.StringVar()
        tk.Label(self.window_manage_food, text='价格').place(x=self.left_index_m, y=90)
        tk.Entry(self.window_manage_food, textvariable=self.food_price).place(x=self.left_index_m + 100, y=90)
        # 商品名输入模块
        self.food_num = tk.StringVar()
        tk.Label(self.window_manage_food, text='库存').place(x=self.left_index_m, y=130)
        tk.Entry(self.window_manage_food, textvariable=self.food_num).place(x=self.left_index_m + 100, y=130)
        # 商品种类输入模块
        self.food_type = tk.StringVar()
        self.types = ["主食", "小吃", "饮料"]
        tk.Label(self.window_manage_food, text='种类').place(x=self.left_index_m, y=170)
        self.choose = ttk.Combobox(self.window_manage_food, textvariable=self.food_type,values=self.types).place(x=self.left_index_m + 100, y=170)



        tk.Button(self.window_manage_food, text='新建商品', height=1, width=16,fg='white', bg='green', command=self.commit_new_food) \
            .place(x=self.left_index_m + 30, y=220)
        tk.Button(self.window_manage_food, text='修改商品', height=1, width=16,fg='white', bg='green', command=self.ulter_food) \
            .place(x=self.left_index_m + 30, y=270)
        tk.Button(self.window_manage_food, text='删除商品', height=1, width=16,fg='white', bg='green', command=self.delete_food) \
            .place(x=self.left_index_m + 30, y=320)
        tk.Button(self.window_manage_food, text='刷新商品', height=1, width=16,fg='white', bg='green', command=self.fresh_food) \
            .place(x=self.left_index_m + 30, y=370)


        self.ccolumns = ['商品ID', '',  '商品名称', '价格', '库存','商品种类']
        self.wwidth_ord = [90, 0, 90, 90, 90, 90]
        self.food_list_table = ttk.Treeview(
            master=self.window_manage_food,  # 父容器
            height=17,  # 表格显示的行数,height行
            columns=self.ccolumns,  # 显示的列
            show='headings',  # 隐藏首列
        )
        self.t = 0
        self.food_list_table.place(x=10, y=10)
        for i in self.ccolumns:
            self.food_list_table.heading(i, text=i)  # 定义表头
        for i in self.ccolumns:
            self.food_list_table.column(i, width=self.wwidth_ord[self.t], minwidth=0, anchor=S, )  # 定义列
            self.t += 1
        self.fresh_food()

    def commit_new_food(self):
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        results = []
        sql = "SELECT * FROM %s %s;" % \
              ('food', 'WHERE food_id = '+ '\'' + self.food_id.get() + '\'')
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            data_dict = []
            # 打印出标题
            for field in cursor.description:
                data_dict.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")

        if len(results) != 0:
            tk.messagebox.showerror(message='该商品号已存在')
            return
        if '' in [self.food_id.get(), user_id, self.food_name.get(), self.food_price.get(), self.food_num.get(),self.food_type.get()]:
            tk.messagebox.showerror(message='信息不全')
            return
        try:
            sql = "INSERT INTO food VALUES " + '(\'{}\',\'{}\',\'{}\',{},{},\'{}\')' \
                .format(self.food_id.get(), user_id, self.food_name.get(), self.food_price.get(), self.food_num.get(), self.food_type.get())

            cursor.execute(sql)
            db.commit()
            tk.messagebox.showinfo(title="通知", message="新建商品成功")
        except:
            db.rollback()
            print(sql + "操作失败")
            tk.messagebox.showerror(message='操作失败，请稍后重试')
        db.close()
        self.fresh_food()

    def ulter_food(self):
        # 从控件获取用户的输入
        # food_id.get(), user_id, food_name.get(), food_price.get(), food_num.get(), food_type.get()
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        # 将新信息提交到数据库
        changed = 0
        sql_alt = 'UPDATE food SET '
        if self.food_name.get() != "":
            sql_alt += " food_name=\'" + self.food_name.get() + "\'"
            changed = 1
        if self.food_price.get() != "":
            if changed == 1:
                sql_alt += ','
            sql_alt += " food_price=\'" + self.food_price.get() + "\'"
            changed = 1
        if self.food_num.get() != "":
            if changed == 1:
                sql_alt += ','
            sql_alt += " food_stock=\'" + self.food_num.get() + "\'"
        if self.food_type.get() != "":
            if changed == 1:
                sql_alt += ','
            sql_alt += " food_type=\'" + self.food_type.get() + "\'"
        sql_alt += " WHERE food_id=\'" + self.food_id.get() + "\' AND seller_id = "+ user_id
        try:  # 执行SQL语句
            cursor.execute(sql_alt)
            db.commit()
            tk.messagebox.showinfo(title="通知", message="修改成功！")
        except:
            db.rollback()
            print(sql_alt + "_失败")
        db.close()
        self.fresh_food()

    def delete_food(self):
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        try:
            sql = 'DELETE FROM food WHERE food_id = ' + self.food_id.get() + ' AND seller_id = '+ user_id
            cursor.execute(sql)
            db.commit()
            tk.messagebox.showinfo(title="通知", message="删除成功")
        except:
            db.rollback()
            print(sql + "操作失败")
            tk.messagebox.showerror(message='操作失败，请稍后重试')
        db.close()
        self.fresh_food()

    def fresh_food(self):
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        # 先清除旧的信息
        x = self.food_list_table.get_children()
        for item in x:
            self.food_list_table.delete(item)

        self.food_id.set("")
        self.food_name.set("")
        self.food_price.set("")
        self.food_num.set("")


        self.food_list = []
        sql = "SELECT * FROM %s %s;" % \
              ('food', 'WHERE seller_id = ' + '\'' + user_id + '\'')
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            self.food_list = cursor.fetchall()

            self.data_dict = []
            # 打印出标题
            for field in cursor.description:
                self.data_dict.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")
        db.close()
        for row in self.food_list:
            self.food_list_table.insert('', 'end', values=row)


class charge_money:
    def __init__(self,role):
        # 首先需要读取用户的 充值金额 验证密码
        # 新建充值界面
        self.window_charge_money = tk.Toplevel()
        self.window_charge_money.geometry('300x150+350+250')
        self.role = role
        if self.role == 0:
            self.window_charge_money.title('充值')
        else:
            self.window_charge_money.title('提现')
        self.charge_amount = tk.StringVar()
        tk.Label(self.window_charge_money, text='金额：').place(x=40, y=40)
        tk.Entry(self.window_charge_money, textvariable=self.charge_amount).place(x=130, y=40)
        # 密码变量及标签、输入框
        self.charge_pwd = tk.StringVar()
        tk.Label(self.window_charge_money, text='账户密码：').place(x=40, y=80)
        tk.Entry(self.window_charge_money, textvariable=self.charge_pwd, show='*').place(x=130, y=80)
        # 确认注册按钮及位置
        tk.Button(self.window_charge_money, text='确认', command=self.charge_money_in).place(x=230, y=110)


    def charge_money_in(self):
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标

        if self.charge_amount.get() == "" or int(self.charge_amount.get()) <= 0:
            tk.messagebox.showerror('错误', '金额有误')
        if self.role == 0:
            self.target_money = int(self.charge_amount.get()) + rest_money
        else:
            self.target_money = rest_money - int(self.charge_amount.get())
        identify_pwd = self.charge_pwd.get()
        if user_pwd != identify_pwd:
            tk.messagebox.showerror('错误', '密码错误')
            return
        # 修改数据库余额
        if self.role == 0:
            cursor.callproc('alter_cus_money', args=(user_id,  self.target_money))
        else:
            cursor.callproc('alter_seller_money', args=(user_id, self.target_money))
        db.commit()
        # flush_info(self)
        tk.messagebox.showinfo(title="通知", message="充值成功！")
        self.window_charge_money.withdraw()

class check_order:
    def __init__(self,role=0):
        # 新建查询订单界面
        self.window_check_order = tk.Toplevel()
        self.window_check_order.geometry('900x500')
        self.window_check_order.title('订单查询')
        self.role=role

        self.columns = ['订单号', '商家名称',  '商品', '订单总额', '状态', '', '客户名称', '客户电话', '客户地址','订单时间']
        width_ord = [60, 80, 120, 80, 80, 0, 80, 100, 120, 150]
        self.order_list_table = ttk.Treeview(
            master=self.window_check_order,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=self.columns,  # 显示的列
            show='headings',  # 隐藏首列
        )
        t = 0
        self.order_list_table.place(x=20, y=40)
        for i in self.columns:
            self.order_list_table.heading(i, text=i)  # 定义表头
        for i in self.columns:
            self.order_list_table.column(i, width=width_ord[t], minwidth=1, anchor=S, )  # 定义列
            t += 1

        self.check()
        # tk.Button(self.window_charge_money, text='确认充值', command=self.charge_money_in).place(x=180, y=80)

    def check(self):
        db = pymysql.connect(host='localhost', port=3306, db='foodsys', user='root', password='5286')  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标

        x = self.order_list_table.get_children()
        for item in x:
            self.order_list_table.delete(item)

        flu_list= []
        if self.role == 0:
            sql = "SELECT * FROM %s %s;" % \
                  ("order_details", 'WHERE 客户账号 = ' + user_id)
        else:
            sql = "SELECT * FROM %s %s;" % \
                  ("order_details", 'WHERE 商家账号 = ' + user_id)
        try:  ###
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            flu_list = cursor.fetchall()

            data_dict_buy = []
            # 打印出标题
            for field in cursor.description:
                data_dict_buy.append(field[0])

        except:
            print(sql + "_失败")
            print("Error: unable to fetch data")
        i = 0

        for row in flu_list:  # 格式：店名、商品、价格
            i += 1
            self.order_list_table.insert('', 'end', values=row)



if __name__ == '__main__':
    try:
        window = tk.Tk()
        StartPage(window)
    except:
        messagebox.showinfo('错误！', '连接数据库失败！')
