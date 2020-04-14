### Kaggle欧洲足球数据库使用指南

1. 从Kaggle下载[欧洲足球数据库](https://www.kaggle.com/hugomathien/soccer)，解压并保存数据库文件database.sqlite到本目录。

2. 在当前目录下，使用以下命令执行extract.py脚本，输出比赛数据统计信息csv表格。

	命令行
	
	python extract.py

3. 在当前目录下，使用以下命令执行merge.py脚本，输出包含比赛数据统计的比赛信息csv表格。

	命令行
	
	python merge.py

### Kaggle European Soccer Database Usage

1. Download [Kaggle European Soccer Database](https://www.kaggle.com/hugomathien/soccer), unzip and save database.sqlite to current directory.

2. Redirect to current directory and run extract.py in command to export event stats csv files.

	Command-line Usage
	
	python extract.py
	
3. Redirect to current directory and run merge.py in command to export match.csv with match event statistics.

	Command-line Usage
	
	python merge.py
