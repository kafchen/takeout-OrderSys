# 8.0.25 MySQL Community Server、Python 3.8、

import random
import pymysql
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *

order_list = set()  # 当前购买的
cur_menu = []  # 当前的菜单
user_id = ''  # 登录的用户ID
user_pwd = ''  # 登录用户的密码
rest_money = 0  # 用户的余额

''' ==============================================================================================
以下是关于 数据库 的操作
=============================================================================================='''
# 连接数据库
db = pymysql.connect(host ='localhost', port=3306, db='restaurant', user='root', password='5286')
# 使用cursor()方法获取操作游标
cursor = db.cursor()


def select(table, par=""):
    # SQL 查询语句
    data_dict = []
    results = []
    sql = "SELECT * FROM %s %s;" % \
          (table, par)
    try:###
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

    return data_dict, results


def Insert(table, par):
    sql = "INSERT INTO %s VALUES %s;" % \
          (table, par)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        db.commit()
        print(sql + "成功")
    except:
        db.rollback()
        print(sql + "_失败")
        print("Error: file to insert")


''' ==============================================================================================
以下是关于 主界面 的操作
=============================================================================================='''


def flush_info():
    """从数据库查询最新消息并显示在控件上"""
    flush_dict, flush_in = select("customer", 'WHERE Cno=' + user_id)
    if len(flush_in) == 0:
        tk.messagebox.showerror(message='未从数据库获得消息，请检查')
    print("从数据库查询到", end="")
    print(flush_in)
    # 刷新用户名
    total_username_show.set(flush_in[0][2])
    # 刷新余额
    global rest_money
    rest_money = flush_in[0][6]
    total_wallet_show.set(rest_money)

    # 刷新订单到控件上
    # 先清除旧的信息
    x = order_list_table.get_children()
    for item in x:
        order_list_table.delete(item)

    data_dict_buy, flu_list = select("view_Cus_look",'WHERE Cno = '+user_id)  # 从数据库获取信息
    i = 0
    for row in flu_list:  # 格式：店名、商品、价格
        i += 1
        order_list_table.insert('', 'end', values=row)


def submit_order():
    total_cost = 0  # 该订单总金额
    if len(order_list) == 0:
        tk.messagebox.showerror(message='空订单')
        return 0
    for i in order_list:
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
    print(order_list)
    '''提交订单到数据库
    先要知道订单分为几组（从几个店买的）
    然后分别把每个组插入一个集合
    
    循环，对于每个集合
    新建一个订单（插入订单表一次）
    新建n条记录（n为订单内的元素个数 即集合内的元素个数）
    '''
    goods_name_to_id = {}  # 获得姓名和ID的对应关系
    aa, name_to_id = select('goods')
    for row in name_to_id:
        goods_name_to_id[row[2]] = row[0]

    gname_to_sno = {}  # 获得姓名和商店名的对应关系
    aa, name_to_sno = select('goods')
    for row in name_to_sno:
        gname_to_sno[row[2]] = row[1]

    free_deliver_tomane = {}  # 获得空闲的配送员与姓名的对照表
    free_deliver = []  # 获得空闲的配送员
    aa, free_deliver_list = select('deliverer', 'WHERE Dstate = \'工作\'')
    for row in free_deliver_list:
        free_deliver.append(row[0])
        free_deliver_tomane[row[0]] = row[2]




    # 获得订单号
    sql_o_num = 'SELECT Ono FROM orderr;'
    cursor.execute(sql_o_num)
    o_num_resu = cursor.fetchall()
    print(o_num_resu)
    tt = 0
    for i in o_num_resu:
        if int(i[0]) > tt:
            tt = int(i[0])
    o_num = tt
    print("最大订单号" + str(o_num))

    commit_table_include = set()
    commit_table_o_num = {}
    for i in order_list:
        if cur_menu[i][0] not in commit_table_include:
            commit_table_include.add(cur_menu[i][0])
            o_num += 1
            commit_table_o_num[cur_menu[i][0]] = str(o_num)
            # 新建一个订单
            # 从空闲配送员随机选取一个

            del_num = random.choice(free_deliver)
            print("本次随机分配的配送员"+del_num)
            sql_commit_order = '(\'{}\',{},\'{}\',{},\'{}\',\'{}\',\'{}\',\'{}\',{})' \
                .format(str(o_num),del_num, user_id, gname_to_sno[cur_menu[i][1]], '正在出餐', '无', '1', 1, 'NOW()')
            Insert('orderr', sql_commit_order)

        # 只插入商品
        sql_commit_order = '(\'{}\',{},\'{}\')' \
            .format(commit_table_o_num[cur_menu[i][0]], goods_name_to_id[cur_menu[i][1]], 1)
        Insert('purchase', sql_commit_order)

    print(commit_table_include)

    # 先获得一个单号sql_commit_order

    # sql_commit_order = '(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})'.format(o_num,'',user_id, n_sex,1, n_tel, 1,8,8)

    # 先插入订单表
    # Insert(orderr, sql_commit_order)

    # 再插入详情表

    '''提交结束'''

    # 更新控件上显示的数字
    flush_info()

    # 已选列表清空
    order_list.clear()
    total_cost_show.set(len(order_list))
    tk.messagebox.showinfo(title="通知", message="提交成功！")

    # 这里最好能够刷新一下菜单

    '''需要的操作：
    判断余额是否足够，够的话减去相应的金额，
    插入订单表
    修改 左下角已选 为0 ，刷新菜单。
    更新主界面
    '''



