


# 计算并绘图
import matplotlib.pyplot as plt

duration = 60  # 模拟60秒
times, attack_speeds = calculate_attack_speed_with_new_equipment(duration)

# 绘图
plt.plot(times, attack_speeds)
plt.xlabel('Time (s)')
plt.ylabel('Attack Speed (attacks/s)')
plt.title('Attack Speed Over Time with New Equipment')
plt.grid()
plt.show()
