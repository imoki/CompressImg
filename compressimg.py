# 批量图片压缩程序
'''
这些可以在main函数中自定义
dirin = 'in'	# 输入图片的文件夹。这里是放准备压缩的图片，默认文件夹名称为in
dirout = 'out'	# 输出图片的文件夹。这里会存放压缩好的图片，默认文件夹名称为out
sizeKB = 100	# 输出图片的最大值，默认100KB。压缩好的图片尺寸不会超过100KB
xout = 1366	# 输出图片的x轴长度，默认1366px，y轴通过动态计算得到。
'''
from PIL import Image
import os
import shutil

def imagesize(file):	# 计算图片占用空间
	size = os.path.getsize(file)/1024 # kb -> b
	return size
	
def createdir(outfile):	# 传入文件路径，递归创建文件夹
	outpath = outfile.split("\\")
	outpath.pop(-1)
	outpath = "\\".join(outpath)
	if not os.path.exists(outfile):
		try:
			os.makedirs(outpath)
		except:
			#print("目录已存在")
			pass

def compress(infile, outfile, sizeKB, xout, step=10, quality=80):	# 图片压缩
	createdir(outfile)
	outsize = imagesize(infile)	# 计算原始图片占用空间
	if outsize > sizeKB:	# 若输出图片占用空间大于目标空间
		im = Image.open(infile)
		while outsize > sizeKB:	# 只要大于目标尺寸，则压缩，直至step为0
			im.save(outfile, quality=quality)	# 暂时保存输出图片
			if quality - step < 0:
				break
			quality -= step
			outsize = imagesize(outfile)	# 再次计算图片占用空间
		x, y = im.size	# 原始图片的x,y轴大小
		yout = int(y * xout / x )	# 输出的y轴大小
		out = im.resize((xout, yout), Image.ANTIALIAS)	# 调整图片大小
		out.save(outfile)	# 保存输出文件
	else:	# 只要小于目标尺寸，则直接复制一份到输出文件夹
		shutil.copy(infile, outfile)

def readimage(imagein, imageout, sizeKB, xout):	# 读取图片，输出图片
	print(imagein)
	compress(imagein, imageout, sizeKB, xout)	# 进行图片压缩

def readimagelist(dirin, dirout):	# 读取所有文件，存入list中
	if os.path.exists(dirin):	# 若输入图片的文件夹存在，否则建立文件夹
		files = os.listdir(dirin)
		for file in files:
			currentpath = os.path.join(dirin, file)	# 路径全名
			outpath = currentpath.split("\\")
			outpath[0] = dirout	# 将第一层目录替换
			outpath = "\\".join(outpath)
			if os.path.isdir(currentpath):
				readimagelist(currentpath, dirout)
			else:
				listimagein.append(currentpath)	# 存入文件路径
				listimageout.append(outpath)	# 生成输出文件路径
	else:
		os.mkdir(dirin)

if __name__ == '__main__':
	global listimagein,listimageout
	listimagein = []
	listimageout = []
	dirin = 'in'	# 输入图片的文件夹
	dirout = 'out'	# 输出图片的文件夹
	sizeKB = 100	# 输出图片的最大值，默认100KB
	xout = 1366	# 输出图片的x轴长度，默认1366px。 y轴通过动态计算得到
	readimagelist(dirin, dirout)	# 读取所有图片文件
	for i in range(0,len(listimagein)):	# 读取输入图片的文件夹中的每一张图片
		readimage(listimagein[i], listimageout[i], sizeKB, xout)