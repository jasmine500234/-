# 1.学生成绩管理系统
student_list = []

while True:
    print("=====学生成绩管理系统=====")
    print("1.录入学生成绩")
    print("2.查询学生成绩")
    print("3.统计全班成绩")
    print("0.退出系统")
    choice = input("请输入您的选择：")

    if choice == "1":
        name = input("请输入学生姓名：")
        id_num = input("请输入学号：")
        chinese = float(input("请输入语文成绩："))
        math = float(input("请输入数学成绩："))
        english = float(input("请输入英语成绩："))
        student = {
            "姓名": name,
            "学号": id_num,
            "语文": chinese,
            "数学": math,
            "英语": english
        }
        student_list.append(student)
        print("录入成功！\n")

    elif choice == "2":
        search_name = input("请输入要查询的学生姓名：")
        find = False
        for s in student_list:
            if s["姓名"] == search_name:
                print("-----学生信息-----")
                print(f"姓名：{s['姓名']} 学号：{s['学号']}")
                print(f"语文：{s['语文']} 数学：{s['数学']} 英语：{s['英语']}")
                total = s["语文"] + s["数学"] + s["英语"]
                avg = total / 3
                print(f"总分：{total} 平均分：{avg:.2f}\n")
                find = True
        if not find:
            print("没有找到该学生！\n")

    elif choice == "3":
        if len(student_list) == 0:
            print("还没有学生数据！\n")
        else:
            all_score = []
            for s in student_list:
                total = s["语文"] + s["数学"] + s["英语"]
                all_score.append(total)
            avg_class = sum(all_score)/len(all_score)
            max_score = max(all_score)
            min_score = min(all_score)
            print(f"全班总分平均分：{avg_class:.2f}")
            print(f"全班最高总分：{max_score}")
            print(f"全班最低总分：{min_score}\n")

    elif choice == "0":
        print("系统退出！")
        break
    else:
        print("输入错误，请重新选择！\n")


# 2.数学计算器
import math

# 1：加法
def add(a, b):
    return a + b

# 2：减法
def sub(a, b):
    return a - b

# 3：乘法
def mul(a, b):
    return a * b

# 4：除法（带判断除0）
def div(a, b):
    if b == 0:
        return "错误：除数不能为0"
    return a / b

# 5：幂运算
def power(a, b):
    return a ** b

# 6：开平方
def sqrt_num(a):
    if a < 0:
        return "错误：负数不能开平方"
    return math.sqrt(a)

# 7：保存记录到文件
def save_record(text):
    with open("calc_history.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

# 8：读取历史记录
def read_history():
    try:
        with open("calc_history.txt", "r", encoding="utf-8") as f:
            content = f.read()
        print("====历史记录====")
        print(content)
    except FileNotFoundError:
        print("暂无历史记录文件！")


# 主程序
while True:
    print("\n====简易计算器====")
    print("1.加法  2.减法  3.乘法  4.除法")
    print("5.幂运算  6.开平方  7.查看历史记录  0.退出")
    op = input("请选择功能：")

    if op == "0":
        print("计算器退出")
        break

    try:
        if op in ["1", "2", "3", "4", "5"]:
            num1 = float(input("请输入第一个数字："))
            num2 = float(input("请输入第二个数字："))
            res = 0
            formula = ""
            if op == "1":
                res = add(num1, num2)
                formula = f"{num1} + {num2} = {res}"
            elif op == "2":
                res = sub(num1, num2)
                formula = f"{num1} - {num2} = {res}"
            elif op == "3":
                res = mul(num1, num2)
                formula = f"{num1} * {num2} = {res}"
            elif op == "4":
                res = div(num1, num2)
                formula = f"{num1} / {num2} = {res}"
            elif op == "5":
                res = power(num1, num2)
                formula = f"{num1} ** {num2} = {res}"
            print("计算结果：", res)
            save_record(formula)

        elif op == "6":
            num = float(input("请输入数字："))
            res = sqrt_num(num)
            formula = f"sqrt({num}) = {res}"
            print("计算结果：", res)
            save_record(formula)

        elif op == "7":
            read_history()

        else:
            print("无效选项！")

    except ValueError:
        print("输入错误！请输入数字！")