def alter_info():  # 修改个人信息

    def commit_info_change():
        identify_pwd = alter_pwd_old.get()
        global user_pwd
        if user_pwd != identify_pwd:
            tk.messagebox.showerror('错误', '密码错误')
            return

        # 从控件获取用户的输入
        altered_id = alter_new_id.get()
        altered_addr = alter_new_addr.get()
        altered_sex = alter_new_sex.get()
        altered_tel = alter_new_tel.get()
        altered_pwd = alter_new_pwd_confirm.get()
        altered_name = alter_new_name.get()

        # 将新信息提交到数据库
        changed = 0
        sql_alt = 'UPDATE customer SET '
        if altered_pwd != "":
            sql_alt += " Cpass=\'" + altered_pwd + "\'"
            changed = 1
        if altered_addr != "":
            if changed == 1:
                sql_alt += ','
            sql_alt += " Caddress=\'" + altered_addr + "\'"
            changed = 1
        if altered_tel != "":
            if changed == 1:
                sql_alt += ','
            sql_alt += " Ctel=\'" + altered_tel + "\'"
            changed = 1
        if altered_sex != "":
            if changed == 1:
                sql_alt += ','
            sql_alt += " Csex=\'" + altered_sex + "\'"
            changed = 1
        if altered_name != "":
            if changed == 1:
                sql_alt += ','
            sql_alt += " Cname=\'" + altered_name + "\'"
        sql_alt += "WHERE Cno=\'" + user_id + "\';"
        try:  # 执行SQL语句
            cursor.execute(sql_alt)
            db.commit()
            user_pwd = identify_pwd  # 修改本地缓存的密码
            tk.messagebox.showinfo(title="通知", message="修改成功！")
        except:
            db.rollback()
            print(sql_alt + "_失败")
        window_alter_info.withdraw()

    # 从数据库查询个人信息
    alter_info_dict, alter_pre_info = select("customer", 'WHERE Cno=' + user_id)
    info = alter_pre_info[0]
    print(alter_pre_info)

    # 新建修改信息界面
    window_alter_info = tk.Toplevel(main_window)
    window_alter_info.geometry('450x350')
    window_alter_info.title('查询/修改信息')
    # 用户名变量及标签、输入框
    alter_new_id = tk.StringVar()
    tk.Label(window_alter_info, text='ID：').place(x=10, y=10)
    tk.Label(window_alter_info, text=info[0] + ' ' * 30 + '不可更改').place(x=110, y=10)
    # tk.Entry(window_alter_info, textvariable=alter_new_id).place(x=250, y=10)
    # 密码变量及标签、输入框
    alter_pwd_old = tk.StringVar()
    tk.Label(window_alter_info, text='老密码：').place(x=10, y=50)
    tk.Label(window_alter_info, text='***').place(x=110, y=50)
    tk.Entry(window_alter_info, textvariable=alter_pwd_old, show='*').place(x=250, y=50)
    # 重复密码变量及标签、输入框
    alter_new_pwd_confirm = tk.StringVar()
    tk.Label(window_alter_info, text='新密码：').place(x=10, y=90)
    tk.Label(window_alter_info, text='***').place(x=110, y=90)
    tk.Entry(window_alter_info, textvariable=alter_new_pwd_confirm, show='*').place(x=250, y=90)
    # 姓名
    alter_new_name = tk.StringVar()
    tk.Label(window_alter_info, text='姓名').place(x=10, y=130)
    tk.Label(window_alter_info, text=info[2]).place(x=110, y=130)
    tk.Entry(window_alter_info, textvariable=alter_new_name).place(x=250, y=130)
    # 性别
    alter_new_sex = tk.StringVar()
    tk.Label(window_alter_info, text='性别(M/F)').place(x=10, y=170)
    tk.Label(window_alter_info, text=info[3]).place(x=110, y=170)
    tk.Entry(window_alter_info, textvariable=alter_new_sex).place(x=250, y=170)
    # 电话
    alter_new_tel = tk.StringVar()
    tk.Label(window_alter_info, text='电话').place(x=10, y=210)
    tk.Label(window_alter_info, text=info[5]).place(x=110, y=210)
    tk.Entry(window_alter_info, textvariable=alter_new_tel).place(x=250, y=210)
    # 住址
    alter_new_addr = tk.StringVar()
    tk.Label(window_alter_info, text='地址').place(x=10, y=250)
    tk.Label(window_alter_info, text=info[4]).place(x=110, y=250)
    tk.Entry(window_alter_info, textvariable=alter_new_addr).place(x=250, y=250)

    # 确认注册按钮及位置
    tk.Button(window_alter_info, text='确认修改', command=commit_info_change).place(x=250, y=310)
    # tk.Button(window_alter_info, text='退出', command=signtowcg).place(x=50, y=310)


