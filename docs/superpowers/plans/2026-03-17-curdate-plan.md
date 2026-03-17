# curdate 命令行工具实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个 Python 命令行工具 `curdate`，在终端展示当前日期时间、农历、法定节假日和当月日历

**Architecture:** 单一 Python 脚本，使用第三方库处理农历和节假日，输出带颜色的 ASCII 格式

**Tech Stack:** Python, zhdate, holidays, termcolor

---

## 实现方案

### 文件结构

```
curDate/
├── curdate/
│   ├── __init__.py
│   ├── main.py          # 主入口
│   ├── date_formatter.py # 日期格式化
│   ├── lunar.py         # 农历处理
│   ├── holiday.py       # 节假日处理
│   └── calendar.py      # 日历生成
├── tests/
│   └── test_curdate.py
├── pyproject.toml
└── docs/superpowers/specs/2026-03-17-curdate-design.md
```

---

## Chunk 1: 项目初始化与依赖

### Task 1: 创建项目结构

**Files:**
- Create: `curdate/__init__.py`
- Create: `curdate/main.py`
- Create: `pyproject.toml`

- [ ] **Step 1: 创建项目目录结构**

```bash
mkdir -p curdate tests
touch curdate/__init__.py
```

- [ ] **Step 2: 创建 pyproject.toml**

```toml
[project]
name = "curdate"
version = "0.1.0"
description = "终端日期时间显示工具"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "zhdate>=0.1.0",
    "holidays>=0.20",
    "termcolor>=2.0.0",
]

[project.scripts]
curdate = "curdate.main:main"
```

- [ ] **Step 3: 安装依赖**

```bash
pip install -e .
```

- [ ] **Step 4: 提交**

```bash
git add .
git commit -m "chore: 初始化项目结构"
```

---

## Chunk 2: 核心模块实现

### Task 2: 日期时间显示模块

**Files:**
- Modify: `curdate/main.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_date_formatter.py
from curdate.main import format_datetime

def test_format_datetime():
    result = format_datetime()
    assert "年" in result
    assert "月" in result
    assert "日" in result
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_date_formatter.py -v
Expected: FAIL (function not defined)
```

- [ ] **Step 3: 实现日期时间格式化**

```python
# curdate/main.py
from datetime import datetime
from termcolor import colored

def format_datetime():
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日 %H:%M:%S")
    return colored(date_str, "white")
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/test_date_formatter.py -v
Expected: PASS
```

- [ ] **Step 5: 提交**

```bash
git add .
git commit -m "feat: 添加日期时间显示功能"
```

### Task 3: 星期显示模块

**Files:**
- Modify: `curdate/main.py:30-35`

- [ ] **Step 1: 编写测试**

```python
# tests/test_weekday.py
from curdate.main import format_weekday

def test_format_weekday():
    result = format_weekday()
    assert "星期" in result
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_weekday.py -v
Expected: FAIL
```

- [ ] **Step 3: 实现星期格式化**

```python
def format_weekday():
    now = datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = weekdays[now.weekday()]
    return colored(weekday_str, "green")
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/test_weekday.py -v
Expected: PASS
```

- [ ] **Step 5: 提交**

```bash
git add .
git commit -m "feat: 添加星期显示功能"
```

### Task 4: 农历显示模块

**Files:**
- Create: `curdate/lunar.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_lunar.py
from curdate.lunar import format_lunar

def test_format_lunar():
    result = format_lunar()
    assert "农历" in result
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_lunar.py -v
Expected: FAIL
```

- [ ] **Step 3: 实现农历格式化**

```python
# curdate/lunar.py
from zhdate import ZhDate
from termcolor import colored

def format_lunar():
    now = ZhDate.now()
    lunar_str = f"农历{now.chinese()}"
    return colored(lunar_str, "yellow")
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/test_lunar.py -v
Expected: PASS
```

- [ ] **Step 5: 提交**

```bash
git add .
git commit -m "feat: 添加农历显示功能"
```

### Task 5: 节假日显示模块

**Files:**
- Create: `curdate/holiday.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_holiday.py
from curdate.holiday import format_holiday, get_next_holiday

def test_format_holiday():
    result = format_holiday()
    assert isinstance(result, str)

def test_get_next_holiday():
    name, date_str, days = get_next_holiday()
    assert isinstance(name, str)
    assert isinstance(date_str, str)
    assert isinstance(days, int)
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_holiday.py -v
Expected: FAIL
```

- [ ] **Step 3: 实现节假日功能**

```python
# curdate/holiday.py
import holidays
from datetime import datetime, timedelta
from termcolor import colored

def format_holiday():
    cn_holidays = holidays.China(years=datetime.now().year)
    today = datetime.now().date()
    
    if today in cn_holidays:
        name = cn_holidays.get(today)
        return colored(f" 假期: {name}", "red")
    return ""

def get_next_holiday():
    cn_holidays = holidays.China(years=datetime.now().year)
    today = datetime.now().date()
    
    for i in range(1, 365):
        check_date = today + timedelta(days=i)
        if check_date in cn_holidays:
            name = cn_holidays.get(check_date)
            days = i
            date_str = check_date.strftime("%m月%d日")
            return name, date_str, days
    
    return "无", "", 0
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/test_holiday.py -v
Expected: PASS
```

- [ ] **Step 5: 提交**

```bash
git add .
git commit -m "feat: 添加节假日显示功能"
```

### Task 6: 日历显示模块

