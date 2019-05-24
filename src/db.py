import os
from os.path import join, dirname
import pymysql.cursors
from flask import Flask, jsonify, make_response, request, render_template
import datetime


conn = pymysql.connect(host='db',
                       user='test',
                       db='test1492_testtable',
                       password='test',
                       cursorclass=pymysql.cursors.DictCursor
                       )


app = Flask(__name__, template_folder='./')


@app.route('/')
def index():
    return 'server is running in localhost'


@app.route('/spot')
def getspot():
    try:
        sql = 'select * from spot'
        with conn.cursor() as c:
            c.execute(sql)
            res = c.fetchall()
            return jsonify(res)
    finally:
        c.close()


@app.route('/spot/<int:id>')
def getspot_byid(id):
    try:
        sql = 'select * from spot join tag on (spot.tagid = tag.id) where spot.id = ' + str(id)
        with conn.cursor() as c:
            c.execute(sql)
            res = c.fetchall()
            return jsonify(res[0])
    finally:
        c.close()


def getSeason(month):
	if month < 4 :
		return 'spring'
	elif month < 7:
		return 'summer'
	elif month < 10:
		return 'fall'
	else:
		return 'winter'

@app.route('/refine/<int:isslope>/<int:isopen>/<int:isseason>')
def refine(isslope, isopen, isseason):
    
    try:
        sql = 'select * from spot join tag on (spot.tagid = tag.id)'
        with conn.cursor() as c:
            c.execute(sql)
            res = c.fetchall()
            tmp = []
		
            if isslope == 1:
                for d in res:
                    if not d['slope'] == 'true':
                        tmp.append(d)
                        res = tmp.copy()
                        tmp.clear()
            if isopen == 1 :
                for d in res:				
                    if not d['opentime'] or not d['endtime'] :
                        tmp.append(d)
                        res = tmp.copy()
                        tmp.clear()

            if isseason == 1:
                month = datetime.datetime.now().month
                for d in res:
                    if d['season'] == getSeason(month):
                        tmp.append(d)
                        res = tmp.copy()
                        tmp.clear()
                        return jsonify(res)
    finally:
        c.close()


@app.route('/tag')
def gettag():
    
    try:
        sql = 'select * from tag'
        with conn.cursor() as c:
            c.execute(sql)
            res = c.fetchall()
            return jsonify(res)
    finally:
        c.close()





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13334,debug=True)