def charge_money():
    def charge_money_in():
        if charge_amount.get() == "" or int(charge_amount.get()) <= 0:
            tk.messagebox.showerror('错误', '金额有误')

        target_money = int(charge_amount.get()) + rest_money
        identify_pwd = charge_pwd.get()
        if user_pwd != identify_pwd:
            tk.messagebox.showerror('错误', '密码错误')
            return
        # 修改数据库余额
        cursor.callproc('alter_cus_money', args=(user_id, target_money))
        db.commit()
        flush_info()
        tk.messagebox.showinfo(title="通知", message="充值成功！")
        window_charge_money.withdraw()

    # 首先需要读取用户的 充值金额 验证密码
    # 新建充值界面
    window_charge_money = tk.Toplevel(main_window)
    window_charge_money.geometry('350x200')
    window_charge_money.title('充值')
    # 充值金额
    charge_amount = tk.StringVar()
    tk.Label(window_charge_money, text='金额：').place(x=10, y=10)
    tk.Entry(window_charge_money, textvariable=charge_amount).place(x=100, y=10)
    # 密码变量及标签、输入框
    charge_pwd = tk.StringVar()
    tk.Label(window_charge_money, text='密码：').place(x=10, y=50)
    tk.Entry(window_charge_money, textvariable=charge_pwd, show='*').place(x=100, y=50)
    # 确认注册按钮及位置
    tk.Button(window_charge_money, text='确认充值', command=charge_money_in).place(x=180, y=80)


# 窗口
main_window = tk.Tk()
main_window.title('外卖管理_主界面 1.0 ')
main_window.geometry('800x520')
main_window.withdraw()  # 实现主窗口隐藏

