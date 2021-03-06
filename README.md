# uniswapTradingBotKIF

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AmisDEX/uniswapTradingBotKIF/main)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AmisDEX/uniswapTradingBotKIF/blob/master/UniswapTradingBot.ipynb)
[![nbviewer](https://img.shields.io/badge/view%20on-nbviewer-brightgreen.svg)](https://nbviewer.jupyter.org/github/AmisDEX/uniswapTradingBotKIF/blob/master/UniswapTradingBot.ipynb)


This is a trading bot that will buy and sell kif between two boundaries.

How to use:

1/ First option (recommended)

Open the notebook in Mybinder (click link above) and run it once the kernel is ready.

2/ Second option
Proceed to install on your local host:

1. use "pip install -r requirements.txt" to download the necessary libraries
2. go to the var.py file and fill in the missing information in the keys dict
3. open up uniTrade.py and edit run function at the bottom of the page to adjust the lower and upper bounds to you liking
4. use "python uniTrade.py" to start the script
