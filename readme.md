# Shortbread

An URL shorten API with Python and Flask on Heroku

## 怎麼使用
`>curl https://shortbread.herokuapp.com/short?url=你要查詢的url(不含http://或https://)`

ex 
	`>curl https://shortbread.herokuapp.com/short?url=tw.yahoo.com`
	Input: tw.yahoo.com
	Output: https://shortbread.herokuapp.com/r/03

`>curl https://shortbread.herokuapp.com/r/03`
會轉到yahoo台灣的網站去


## 開發環境建置

	基本上跟隨Heorku的官方教學做
	https://devcenter.heroku.com/articles/getting-started-with-python#introduction

	1. 裝Chocolatey
	https://chocolatey.org/install

	2. 裝python 3

	3. 裝pip和pipenv

		pipenv是讓各專案有各自的虛擬空間

	4. 裝Flask

	5. 裝Heroku CLI

	6. 裝Psycopg2
		主要是用來操作Postgres用到的
	7. 裝Flask-Migrate

	8. 裝Flask-SQLAlchemy

## deploy到Heroku上
	
### 事前準備

Local端可以正常運作之後，就可以
1.用Heorku CLI
2.網頁去建立Python App

此外還要準備
1. Procfile
		`web gunicorn 你的app主要的python檔:app`
    以我這個project來說是main.py
	`web gunicorn main:app`

2. requirements.txt
		把所需要的套件全部列在上面
		可用 `pip freeze > requirements.txt` 產生

### push上去Heroku
	
把Procfile和requirement.txt 以及專案的檔案都add並且 commit之後
再push到Heroku上
`git push heroku master`

### 連結Heroku Postgres
可以用Heroku CLI或網頁在app加上Heroku Postgres的Add-on

建好之後可以在Settings找到資料庫的URL，把他加上去
` app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://資料庫url'`

### 初始化db
		
用dbModel.py來調整資料庫的table
		
1. 在local端執行
	`python dbModel.py db init`
	`python dbModel.py db migrate`

2. 完畢會產生migrations/資料夾，把他push到heroku上
	再執行 `heorku run dbModel.py db upgrade`

### heroku app的位置
https://project名稱.herokuapp.com/

### heroku app的log檔
https://dashboard.heroku.com/apps/project名稱/logs
或是用CLI看log `heroku logs -t`

## Reference 
https://github.com/twtrubiks/Deploying-Flask-To-Heroku
https://github.com/twtrubiks/Flask-Migrate-Tutorial
https://impythonist.wordpress.com/2015/10/31/building-your-own-url-shortening-service-with-python-and-flask/
https://gist.github.com/bhelx/778542