left_index = 640  # 保证控件左边对齐
# 标签 用户名密码
tk.Label(main_window, text='用户名:').place(x=left_index, y=15)
tk.Label(main_window, text='余  额:').place(x=left_index, y=55)
tk.Label(main_window, text='已选:').place(x=40, y=480)
tk.Label(main_window, text='最近购买的订单：').place(x=440, y=180)
total_cost_show = tk.StringVar()  # 用于展示已选商品数量
tk.Label(main_window, textvariable=total_cost_show).place(x=70, y=480)
total_cost_show.set("当前为0")

total_wallet_show = tk.StringVar()  # 用于展示余额
tk.Label(main_window, textvariable=total_wallet_show).place(x=left_index + 40, y=55)

total_username_show = tk.StringVar()  # 用于展示用户名
tk.Label(main_window, textvariable=total_username_show).place(x=left_index + 40, y=15)

bt_charge = tk.Button(main_window, text='充值余额', height=1, width=16, command=charge_money)
bt_charge.place(x=left_index - 140, y=50)
bt_user_info = tk.Button(main_window, text='查询修改个人信息', height=1, width=16, command=alter_info)
bt_user_info.place(x=left_index - 140, y=10)
bt_submit = tk.Button(main_window, text='提交订单', height=1, width=10, command=submit_order)
bt_submit.place(x=250, y=480)
bt_flush_order = tk.Button(main_window, text='刷  新', height=1, width=10, command=flush_info)
bt_flush_order.place(x=700, y=120)

# def creat_order_list():  # 显示订单的控件 显示最近几个
columns = ['订单号', '商家名', '金额', '状态', '日期']
width_ord = [45, 70, 50, 70, 110]
order_list_table = Treeview(
    master=main_window,  # 父容器
    height=10,  # 表格显示的行数,height行
    columns=columns,  # 显示的列
    show='headings',  # 隐藏首列
)
t = 0
order_list_table.place(x=440, y=200)
for i in columns:
    order_list_table.heading(i, text=i)  # 定义表头
for i in columns:
    order_list_table.column(i, width=width_ord[t], minwidth=40, anchor=S, )  # 定义列
    t += 1


