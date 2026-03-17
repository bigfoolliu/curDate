# curdate

终端日期时间显示工具 - 显示公历、农历、法定节假日和日历。

## 功能特性

- 📅 显示当前日期和时间
- 🌙 显示农历日期
- 🎊 显示法定节假日和下一假期倒计时
- 📆 显示当月日历

## 安装

```bash
pip install -e .
```

## 使用

```bash
curdate
```

## 演示效果

```text
🗓️ 2026/03/17 (周二) | 🕐 22:07:40 | 🌙 农历正月二十九

🎊 下一假期: 清明节 (04月05日) - 19天后

📅 2026年3月
  日 一 二 三 四 五 六
   1  2  3  4  5  6  7
   8  9 10 11 12 13 14
  15 16 17 18 19 20 21
  22 23 24 25 26 27 28
  29 30 31
```

## 依赖

- [zhdate](https://pypi.org/project/zhdate/) - 农历转换
- [holidays](https://pypi.org/project/holidays/) - 中国法定节假日
- [termcolor](https://pypi.org/project/termcolor/) - 彩色输出
