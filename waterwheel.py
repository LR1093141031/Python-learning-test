import time
import os
import matplotlib.pyplot as plt
import math


# 洛伦兹水车 欧拉法
class Water_Wheel():
    def __init__(self):
        self.max_interation = 100000   # q 最大迭代次数
        self.step_interval = 0.001  # h 步长 s
        self.bucket_num = 13  # N 桶数量
        self.inject_speed = 70  # Q 注入速度 l/s
        self.leak_speed_ratio = 1  # k 相对出水速度比率 100percent/s
        self.wheel_radius = 0.05  # r 水车半径
        self.damping = 1  # v 水车阻尼系数 正相关
        self.gravity = 9.8  # g 重力加速度
        self.wheel_weight = 10  # M0 水车框架质量
        self.bucket_weight = [0 for i in range(self.bucket_num)]  # m 桶的质量
        self.bucket_angles = [i*2*math.pi/self.bucket_num for i in range(self.bucket_num)]  # theta 桶位置角
        self.angular_velocity = 0.01  # omega 水车角速度
        self.angular_acceleration = 0  # j 水车角加速度
        self.water_wheel_weight = 0  # 水车总质量
        self.water_wheel_barycenter = [0, 0]  # z 水车质心

        self.barycenter_plot_x = []
        self.barycenter_plot_y = []

    def plot(self):
        for i in range(self.max_interation):
            checked_bucket = max(enumerate([math.sin(angle) for angle in self.bucket_angles]), key=lambda x: x[-1])[0]  # 获得最上方水桶编号
            self.bucket_weight = [i * math.exp(- self.leak_speed_ratio * self.step_interval) for i in self.bucket_weight]  # 水桶漏水
            self.bucket_weight[checked_bucket] = (self.bucket_weight[checked_bucket] + self.inject_speed * self.step_interval) * \
                                                 math.exp(- self.leak_speed_ratio * self.step_interval)  # 水桶加水
            self.bucket_angles = [(i + self.angular_velocity * self.step_interval) % (2*math.pi) for i in self.bucket_angles]  # 水桶角度位移
            self.angular_velocity += self.step_interval * self.angular_acceleration  # 计算下一时刻角速度
            self.water_wheel_weight = sum(self.bucket_weight) + self.wheel_weight  # 水车总质量
            for i in range(self.bucket_num):
                self.water_wheel_barycenter[0] += self.bucket_weight[i] * math.cos(self.bucket_angles[i])  # 计算质心x坐标
                self.water_wheel_barycenter[1] += self.bucket_weight[i] * math.sin(self.bucket_angles[i])  # 计算质心x坐标
            self.water_wheel_barycenter = [(i * self.wheel_radius / self.water_wheel_weight) for i in self.water_wheel_barycenter]
            self.angular_acceleration = -1 * (self.gravity * self.water_wheel_barycenter[0] + self.damping *
                                              self.angular_velocity / self.water_wheel_weight) / pow(self.wheel_radius, 2)  # 下一时刻角加速度
            self.barycenter_plot_x.append(self.water_wheel_barycenter[0])
            self.barycenter_plot_y.append(self.water_wheel_barycenter[1])

        # print(self.barycenter_plot_y)
        print('done')
        plt.plot(self.barycenter_plot_x, self.barycenter_plot_y)
        plt.show()

    #def __iter__(self):
    #    return self

    #def __next__(self):

if __name__ == '__main__':
    water_wheel = Water_Wheel()
    water_wheel.plot()