class My_Tk():
    def __init__(self):
        self.main_window = main_window
        # self.main_window.geometry('800x500')
        self.orm = {}
        self.create_button()
        self.create_heading()
        self.create_tv()
        self.insert_tv()  # 进入时 刷新一次

    def create_button(self):
        Button(self.main_window, text='刷新菜单', command=self.insert_tv).pack()

    def create_heading(self, ):
        '''重新做一个treeview的头，不然滚动滚动条，看不标题'''
        heading_frame = Frame(self.main_window)
        heading_frame.place(x=15, y=30)

        # 填充用
        button_frame = Label(heading_frame, width=0.5)
        button_frame.place(x=10, y=60)
        # 全选按钮
        self.all_buttonvar = IntVar()
        self.all_button = Checkbutton(heading_frame, text='', variable=self.all_buttonvar, command=self.select_all)
        self.all_button.pack(side=LEFT)
        self.all_buttonvar.set(0)

        self.columns = ['店铺', '商品', '价格']
        self.widths = [100, 100, 100]

        # 重建tree的头
        for i in range(len(self.columns)):
            Label(heading_frame, text=self.columns[i], width=int(self.widths[i] * 0.16), anchor='center',
                  relief=GROOVE).pack(side=LEFT)

    def create_tv(self):
        # 放置 canvas、滚动条的frame
        canvas_frame = Frame(self.main_window, width=400, height=400)
        canvas_frame.place(x=10, y=60)

        # 只剩Canvas可以放置treeview和按钮，并且跟滚动条配合
        self.canvas = Canvas(canvas_frame, width=400, height=400, scrollregion=(0, 0, 400, 400))
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
        self.tv_frame = self.canvas.create_window(0, 0, window=tv_frame, anchor='nw', width=400,
                                                  height=400)  # anchor该窗口在左上方

        # 放置button的frame
        self.button_frame = Frame(tv_frame)
        self.button_frame.pack(side=LEFT, fill=Y)
        Label(self.button_frame, width=3).pack()  # 填充用

        # 创建treeview
        self.tv = Treeview(tv_frame, height=10, columns=self.columns, show='headings')  # height好像设定不了行数，实际由插入的行数决定
        self.tv.pack(expand=1, side=LEFT, fill=BOTH)
        # self.tv.place()
        # 设定每一列的属性
        for i in range(len(self.columns)):
            self.tv.column(self.columns[i], widt=1, minwidth=self.widths[i], anchor='center', stretch=True)

        # 设定treeview格式
        self.tv.tag_configure('oddrow', font='Arial 12')  # 设定treeview里字体格式font=ft
        self.tv.tag_configure('select', background='SkyBlue', font='Arial 12')  # 当对应的按钮被打勾，那么对于的行背景颜色改变
        self.rowheight = 27  # tkinter里只能用整数
        Style().configure('Treeview', rowheight=self.rowheight)  # 设定每一行的高度

        # 设定选中的每一行字体颜色、背景颜色 (被选中时，没有变化)
        Style().map("Treeview",
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

        global cur_menu  # 使用全局的菜单变量
        data_dict_in, cur_menu = select("view_Cus_buy")
        i = 0
        for row in cur_menu:  # 格式：店名、商品、价格
            i += 1
            tv_item = self.tv.insert('', i, value=row, tags=('oddrow'))  # item默认状态tags

            ck_button = tkinter.Checkbutton(self.button_frame, variable=IntVar())
            ck_button['command'] = lambda item=tv_item: self.select_button(item)
            ck_button.pack()
            self.orm[tv_item] = [ck_button]

        # 每次点击插入tree，先设定全选按钮不打勾，接着打勾并且调用其函数
        self.all_buttonvar.set(1)
        self.all_button.invoke()
        order_list.clear()

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
                order_list.add(a)
                # print("___全选")
            else:
                button.deselect()
                self.tv.item(item, tags='oddrow')
                if len(order_list) != 0:
                    order_list.remove(a)
                # print("___全不选")
        total_cost_show.set(len(order_list))
        # print(order_list)

    def select_button(self, item):
        print("单 选 ", end="")
        print(item)
        a = eval("0x" + str(item[1:]))
        print(a)
        a = a % len(cur_menu)
        if a in order_list:
            order_list.remove(a)
        else:
            order_list.add(a)
        print(order_list)
        total_cost_show.set(len(order_list))
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


My_Tk()
''' ==============================================================================================
以下是关于 登录界面 的操作
=============================================================================================='''

# 窗口
# loggin_window = tk.Tk()
loggin_window = tk.Toplevel(main_window)

loggin_window.title('外卖管理_用户登录界面 1.0 ')
loggin_window.geometry('350x500')
# 画布放置图片
canvas = tk.Canvas(loggin_window, height=250, width=250)
imagefile = tk.PhotoImage(file='qm.png')
image = canvas.create_image(0, 0, anchor='nw', image=imagefile)
# canvas.pack(side='top')
canvas.place(x=50, y=25)
# 标签 用户名密码
tk.Label(loggin_window, text='用户ID:').place(x=60, y=310)
tk.Label(loggin_window, text='密  码:').place(x=60, y=350)

# 用户名输入框
var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(loggin_window, textvariable=var_usr_name)
entry_usr_name.place(x=130, y=310)
# 密码输入框
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(loggin_window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=130, y=350)


# 退出的函数
def usr_sign_quit():
    loggin_window.destroy()
    exit()


def usr_log_in():
    # 输入框获取用户名密码
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    usrs_info = {}
    other_user = []
    # 从数据库获取用户信息
    data_dict, resu = select("password")
    for row in resu:  # 格式：账号、密码、类型
        if row[2] == "用户":  # 只加载类型为用户的账号密码
            usrs_info[row[0]] = row[1]
        else:
            other_user.append(row[0])

    # 判断用户名和密码是否匹配
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='welcome',
                                   message='欢迎您：' + usr_name)
            global user_id  # 保存全局信息
            global user_pwd
            user_id = usr_name
            user_pwd = usr_pwd
            loggin_window.destroy()
            main_window.deiconify()
            flush_info()

            # main_window.iconify() # 这种方法不直接在前台展示
        else:
            tk.messagebox.showerror(message='密码错误')
    # 用户名密码不能为空
    elif usr_name == '' or usr_pwd == '':
        tk.messagebox.showerror(message='用户名或密码为空')
    elif usr_name in other_user:
        tk.messagebox.showerror(message='账户类型出错，请切换其它系统')
    # 不在数据库中弹出是否注册的框
    else:
        is_signup = tk.messagebox.askyesno('欢迎', '您还没有注册，是否现在注册')
        if is_signup:
            usr_sign_up()


