from datetime import datetime, timedelta
import calendar as cal_module
import holidays
from zhdate import ZhDate
from termcolor import colored


def get_datetime_info():
    now = datetime.now()

    # 日期: 2026/03/17
    date_str = colored(now.strftime("🗓️ %Y/%m/%d"), "blue", attrs=["bold"])

    # 星期: (周二)
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_str = colored(f"({weekdays[now.weekday()]})", "green", attrs=["bold"])

    # 时间: 21:54:07
    time_str = colored(now.strftime("🕐 %H:%M:%S"), "white")

    # 农历: 农历正月廿九
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


def main():
    print()

    # 顶部信息行: 🗓️ 2026/03/17 (周二) | 🕐 21:54:07 | 🌙 农历正月廿九
    print(get_datetime_info())
    print()

    # 假期信息
    today_holiday, next_holiday = get_holiday_info()
    if today_holiday:
        print(today_holiday)
    elif next_holiday:
        name, date_str, days = next_holiday
        print(colored(f"🎊 下一假期: {name} ({date_str}) - {days}天后", "magenta", attrs=["bold"]))
    print()

    # 日历部分
    now = datetime.now()
    print(colored(f"📅 {now.year}年{now.month}月", "white", attrs=["bold"]))
    calendar_lines = get_calendar()
    for line in calendar_lines:
        print(f"  {line}")


if __name__ == "__main__":
    main()
