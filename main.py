import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import os
from selenium import webdriver
import threading
def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}"
def open_chrome_tab():
    start_time = time.time()
    chrome_driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    os.environ['webdriver.chrome.driver'] = chrome_driver_path
    driver = webdriver.Chrome()
    driver.get('https://www.youtube.com/')
    element = driver.find_element('css selector', 'a#video-title-link')
    element.click()
    time.sleep(5)
    driver.quit()
    end_time = time.time()
    formatted_start_time = time.strftime("%H:%M", time.localtime(start_time))
    formatted_end_time = time.strftime("%H:%M", time.localtime(end_time))
    print(f'Браузер открылся в {formatted_start_time}')
    print(f'Браузер закрылся в {formatted_end_time}')
def background_task():
    shutdown_time = entry.get()
    try:
        hours, minutes = map(int, shutdown_time.split(':'))
        formatted_shutdown_time = f"{hours:02d}:{minutes:02d}"
        shutdown_time_label.config(text=f'Время выключения: {formatted_shutdown_time}')

        current_time = time.localtime()
        current_hours = current_time.tm_hour
        current_minutes = current_time.tm_min
        seconds_until_shutdown = (hours - current_hours) * 3600 + (minutes - current_minutes) * 60
        if seconds_until_shutdown <= 0:
            messagebox.showerror("Ошибка", "Время для выключения уже прошло или некорректно.")
        else:
            messagebox.showinfo("Установка выключения",
                                f"Компьютер будет выключен через {seconds_until_shutdown // 3600} часов {seconds_until_shutdown % 3600 // 60} минут.")
            start_time = time.time()
            formatted_start_time = time.strftime("%H:%M", time.localtime(start_time))
            start_time_label.config(text=f'Начало: {formatted_start_time}')
            print(f'НАЧАЛАСЬ ПРОГРАММА в {formatted_start_time}')
            time.sleep(seconds_until_shutdown - 300)
            open_chrome_tab()
            time.sleep(seconds_until_shutdown - 250)
            end_time = time.time()
            formatted_end_time = time.strftime("%H:%M", time.localtime(end_time))
            print(f'КОМПУКТЕР ВЫРУБИЛСЯ  в {formatted_end_time}')
            subprocess.run(["shutdown", "/s", "/t", "0"])
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат времени.")

def set_shutdown_time():
    thread = threading.Thread(target=background_task)
    thread.start()

def stop_execution():
    app.destroy()

app = tk.Tk()
app.title("Автоматическое выключение компьютера")
app.geometry("440x250")

label = tk.Label(app, text="Укажите время для автоматического выключения (ЧЧ:ММ):")
label.pack(anchor='center', pady=10)

entry = tk.Entry(app)
entry.pack(anchor='center', pady=5)

start_button = tk.Button(app, text="Установить выключение", command=set_shutdown_time)
start_button.pack(anchor='center', pady=5)

start_time_label = tk.Label(app, text="Начало: ")
start_time_label.pack(anchor='center', pady=5)

shutdown_time_label = tk.Label(app, text="Время выключения: ")
shutdown_time_label.pack(anchor='center', pady=5)

stop_button = tk.Button(app, text="Прекратить работу", command=stop_execution)
stop_button.pack(anchor='center', pady=25)

app.mainloop()