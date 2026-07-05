import psutil

print("CPU:", psutil.cpu_percent(interval=1), "%")
print("RAM:", psutil.virtual_memory().percent, "%")