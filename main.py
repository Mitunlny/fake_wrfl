import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def replace_strings_in_file(file_path, replacements):
    """
    替换文件中的特定字符串
    
    参数:
        file_path (str): 要处理的文件路径
        replacements (dict): 替换映射字典 {原字符串: 新字符串}
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 执行替换
        modified = False
        for old_str, new_str in replacements.items():
            if old_str in content:
                content = content.replace(old_str, new_str)
                modified = True
        
        # 如果有修改，则写回文件
        if modified:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("成功", f"文件 {file_path} 已更新")
            return True
        else:
            messagebox.showwarning("警告", "文件中未找到需要替换的内容")
            return False
            
    except FileNotFoundError:
        messagebox.showerror("错误", f"文件 {file_path} 未找到")
        return False
    except Exception as e:
        messagebox.showerror("错误", f"处理文件时发生错误: {e}")
        return False

def reset_fake_wrfl_from_template():
    """使用backup的内容重置fake_wrfl.py"""
    try:
        # 读取模板文件内容
        with open('backup.txt', 'r', encoding='utf-8') as template_file:
            template_content = template_file.read()
        
        # 写入目标文件
        with open('fake_wrfl.py', 'w', encoding='utf-8') as target_file:
            target_file.write(template_content)
        
        return True
    except FileNotFoundError:
        messagebox.showerror("错误", "模板文件backup.txt未找到")
        return False
    except Exception as e:
        messagebox.showerror("错误", f"重置文件时发生错误: {e}")
        return False

def get_current_time():
    """获取当前时间并格式化为字符串"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def set_start_time():
    """设置请假开始时间为当前时间"""
    start_time_entry.delete(0, tk.END)
    start_time_entry.insert(0, get_current_time())

def set_end_time():
    """设置请假结束时间为当前时间"""
    end_time_entry.delete(0, tk.END)
    end_time_entry.insert(0, get_current_time())

def set_create_time():
    """设置创建时间为当前时间"""
    create_time_entry.delete(0, tk.END)
    create_time_entry.insert(0, get_current_time())

def set_finish_time():
    """设置办结时间为当前时间"""
    finish_time_entry.delete(0, tk.END)
    finish_time_entry.insert(0, get_current_time())

def set_all_times():
    """设置所有时间字段为当前时间"""
    current_time = get_current_time()
    start_time_entry.delete(0, tk.END)
    start_time_entry.insert(0, current_time)
    end_time_entry.delete(0, tk.END)
    end_time_entry.insert(0, current_time)
    create_time_entry.delete(0, tk.END)
    create_time_entry.insert(0, current_time)
    finish_time_entry.delete(0, tk.END)
    finish_time_entry.insert(0, current_time)

def submit_form():
    # 获取用户输入
    data = {
        '{name}': name_entry.get(),
        '{student_id}': student_id_entry.get(),
        '{year}': year_entry.get(),
        '{semester}': semester_entry.get(),
        '{student_class}': class_entry.get(),
        '{sex}': sex_combobox.get(),
        '{Type}': type_combobox.get(),
        '{day}': day_entry.get(),
        '{start_time}': start_time_entry.get(),
        '{end_time}': end_time_entry.get(),
        '{creat_time}': create_time_entry.get(),
        '{finish_time}': finish_time_entry.get()
    }
    
    # 检查必填字段
    for field, value in data.items():
        if not value:
            messagebox.showerror("错误", "请填写所有字段")
            return
    
    # 执行替换
    file_path = "fake_wrfl.py"
    if not replace_strings_in_file(file_path, data):
        return
    
    # 运行脚本
    try:
        os.system(f'python "{file_path}"')
    except Exception as e:
        messagebox.showerror("错误", f"运行脚本时出错: {e}")
        return
    
    # 重置fake_wrfl.py文件为backup.txt的内容
    if reset_fake_wrfl_from_template():
        messagebox.showinfo("完成", "所有操作已完成，文件已重置")

# 创建主窗口
root = tk.Tk()
root.title("请假条信息填写系统 | made by M.Y")
root.geometry("450x610")

# 设置样式
style = ttk.Style()
style.configure('TLabel', font=('Arial', 10))
style.configure('TEntry', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10, 'bold'))

# 创建表单框架
form_frame = ttk.Frame(root, padding="20")
form_frame.pack(fill=tk.BOTH, expand=True)

# 姓名
ttk.Label(form_frame, text="姓名:").grid(row=0, column=0, sticky=tk.W, pady=5)
name_entry = ttk.Entry(form_frame)
name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

