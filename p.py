import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# 示例数据
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 35]

# 创建折线图
sns.lineplot(x = x, y = y)

# 保存图像到当前目录
plt.savefig(r'static/line_plot.png')

