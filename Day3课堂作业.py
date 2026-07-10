import numpy as np

# 全局存储：学生姓名列表、成绩列表
student_names = []
score_list = []

def input_scores():
    """功能1：录入学生姓名和成绩，numpy保存分数数组"""
    student_names.clear()
    score_list.clear()
    while True:
        try:
            count = int(input("请输入学生人数："))
            if count > 0:
                break
            else:
                print("人数必须大于0！")
        except ValueError:
            print("请输入合法数字！")

    for i in range(count):
        name = input(f"请输入第{i+1}个学生姓名：")
        while True:
            try:
                s = float(input("请输入成绩："))
                if 0 <= s <= 100:
                    break
                else:
                    print("成绩范围必须在0‑100之间！")
            except ValueError:
                print("成绩输入错误，请输入数字！")
        student_names.append(name)
        score_list.append(s)
    # 使用numpy数组存储分数，满足作业要求
    global score_np
    score_np = np.array(score_list)
    print("====学生成绩录入完毕====")


def stat_analyse():
    """功能2：成绩统计分析，借助numpy计算平均值、最大值、最小值、方差"""
    if len(score_np) == 0:
        print("还没有录入学生成绩，请先输入成绩！")
        return
    avg = np.mean(score_np)
    max_s = np.max(score_np)
    min_s = np.min(score_np)
    var_s = np.var(score_np)
    print("=====成绩统计结果=====")
    print(f"平均分：{avg:.2f}")
    print(f"最高分：{max_s}")
    print(f"最低分：{min_s}")
    print(f"成绩方差：{var_s:.2f}")


def show_rank():
    """功能3：查看成绩排名（从高到低）"""
    if len(score_np) == 0:
        print("还没有录入学生成绩！")
        return
    # 得到排序之后的索引
    sorted_index = np.argsort(-score_np)
    print("=====成绩排名（由高到低）=====")
    for rank, idx in enumerate(sorted_index, start=1):
        print(f"第{rank}名：{student_names[idx]}，分数：{score_np[idx]}")


def score_distribute():
    """功能4：成绩等级划分：优秀>=90，良好80‑89，及格60‑79，不及格<60"""
    if len(score_np) == 0:
        print("还没有录入学生成绩！")
        return
    excellent = 0
    good = 0
    pass_ = 0
    fail = 0
    for s in score_np:
        if s >= 90:
            excellent += 1
        elif s >= 80:
            good += 1
        elif s >= 60:
            pass_ += 1
        else:
            fail += 1
    total = len(score_np)
    print("=====成绩分布情况=====")
    print(f"优秀(≥90)：{excellent}人，占比{excellent/total*100:.1f}%")
    print(f"良好(80‑89)：{good}人，占比{good/total*100:.1f}%")
    print(f"及格(60‑79)：{pass_}人，占比{pass_/total*100:.1f}%")
    print(f"不及格(<60)：{fail}人，占比{fail/total*100:.1f}%")


def query_student():
    """功能5：根据学生姓名查询分数"""
    if len(score_np) == 0:
        print("还没有录入学生成绩！")
        return
    find_name = input("请输入要查询的学生姓名：")
    if find_name in student_names:
        pos = student_names.index(find_name)
        s = score_np[pos]
        # 判断等级
        if s >= 90:
            level = "优秀"
        elif s >= 80:
            level = "良好"
        elif s >= 60:
            level = "及格"
        else:
            level = "不及格"
        print(f"学生：{find_name}，分数：{s}，等级：{level}")
    else:
        print("没有找到该学生！")


def main_menu():
    """主菜单循环"""
    while True:
        print("=" * 40)
        print("        成绩分析系统")
        print("=" * 40)
        print("1. 输入成绩数据")
        print("2. 查看成绩统计")
        print("3. 查看成绩排名")
        print("4. 查看成绩分布")
        print("5. 查询学生成绩")
        print("6. 退出系统")
        print("=" * 40)
        choice = input("请选择：")
        if choice == "1":
            input_scores()
        elif choice == "2":
            stat_analyse()
        elif choice == "3":
            show_rank()
        elif choice == "4":
            score_distribute()
        elif choice == "5":
            query_student()
        elif choice == "6":
            print("程序退出！")
            break
        else:
            print("输入选项错误，请输入1‑6之间数字！")
        input("\n按下回车继续回到菜单...")


if __name__ == "__main__":
    score_np = np.array([])
    main_menu()