def usr_sign_up():
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        n_id = new_id.get()
        n_pwd = new_pwd.get()
        n_pwd_c = new_pwd_confirm.get()
        n_name = new_name.get()
        n_sex = new_sex.get()
        n_tel = new_tel.get()
        n_addr = new_addr.get()

        if '' in [n_id, n_pwd, n_pwd_c, n_name, n_sex, n_tel, n_addr]:
            tk.messagebox.showerror('错误', '有内容为空')
            return

            # 本地加载已有用户信息,如果没有则已有用户信息为空

        # 从数据库获取用户信息
        exist_usr_info = []
        user_dict, resu = select("password")
        for row in resu:  # 格式：账号、密码、类型
            exist_usr_info.append(row[0])

            # 检查用户名存在、密码为空、密码前后不一致
        if n_id in exist_usr_info:
            tk.messagebox.showerror('错误', '用户名已存在')
        elif n_pwd == '' or n_id == '':
            tk.messagebox.showerror('错误', '用户名或密码为空')
        elif n_pwd != n_pwd_c:
            tk.messagebox.showerror('错误', '密码前后不一致')
        # 注册信息没有问题则将用户名密码写入数据库
        else:
            # 在这里插入数据库一条新的信息
            # ins = '(\'' + n_id + '\',\'' + n_pwd + '\',' + '\'用户\'' + ')'
            ins = '(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})'.format(n_id, n_pwd, n_name, n_sex, n_addr, n_tel, 1)

            Insert('Customer', ins)
            tk.messagebox.showinfo('欢迎', '注册成功')
            # 注册成功关闭注册框
            window_sign_up.destroy()

    # 新建注册界面
    window_sign_up = tk.Toplevel(loggin_window)
    window_sign_up.geometry('350x350')
    window_sign_up.title('注册')
    # 用户名变量及标签、输入框
    new_id = tk.StringVar()
    tk.Label(window_sign_up, text='ID：').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=new_id).place(x=150, y=10)
    # 密码变量及标签、输入框
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='密码：').place(x=10, y=50)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='确认密码：').place(x=10, y=90)
    tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)
    # 姓名
    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='姓名').place(x=10, y=130)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=130)
    # 性别
    new_sex = tk.StringVar()
    tk.Label(window_sign_up, text='性别(M/F)').place(x=10, y=170)
    tk.Entry(window_sign_up, textvariable=new_sex).place(x=150, y=170)
    # 电话
    new_tel = tk.StringVar()
    tk.Label(window_sign_up, text='电话').place(x=10, y=210)
    tk.Entry(window_sign_up, textvariable=new_tel).place(x=150, y=210)
    # 住址
    new_addr = tk.StringVar()
    tk.Label(window_sign_up, text='地址').place(x=10, y=250)
    tk.Entry(window_sign_up, textvariable=new_addr).place(x=150, y=250)

    # 确认注册按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='确认注册',
                                   command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=310)


# 登录 注册 退出三个按钮
bt_login = tk.Button(loggin_window, text='登录', command=usr_log_in)
bt_login.place(x=80, y=400)
bt_logup = tk.Button(loggin_window, text='注册', command=usr_sign_up)
bt_logup.place(x=150, y=400)
bt_logquit = tk.Button(loggin_window, text='退出', command=usr_sign_quit)
bt_logquit.place(x=220, y=400)

''' ==============================================================================================
以下是关于 main 的操作
=============================================================================================='''

if __name__ == '__main__':
    print('This is main in' + __name__)
    # main_window.deiconify()
    main_window.mainloop()

    print("用户成功登录进入系统")

    # 关闭数据库连接
    db.close()

''' ==============================================================================================


=============================================================================================='''