# 学号
ttk.Label(form_frame, text="学号:").grid(row=1, column=0, sticky=tk.W, pady=5)
student_id_entry = ttk.Entry(form_frame)
student_id_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

# 学年
ttk.Label(form_frame, text="学年 (xxxx-xxxx):").grid(row=2, column=0, sticky=tk.W, pady=5)
year_entry = ttk.Entry(form_frame)
year_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)

# 学期
ttk.Label(form_frame, text="学期 (第x学期):").grid(row=3, column=0, sticky=tk.W, pady=5)
semester_entry = ttk.Entry(form_frame)
semester_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)

# 专业班级
ttk.Label(form_frame, text="专业班级:").grid(row=4, column=0, sticky=tk.W, pady=5)
class_entry = ttk.Entry(form_frame)
class_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)

# 性别
ttk.Label(form_frame, text="性别:").grid(row=5, column=0, sticky=tk.W, pady=5)
sex_combobox = ttk.Combobox(form_frame, values=["男", "女"])
sex_combobox.grid(row=5, column=1, sticky=tk.EW, pady=5)

# 请假类型
ttk.Label(form_frame, text="请假类型:").grid(row=6, column=0, sticky=tk.W, pady=5)
type_combobox = ttk.Combobox(form_frame, values=["事假", "病假"])
type_combobox.grid(row=6, column=1, sticky=tk.EW, pady=5)

# 请假天数
ttk.Label(form_frame, text="请假天数:").grid(row=7, column=0, sticky=tk.W, pady=5)
day_entry = ttk.Entry(form_frame)
day_entry.grid(row=7, column=1, sticky=tk.EW, pady=5)

# 请假开始时间
ttk.Label(form_frame, text="请假开始时间:").grid(row=8, column=0, sticky=tk.W, pady=5)
start_time_frame = ttk.Frame(form_frame)
start_time_frame.grid(row=8, column=1, sticky=tk.EW, pady=5)
start_time_entry = ttk.Entry(start_time_frame)
start_time_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
start_time_button = ttk.Button(start_time_frame, text="现在", width=5, command=set_start_time)
start_time_button.pack(side=tk.RIGHT, padx=(5, 0))

# 请假结束时间
ttk.Label(form_frame, text="请假结束时间:").grid(row=9, column=0, sticky=tk.W, pady=5)
end_time_frame = ttk.Frame(form_frame)
end_time_frame.grid(row=9, column=1, sticky=tk.EW, pady=5)
end_time_entry = ttk.Entry(end_time_frame)
end_time_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
end_time_button = ttk.Button(end_time_frame, text="现在", width=5, command=set_end_time)
end_time_button.pack(side=tk.RIGHT, padx=(5, 0))

# 创建时间
ttk.Label(form_frame, text="创建时间:").grid(row=10, column=0, sticky=tk.W, pady=5)
create_time_frame = ttk.Frame(form_frame)
create_time_frame.grid(row=10, column=1, sticky=tk.EW, pady=5)
create_time_entry = ttk.Entry(create_time_frame)
create_time_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
create_time_button = ttk.Button(create_time_frame, text="现在", width=5, command=set_create_time)
create_time_button.pack(side=tk.RIGHT, padx=(5, 0))

# 办结时间
ttk.Label(form_frame, text="办结时间:").grid(row=11, column=0, sticky=tk.W, pady=5)
finish_time_frame = ttk.Frame(form_frame)
finish_time_frame.grid(row=11, column=1, sticky=tk.EW, pady=5)
finish_time_entry = ttk.Entry(finish_time_frame)
finish_time_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
finish_time_button = ttk.Button(finish_time_frame, text="现在", width=5, command=set_finish_time)
finish_time_button.pack(side=tk.RIGHT, padx=(5, 0))



# 提交按钮
submit_button = ttk.Button(form_frame, text="提交", command=submit_form)
submit_button.grid(row=13, column=0, columnspan=2, pady=20)

# 提示字体

text_widget = tk.Text(root)
text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
text_widget.tag_configure("red", foreground="red") # 配置标签样式:cite[6]:cite[8]
text_widget.insert(tk.END, "本程序为良好的开源项目，并无任何病毒和恶意代码！我们不会对您的电脑造成任何伤害！！！使用本项目起，即代表您已经同意您使用本项目所造成的所有后果一律由您本人承担！！！\n", "red") # 插入文本时应用标签:cite[6]


text_widget.insert(tk.END, "如果您觉得本项目对您有所帮助，欢迎在GitHub上给本项目点个⭐️⭐️⭐️⭐️⭐️！\n")


# 配置网格权重
form_frame.columnconfigure(1, weight=1)

# 运行主循环
root.mainloop()