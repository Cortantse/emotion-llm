import datetime

def print_error(fn, err):
    # 定义颜色 ANSI 转义序列
    red = "\033[31m"   # 红色字体
    bold = "\033[1m"   # 加粗
    reset = "\033[0m"  # 重置样式

    # 获取函数名
    fn_name = getattr(fn, '__qualname__', 'unknown function')

    # 获取当前时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构造错误信息
    msg = f"{bold}{red}[{current_time}] 不可恢复的错误发生在 {fn_name}: {err}{reset}\n"

    # 输出并记录日志
    print(msg)
    with open('error.log', 'a') as f:
        f.write(f"{current_time}: 不可恢复的错误发生在 {fn_name}: {err}\n")
        
    # 抛出异常，阻止程序继续执行
    raise ValueError(msg)

def print_warning(fn, err, warning_level="请填入强度，可选择 低风险/中风险/高风险"):
    # 定义颜色 ANSI 转义序列
    yellow = "\033[33m"  # 黄色字体
    bold = "\033[1m"     # 加粗
    reset = "\033[0m"    # 重置样式

    # 防止默认值
    if warning_level == "请填入强度，可选择 低风险/中风险/高风险":
        warning_level = "未知风险"
        print_warning(print_warning, "未填入风险强度", "低风险")

    # 获取函数名
    fn_name = getattr(fn, '__qualname__', 'unknown function')

    # 获取当前时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构造警告信息
    msg = f"{bold}{yellow}[{current_time}] {warning_level}的警告发生在 {fn_name}: {err}{reset}\n"

    # 输出警告信息
    print(msg)
    with open('error.log', 'a') as f:
        f.write(f"{current_time}: {warning_level}的警告发生在 {fn_name}: {err}\n")


if __name__ == "__main__":

    def test():
        try:
            1/0
        except Exception as e:
            print_error(test, e)
        try:
            1/0
        except Exception as e:
            print_warning(test, e, "低风险")
        try:
            1/0
        except Exception as e:
            print_warning(test, e, "中风险")
        try:
            1/0
        except Exception as e:
            print_warning(test, e, "高风险")
        try:
            1/0
        except Exception as e:
            print_warning(test, e)

    test()
