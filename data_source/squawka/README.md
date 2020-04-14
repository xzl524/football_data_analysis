### Squawka足球数据使用指南

1. 下载Squawka爬虫：https://github.com/ucdcoc/squawka-scraper 。因Squawka网站结构变化，此爬虫已无法直接使用，但是仍可以用于后续数据处理。

2. 建立一个Python2.7的环境：squawka_27，具体方法参见：https://stackoverflow.com/questions/33709391/using-multiple-python-engines-32bit-64bit-and-2-7-3-5 ，并根据Squawka爬虫说明安装需要的程序包。

3. 使用以下命令执行激活squawka_27环境。

	命令行

		activate squawka_27

4. 在此说明文件当前目录下，使用以下命令执行download.py脚本，下载XML数据文件。

	命令行

	    python download.py

5. 在此说明文件当前目录下，使用以下命令执行clean.py脚本，移除有问题的/无法处理的XML文件。

	命令行

	    python clean.py

6. 在此说明文件当前目录下，使用以下命令执行export.py脚本，输出各项比赛数据信息csv表格。

	命令行

    python export.py

7.  在此说明文件当前目录下，使用以下命令执行merge.py脚本，把每只球队每场比赛的各项比赛数据信息进行汇总，并与比赛结果进行合并，输出每只球队的比赛数据（每一行是每只球队每场比赛的数据）和每场比赛的比赛数据（每一行是每场比赛两只球队的数据）。
	
	命令行
	
    python merge.py