**Files:**
- Create: `curdate/calendar.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_calendar.py
from curdate.calendar import format_calendar

def test_format_calendar():
    result = format_calendar()
    assert "一月" in result or "二月" in result or "三月" in result or "四月" in result or "五月" in result or "六月" in result or "七月" in result or "八月" in result or "九月" in result or "十月" in result or "十一月" in result or "十二月" in result
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_calendar.py -v
Expected: FAIL
```

- [ ] **Step 3: 实现日历功能**

```python
# curdate/calendar.py
import calendar
from datetime import datetime
from termcolor import colored

def format_calendar():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    month_names = ["一月", "二月", "三月", "四月", "五月", "六月",
                   "七月", "八月", "九月", "十月", "十一月", "十二月"]
    
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)
    
    header = f"     {month_names[month-1]} {year}\n"
    weekdays = colored("日 一 二 三 四 五 六", "cyan")
    
    lines = [header, weekdays, "\n"]
    
    for week in month_days:
        line = ""
        for d in week:
            if d == 0:
                line += "   "
            elif d == day:
                line += colored(f"{d:>2}", "cyan", attrs=["reverse"]) + " "
            else:
                line += f"{d:>2} "
        lines.append(line.rstrip() + "\n")
    
    return "".join(lines)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/test_calendar.py -v
Expected: PASS
```

- [ ] **Step 5: 提交**

```bash
git add .
git commit -m "feat: 添加日历显示功能"
```

---

## Chunk 3: 集成与打包

### Task 7: 集成主程序

**Files:**
- Modify: `curdate/main.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/test_integration.py
from curdate.main import main
from io import StringIO
import sys

def test_main_output():
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        main()
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    
    assert "年" in output
    assert "农历" in output
    assert "星期" in output
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/test_integration.py -v
Expected: FAIL
```

- [ ] **Step 3: 实现主程序**

```python
# curdate/main.py 完整代码
from datetime import datetime
from termcolor import colored
from zhdate import ZhDate
import holidays

def format_datetime():
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日 %H:%M:%S")
    return colored(date_str, "white")

def format_weekday():
    now = datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = weekdays[now.weekday()]
    return colored(weekday_str, "green")

def format_lunar():
    now = ZhDate.now()
    lunar_str = f"农历{now.chinese()}"
    return colored(lunar_str, "yellow")

def format_holiday():
    cn_holidays = holidays.China(years=datetime.now().year)
    today = datetime.now().date()
    
    if today in cn_holidays:
        name = cn_holidays.get(today)
        return colored(f" 假期: {name}", "red")
    return ""

def get_next_holiday():
    cn_holidays = holidays.China(years=datetime.now().year)
    today = datetime.now().date()
    
    for i in range(1, 365):
        check_date = today + timedelta(days=i)
        if check_date in cn_holidays:
            name = cn_holidays.get(check_date)
            days = i
            date_str = check_date.strftime("%m月%d日")
            return name, date_str, days
    
    return "无", "", 0

def format_calendar():
    import calendar as cal_module
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    month_names = ["一月", "二月", "三月", "四月", "五月", "六月",
                   "七月", "八月", "九月", "十月", "十一月", "十二月"]
    
    cal = cal_module.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)
    
    header = f"     {month_names[month-1]} {year}\n"
    weekdays = colored("日 一 二 三 四 五 六", "cyan")
    
    lines = [header, weekdays, "\n"]
    
    for week in month_days:
        line = ""
        for d in week:
            if d == 0:
                line += "   "
            elif d == day:
                line += colored(f"{d:>2}", "cyan", attrs=["reverse"]) + " "
            else:
                line += f"{d:>2} "
        lines.append(line.rstrip() + "\n")
    
    return "".join(lines)

def main():
    from datetime import timedelta
    
    print(colored("╔" + "═" * 40 + "╗", "cyan"))
    print(colored("║", "cyan") + format_datetime().center(40) + colored("║", "cyan"))
    print(colored("║", "cyan") + format_weekday().center(40) + colored("║", "cyan"))
    print(colored("║", "cyan") + format_lunar().center(40) + colored("║", "cyan"))
    
    holiday_info = format_holiday()
    if holiday_info:
        print(colored("║", "cyan") + holiday_info.center(40) + colored("║", "cyan"))
    
    name, date_str, days = get_next_holiday()
    if days > 0:
        next_info = colored(f" ⚐ 下一个假期: {name} ({date_str}) ", "magenta")
        days_info = colored(f"       距离 {days} 天", "magenta")
        print(colored("║", "cyan") + next_info.center(40) + colored("║", "cyan"))
        print(colored("║", "cyan") + days_info.center(40) + colored("║", "cyan"))
    
    print(colored("╚" + "═" * 40 + "╝", "cyan"))
    print()
    print(format_calendar())

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/ -v
Expected: ALL PASS
```

- [ ] **Step 5: 运行程序验证输出**

```bash
curdate
# 或
python -m curdate.main
```

- [ ] **Step 6: 提交**

```bash
git add .
git commit -m "feat: 集成所有模块完成主程序"
```

---

## Chunk 4: 最终验证

### Task 8: 最终测试与清理

- [ ] **Step 1: 运行完整测试**

```bash
pytest tests/ -v
```

- [ ] **Step 2: 测试命令行**

```bash
curdate
```

- [ ] **Step 3: 提交最终版本**

```bash
git add .
git commit -m "feat: 完成 curdate 工具开发"
```
