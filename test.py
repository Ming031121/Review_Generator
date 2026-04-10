import matplotlib.pyplot as plt
def calculate_attack_speed(duration):
    initial_attack_speed = 0.7  # 初始攻击速度（每秒攻击次数）
    attack_speed = initial_attack_speed
    mana = 0  # 初始蓝量
    time = 0  # 初始时间
    times = [0]  # 存储时间点
    attack_speeds = [attack_speed]  # 存储对应攻击速度

    while time < duration:
        # 计算当前攻击间隔
        attack_interval = 1 / attack_speed

        # 更新时间
        time += attack_interval

        # 更新蓝量
        mana += 10

        # 检查是否释放技能
        if mana >= 40:
            mana = 0  # 蓝量清空

            attack_speed *= 1.25  # 攻击速度增加25%
            if attack_speed > 5.0:
                attack_speed = 5.0


        # 保存当前时间和攻击速度
        times.append(time)
        attack_speeds.append(attack_speed)
        print(f"time:{time}, attacl_speed:{attack_speed}")

    return times, attack_speeds


def calculate_attack_speed_with_blue(duration, max_attack_speed=5.0):
    initial_attack_speed = 0.7*1.08  # 初始攻击速度（每秒攻击次数）
    attack_speed = initial_attack_speed
    mana = 30  # 初始蓝量，装备效果增加30点
    time = 0  # 初始时间
    times = [0]  # 存储时间点
    attack_speeds = [attack_speed]  # 存储对应攻击速度

    while time < duration:
        # 计算当前攻击间隔
        attack_interval = 1 / attack_speed

        # 更新时间
        time += attack_interval

        # 更新蓝量
        mana += 10

        # 检查是否释放技能
        if mana >= 40:
            mana = 10  # 蓝量清空后装备效果增加10点蓝量
            attack_speed *= 1.25  # 攻击速度增加25%
            attack_speed *= 1.08
            # 限制攻击速度不能超过最大值
            if attack_speed > max_attack_speed:
                attack_speed = max_attack_speed

        # 保存当前时间和攻击速度
        times.append(time)
        attack_speeds.append(attack_speed)

    return times, attack_speeds

def calculate_attack_speed_with_yangdao(duration, max_attack_speed=5.0):
    initial_attack_speed = 0.7 * 1.1  # 初始攻击速度增加10%
    attack_speed = initial_attack_speed
    mana = 0  # 初始蓝量
    time = 0  # 初始时间
    times = [0]  # 存储时间点
    attack_speeds = [attack_speed]  # 存储对应攻击速度

    while time < duration:
        # 计算当前攻击间隔
        attack_interval = 1 / attack_speed

        # 更新时间
        time += attack_interval

        # 更新蓝量
        mana += 10

        # 每次攻击增加5%攻击速度
        attack_speed *= 1.05

        # 限制攻击速度不能超过最大值
        if attack_speed > max_attack_speed:
            attack_speed = max_attack_speed

        # 检查是否释放技能
        if mana >= 40:
            mana = 0  # 蓝量清空，技能释放后不影响攻击速度
            attack_speed = attack_speed * 1.25

            if attack_speed > max_attack_speed:
                attack_speed = max_attack_speed

        # 保存当前时间和攻击速度
        times.append(time)
        attack_speeds.append(attack_speed)

    return times, attack_speeds

duration = 60

times1, speeds1 = calculate_attack_speed(duration)
times2, speeds2 = calculate_attack_speed_with_blue(duration)
times3, speeds3 = calculate_attack_speed_with_yangdao(duration)

# Plot all cases
plt.figure(figsize=(10, 6))
plt.plot(times1, speeds1, label="Case 1: Original Setup")
plt.plot(times2, speeds2, label="Case 2: +30 Mana and +10 Mana on Skill")
plt.plot(times3, speeds3, label="Case 3: +10% Initial Speed, +5%/Attack, +25% on Skill")

# Customize the plot
plt.xlabel('Time (s)')
plt.ylabel('Attack Speed (attacks/s)')
plt.title('Attack Speed Over Time for Different Cases')
plt.legend()
plt.grid()
plt.show()