import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import os
from selenium import webdriver
import threading

def background_task():
    shutdown_time = entry.get()
    try:
        hours, minutes = map(int, shutdown_time.split(':'))
        current_time = time.localtime()
        current_hours = current_time.tm_hour
        current_minutes = current_time.tm_min
        seconds_until_shutdown = (hours - current_hours) * 3600 + (minutes - current_minutes) * 60

        if seconds_until_shutdown <= 0:
            messagebox.showerror("Ошибка", "Время для выключения уже прошло или некорректно.")
        else:
            messagebox.showinfo("Установка выключения",
                                f"Компьютер будет выключен через {seconds_until_shutdown // 3600} часов {seconds_until_shutdown % 3600 // 60} минут.")

            chrome_driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
            os.environ['webdriver.chrome.driver'] = chrome_driver_path
            driver = webdriver.Chrome()
            driver.get('https://www.youtube.com/')
            element = driver.find_element('css selector', 'a#video-title-link')
            element.click()
            time.sleep(20)
            driver.quit()
            time.sleep(seconds_until_shutdown - 300)  # Wait 5 minutes (300 seconds) before shutdown
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
app.geometry("400x200")

label = tk.Label(app, text="Укажите время для автоматического выключения (ЧЧ:ММ):")
label.pack(anchor='center', pady=10)

entry = tk.Entry(app)
entry.pack(anchor='center', pady=5)

start_button = tk.Button(app, text="Установить выключение", command=set_shutdown_time)
start_button.pack(anchor='center',pady=5)

stop_button = tk.Button(app, text="Прекратить работу", command=stop_execution)
stop_button.pack(anchor='center')

app.mainloop()
