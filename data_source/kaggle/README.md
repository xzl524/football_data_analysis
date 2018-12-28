# Kaggle欧洲足球数据库使用指南

* 从Kaggle下载[欧洲足球数据库](https://www.kaggle.com/hugomathien/soccer)，解压并保存到本地（可保存到本目录），得到数据库文件database.sqlite。

* 若需要从数据库中输出比赛相关数据统计，请使用以下命令执行extract.py脚本，输出比赛相关数据统计信息的csv表格。

执行命令行
	
	python extract.py [path_to_database]
	
参数解释

path_to_database: database.sqlite的路径.


# Kaggle European Soccer Database Usage

* Download [Kaggle European Soccer Database](https://www.kaggle.com/hugomathien/soccer), unzip and save database.sqlite to local disk (it can be saved in current directory).

* Run extract.py in command to export event stats csv files if match event stats are desired.

Command-line Usage
	
	python extract.py [path_to_database]

Parameter Descriptions

path_to_database: str, directory of database.sqlite.
