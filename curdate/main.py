from datetime import datetime, timedelta
import calendar as cal_module
import holidays
import argparse
from zhdate import ZhDate
from termcolor import colored

from curdate.birthday import (
    get_upcoming_birthdays,
    add_birthday,
    delete_birthday,
    update_birthday,
    list_birthdays
)

MONTH_DAYS = {
    1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}


def validate_date(month: int, day: int) -> bool:
    if month < 1 or month > 12:
        return False
    return 1 <= day <= MONTH_DAYS.get(month, 30)


def get_datetime_info():
    now = datetime.now()

    date_str = colored(now.strftime("🗓️ %Y/%m/%d"), "blue", attrs=["bold"])

    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_str = colored(f"({weekdays[now.weekday()]})", "green", attrs=["bold"])

    time_str = colored(now.strftime("🕐 %H:%M:%S"), "white")

    lunar = ZhDate.from_datetime(now)
    chinese_str = lunar.chinese()
    parts = chinese_str.split('年')
    if len(parts) > 1:
        month_day = parts[1].split(' ')[0]
        lunar_str = colored(f"🌙 农历{month_day}", "yellow", attrs=["bold"])
    else:
        lunar_str = colored(f"🌙 农历{parts[0]}", "yellow", attrs=["bold"])

    return f"{date_str} {weekday_str} | {time_str} | {lunar_str}"


def get_holiday_info():
    cn_holidays = holidays.China(years=datetime.now().year)
    today = datetime.now().date()

    if today in cn_holidays:
        return colored(f"🎉 今天是 {cn_holidays.get(today)}", "red", attrs=["bold"]), None

    for i in range(1, 365):
        check_date = today + timedelta(days=i)
        if check_date in cn_holidays:
            name = cn_holidays.get(check_date)
            date_str = check_date.strftime("%m月%d日")
            return None, (name, date_str, i)

    return None, None


def get_birthday_info():
    upcoming = get_upcoming_birthdays(3)
    if not upcoming:
        return None

    lines = [colored("🎂 近期生日:", "cyan", attrs=["bold"])]
    for b in upcoming:
        name = b["name"]
        birth_type = b["type"]
        days_until = b["days_until"]
        passed = b["passed"]

        if birth_type == "lunar":
            type_str = f"农历{b['month']}月{b['day']}日"
            icon = "🧑"
        else:
            type_str = f"公历{b['month']}月{b['day']}日"
            icon = "👩" if "女" in name or "女" in name else "👨"
            if icon == "👩" and not any(c in name for c in ["女", "妈", "婆", "姨", "姑", "姐", "妹"]):
                icon = "🧑"

        if passed:
            days_str = colored("已过（去年）", "red")
        else:
            days_str = colored(f"还有 {days_until}天", "green")

        lines.append(f"   {icon} {name} - {type_str} - {days_str}")

    return "\n".join(lines)


def get_calendar():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    month_names = ["一月", "二月", "三月", "四月", "五月", "六月",
                   "七月", "八月", "九月", "十月", "十一月", "十二月"]

    cal = cal_module.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    lines = []
    lines.append(colored("日 一 二 三 四 五 六", "white"))

    for week in month_days:
        line_parts = []
        for d in week:
            if d == 0:
                line_parts.append("  ")
            elif d == day:
                line_parts.append(colored(f"{d:>2}", "cyan", attrs=["reverse", "bold"]))
            else:
                line_parts.append(f"{d:>2}")
        lines.append(" ".join(line_parts))

    return lines


def interactive_add():
    name = input("请输入姓名: ").strip()
    if not name:
        print(colored("✗ 姓名不能为空", "red"))
        return

    print("选择日期类型: (1) 公历 (2) 农历")
    choice = input("请输入选项: ").strip()

    birth_type = "solar" if choice == "1" else "lunar"

    try:
        month = int(input("输入月份 (1-12): ").strip())
        max_day = MONTH_DAYS.get(month, 30)
        day = int(input(f"输入日期 (1-{max_day}): ").strip())
    except ValueError:
        print(colored("✗ 请输入有效的数字", "red"))
        return

    if not validate_date(month, day):
        print(colored("✗ 日期无效", "red"))
        return

    type_label = "公历" if birth_type == "solar" else "农历"
    if add_birthday(name, birth_type, month, day):
        print(colored(f"✓ 已添加 {name} 的生日（{type_label} {month}月{day}日）", "green"))
    else:
        print(colored(f"✗ {name} 的生日已存在", "red"))


