# Football (Soccer) Data Analysis Projects

Apply machine learning/data mining techniques to understand football (soccer).

### Dataset
* [Kaggle dataset](https://www.kaggle.com/hugomathien/soccer)
* [Squawka dataset using Squawka scraper](https://github.com/ucdcoc/squawka-scraper) (this tool requires some modifications).

### Projects (Completed)
1. [European Soccer Database Analysis](https://github.com/xzl524/football_data_analysis/tree/master/projects/european_soccer_database_analysis)
	- predicts distributions of number of goals, match results, and match scores with poisson model.
	- applies exploratory data analysis
2. [Football Match Outcome Prediction](https://github.com/xzl524/football_data_analysis/tree/master/projects/match_outcome_prediction)
	- applies supervised learning to football event data for match outcome prediction.
	- tries to answer 2 questions:
		- to what degree can football event data predict match outcome?
		- what event types are most related to match outcome?

### Projects (Ongoing)
To Be Continued.

### Requirements
Python 3.6 (with Tensorflow if neural network model is needed)

### 写在前面：大数据能否改变足球比赛？
#### 作者：带球小弟
不管你喜不喜欢，足球比赛转播中都会播报比赛双方的各项数据统计，包括控球率、射门次数、角球次数、传球次数、越位次数等等。事实上，足球比赛已经全方位地拥抱了数据。教练会用数据分析软件来准备比赛，球迷会用比赛数据统计来探讨比赛，球探会用球员数据系统来挖掘球员。抛开一切，对于足球比赛本身大家最关心的也就是比分，进球数和球队积分，这些通通都是数据，只是现在的数据类型更加丰富和复杂了。

在这一大数据和人工智能时代，数据的重要性已经被广泛接受。事实上，数据已经被用来改变体育比赛了。最著名的案例发生在棒球，最后还被拍成了电影《点球成金》。很多人相信同样的事情也会发生在足球，这其中就包括了本人。

然而，面对数据，也有很多人感到的不是希望，而是焦虑。我很难去说这样的人一定是保守的。原因有以下两点。

首先，数据本身往往太过复杂而令人难以理解。任何想要通过直接阅读数据来理解数据的尝试都很困难。

其次，想要从数据中得到结论也没有想象中那么简单。这里要对数据分析泼盆冷水，降低一下你对数据分析的期待：数据分析并不一定能给出令人满意的答案，即使有大数据也不行。事实上，大数据在某种程度上来说并没有使得分析变得更加简单，反而是增加了困难。原因在于，很多情况下大数据带来的不是更多的信息，而是更多的“噪音”。如果没有合适的工具和方法论，要想从“噪音”中提取有效信息其实更加困难。

要化解上述困难，需要我们能够正确地对待数据和数据分析。对待数据，我们需要去把握的不是数据，而是数据背后的规律。这样的态度有助于我们不会在纷繁的数据中迷失。对待数据分析，我们需要事实求是。确保使用恰当的数据分析工具，正确理解数据分析的结论，并用实践去检验结论。本人在对数据分析过程进行说明的同时，也会对如何正确使用数据分析的方法论进行讨论。这样的讨论普遍适用，而非只限于足球数据。

最后，我希望数据分析能够在未来帮助到中国足球。本人相信，中国足球现在还很落后，但是马上就会有很大的进步。这样的进步还用不到数据和数据分析。等到中国足球发展到一定程度想要利用数据更进一步的时候，希望现在的讨论能够对中国足球有所帮助。

### 技术说明

理论工具：最主要的数学理论是概率论和数理统计，以及由此发展出来的机器学习算法，包括现在很热门的深度学习（或者叫做神经网络）。

编程工具：python。

语言能力：虽然所有的数据分析均用中文叙述，但是因为数据库本身是英文的，所以一定的英文基础是需要的。
