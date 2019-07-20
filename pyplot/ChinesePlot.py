import numpy
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import functools
class ChinessPlot():
    def __init__(self,font_file):
        self.font = fm.FontProperties(fname=font_file)
        plt.legend = functools.partial(plt.legend,prop=self.font)
        plt.title = functools.partial(plt.title,fontproperties=self.font)
        plt.xlabel = functools.partial(plt.xlabel,fontproperties=self.font)
        plt.ylabel = functools.partial(plt.ylabel,fontproperties=self.font)
        plt.text = functools.partial(plt.text,fontproperties=self.font)
        plt.annotate = functools.partial(plt.annotate,fontproperties = self.font)

    def draw(self):
        x = numpy.linspace(-10,10,100)
        y = (lambda x:2*x+5)(x)
        plt.title('匀速运动')
        plt.xlabel('x轴')
        plt.ylabel('y轴')
        plt.plot(x,y,label='线性函数')
        plt.text(-2.5,0,"文本描述",va='top')
        plt.legend()
        plt.annotate('0点',(0,5), xytext=(+30, -30), textcoords='offset points', xycoords='data', arrowprops=dict(arrowstyle='->',
                                 connectionstyle='arc3, rad=.2'))
        plt.show()



if __name__ == '__main__':
    ChinessPlot('fonts/youyuan.TTF').draw()