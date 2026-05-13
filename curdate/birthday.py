"""
生日管理模块
提供生日数据的加载、保存、添加、删除、修改和查询功能
"""

import json
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional
from zhdate import ZhDate


# 数据文件路径：用户 home 目录下的 .curdate_birthdays.json
DATA_FILE = Path.home() / ".curdate_birthdays.json"


def load_birthdays() -> List[Dict]:
    """
    加载生日数据

    Returns:
        生日列表
    """
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("birthdays", [])
    except (json.JSONDecodeError, IOError):
        return []


def save_birthdays(birthdays: List[Dict]) -> None:
    """
    保存生日数据

    Args:
        birthdays: 生日列表
    """
    data = {"birthdays": birthdays}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_birthday(name: str, birth_type: str, month: int, day: int) -> bool:
    """
    添加生日

    Args:
        name: 姓名
        birth_type: 生日类型，"lunar" 或 "solar"
        month: 月份
        day: 日期

    Returns:
        成功返回 True，名字已存在返回 False
    """
    birthdays = load_birthdays()

    # 检查名字是否已存在
    for b in birthdays:
        if b["name"] == name:
            return False

    new_birthday = {
        "name": name,
        "type": birth_type,
        "month": month,
        "day": day,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    birthdays.append(new_birthday)
    save_birthdays(birthdays)
    return True


def delete_birthday(name: str) -> bool:
    """
    删除生日

    Args:
        name: 姓名

    Returns:
        找到并删除返回 True
    """
    birthdays = load_birthdays()

    for i, b in enumerate(birthdays):
        if b["name"] == name:
            birthdays.pop(i)
            save_birthdays(birthdays)
            return True

    return False


def update_birthday(name: str, birth_type: str, month: int, day: int) -> bool:
    """
    修改生日

    Args:
        name: 姓名
        birth_type: 生日类型，"lunar" 或 "solar"
        month: 月份
        day: 日期

    Returns:
        成功返回 True，未找到返回 False
    """
    birthdays = load_birthdays()

    for b in birthdays:
        if b["name"] == name:
            b["type"] = birth_type
            b["month"] = month
            b["day"] = day
            save_birthdays(birthdays)
            return True

    return False


def _convert_to_solar(birth_type: str, month: int, day: int, year: int) -> Optional[date]:
    """
    将生日转换为公历日期

    Args:
        birth_type: 生日类型
        month: 月份
        day: 日期
        year: 年份

    Returns:
        公历日期
    """
    try:
        if birth_type == "lunar":
            # 农历转公历
            zh_date = ZhDate(year, month, day)
            solar = zh_date.to_datetime().date()
            return solar
        else:
            # 公历直接使用
            return date(year, month, day)
    except (ValueError, OverflowError):
        # 农历日期无效（如闰月等）
        return None


def _calculate_days_until(birth_type: str, month: int, day: int) -> Dict:
    """
    计算距离生日的天数

    Args:
        birth_type: 生日类型
        month: 月份
        day: 日期

    Returns:
        包含 days_until 和 passed 的字典
    """
    today = date.today()
    current_year = today.year

    # 先尝试今年
    solar_date = _convert_to_solar(birth_type, month, day, current_year)

    if solar_date is None:
        return {"days_until": 9999, "passed": True}

    if solar_date >= today:
        # 今年生日还未过
        days_until = (solar_date - today).days
        passed = False
    else:
        # 今年已过，计算到明年的天数
        next_year = current_year + 1
        solar_date_next = _convert_to_solar(birth_type, month, day, next_year)

        if solar_date_next is None:
            return {"days_until": 9999, "passed": True}

        days_until = (solar_date_next - today).days
        passed = True

    return {"days_until": days_until, "passed": passed, "solar_date": solar_date}


def get_upcoming_birthdays(limit: int = 3, days_limit: int = 30) -> List[Dict]:
    """
    获取即将到来的生日列表

    Args:
        limit: 返回数量限制
        days_limit: 只返回该天数范围内的生日

    Returns:
        即将到来的生日列表
    """
    birthdays = load_birthdays()
    today = date.today()
    current_year = today.year
    upcoming = []

    for b in birthdays:
        month = b["month"]
        day = b["day"]
        birth_type = b["type"]

        result = _calculate_days_until(birth_type, month, day)
        days_until = result.get("days_until", 9999)
        passed = result.get("passed", True)
        solar_date = result.get("solar_date")

        if solar_date:
            solar_date_str = solar_date.strftime("%m月%d日")
        else:
            solar_date_str = "未知"

        upcoming.append({
            "name": b["name"],
            "type": birth_type,
            "month": month,
            "day": day,
            "days_until": days_until,
            "passed": passed,
            "solar_date": solar_date_str
        })

    upcoming.sort(key=lambda x: x["days_until"])

    within_limit = [u for u in upcoming if u["days_until"] <= days_limit]

    if not within_limit and upcoming:
        return [upcoming[0]]

    return within_limit[:limit]


def list_birthdays() -> List[Dict]:
    """
    返回所有生日的列表

    Returns:
        所有生日列表
    """
    return load_birthdays()