def interactive_delete(name: str):
    if not name:
        print(colored("✗ 姓名不能为空", "red"))
        return

    if delete_birthday(name):
        print(colored(f"✓ 已删除 {name} 的生日", "green"))
    else:
        print(colored(f"✗ 未找到 {name} 的生日", "red"))


def interactive_edit(name: str):
    if not name:
        print(colored("✗ 姓名不能为空", "red"))
        return

    birthdays = list_birthdays()
    found = None
    for b in birthdays:
        if b["name"] == name:
            found = b
            break

    if not found:
        print(colored(f"✗ 未找到 {name} 的生日", "red"))
        return

    print(f"当前: {name} - {'农历' if found['type'] == 'lunar' else '公历'} {found['month']}月{found['day']}日")
    print("选择日期类型: (1) 公历 (2) 农历")
    choice = input("请输入选项: ").strip()

    birth_type = "solar" if choice == "1" else "lunar"

    try:
        month = int(input("输入月份 (1-12): ").strip())
        max_day = MONTH_DAYS.get(month, 30)
        day = int(input(f"输入日期 (1-{max_day}): ").strip())
    except ValueError:
        print(colored("✗ 请输入有效的数字", "red"))
        return

    if not validate_date(month, day):
        print(colored("✗ 日期无效", "red"))
        return

    type_label = "公历" if birth_type == "solar" else "农历"
    if update_birthday(name, birth_type, month, day):
        print(colored(f"✓ 已更新 {name} 的生日（{type_label} {month}月{day}日）", "green"))
    else:
        print(colored("✗ 更新失败", "red"))


def show_birthday_list():
    birthdays = list_birthdays()
    if not birthdays:
        print(colored("暂无存储的生日", "yellow"))
        return

    print(colored("🎂 已存储的生日:", "cyan", attrs=["bold"]))
    for b in birthdays:
        name = b["name"]
        birth_type = b["type"]
        month = b["month"]
        day = b["day"]

        if birth_type == "lunar":
            type_str = f"农历 {month}月{day}日"
            icon = "🧑"
        else:
            type_str = f"公历 {month}月{day}日"
            icon = "👩" if any(c in name for c in ["女", "妈", "婆", "姨", "姑", "姐", "妹"]) else "👨"
            if icon == "👩" and not any(c in name for c in ["女", "妈", "婆", "姨", "姑", "姐", "妹"]):
                icon = "🧑"

        print(f"   {icon} {name} - {type_str}")


def main():
    parser = argparse.ArgumentParser(prog="curdate", description="日期和生日管理工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    subparsers.add_parser("add", help="添加生日")
    subparsers.add_parser("list", help="列出所有生日")

    delete_parser = subparsers.add_parser("delete", help="删除生日")
    delete_parser.add_argument("name", help="姓名")

    edit_parser = subparsers.add_parser("edit", help="修改生日")
    edit_parser.add_argument("name", help="姓名")

    args = parser.parse_args()

    if args.command == "add":
        interactive_add()
        return

    if args.command == "delete":
        interactive_delete(args.name)
        return

    if args.command == "edit":
        interactive_edit(args.name)
        return

    if args.command == "list":
        show_birthday_list()
        return

    print()

    print(get_datetime_info())
    print()

    today_holiday, next_holiday = get_holiday_info()
    if today_holiday:
        print(today_holiday)
    elif next_holiday:
        name, date_str, days = next_holiday
        print(colored(f"🎊 下一假期: {name} ({date_str}) - {days}天后", "magenta", attrs=["bold"]))
    print()

    birthday_info = get_birthday_info()
    if birthday_info:
        print(birthday_info)
        print()

    now = datetime.now()
    print(colored(f"📅 {now.year}年{now.month}月", "white", attrs=["bold"]))
    calendar_lines = get_calendar()
    for line in calendar_lines:
        print(f"  {line}")


if __name__ == "__main__":
    main()