from flask import Flask,jsonify, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gamru12'
app.config['MYSQL_DB'] = 'companydb'
app.config["MYSQL_CURSORCLASS"]='DictCursor'
mysql = MySQL(app)



@app.route('/',defaults={'page':1})
@app.route('/<int:page>')
def listCompany(page):
    page-=1
    perpage=10
    startat=page*perpage
    cur = mysql.connection.cursor()
    query="Select * from company limit %s,%s "
    cur.execute(query,(startat,perpage))
    print cur.description
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/listFolder',defaults={'page':1})
@app.route('/listFolder/<string:id>/<int:page>')
def listFolder(id,page):
    page-=1
    perpage=10
    startat=page*perpage
    cur = mysql.connection.cursor()
    
    query="Select * from folder  where companyId=%s limit %s,%s"
    cur.execute(query, (id,startat,perpage))

    print cur.description
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/listDocument',defaults={'page':1})
@app.route('/listDocument/<string:id>/<int:page>')
def listDocument(id,page):
    page-=1
    perpage=10
    startat=page*perpage
    cur = mysql.connection.cursor()
    query="Select * from document where folderId=%s limit %s,%s"
    cur.execute(query, (id,startat,perpage))
    print cur.description
    data = cur.fetchall()
    cur.close()
    return jsonify(data)



@app.route('/createCompany',methods=['POST'])
def createCompany():
    cur=mysql.connection.cursor()
    content=request.get_json()
    name=content['name']
    no=content['no']
    mail=content['mail']
    isActive=content['isActive']
    query="Insert into company(name,no,mail,isActive) VALUES(%s,%s,%s,%s)"
    cur.execute(query, (name,no,mail,isActive))
    mysql.connection.commit()
    return "tamam"
@app.route('/createFolder',methods=['POST'])
def createFolder():
    cur=mysql.connection.cursor()
    content=request.get_json()
    name=content['name']
    companyId=content['companyId']
    query="Insert into folder(FolderName,companyId) VALUES(%s,%s)"
    cur.execute(query, (name,companyId))
    mysql.connection.commit()
    return "tamam"
@app.route('/createDocument',methods=['POST'])
def createDocument():
    cur=mysql.connection.cursor()
    content=request.get_json()
    name=content['name']
    folderId=content['folderId']
    query="Insert into document(name,folderId) VALUES(%s,%s)"
    cur.execute(query, (name,folderId))
    mysql.connection.commit()
    return "tamam"



@app.route('/updateCompany/<string:id>',methods=['PUT'])
def updateCompany(id):

    cur=mysql.connection.cursor()
    content=request.get_json()
    name=content['name']
    no=content['no']
    mail=content['mail']
    isActive=content['isActive']
    id=content['id']
    query="UPDATE company SET name=%s,no=%s,mail=%s,isActive=%s WHERE id=%s"
    
    cur.execute(query, (name,no,mail,isActive,id))
    mysql.connection.commit()
    return "tamam"

@app.route('/updateFolder/<string:id>',methods=['PUT'])
def updateFolder(id):

    cur=mysql.connection.cursor()
    content=request.get_json()
    id=content['id']
    name=content['name']
    companyId=content['companyId']
    query="UPDATE folder SET name=%s,companyId=%s WHERE id=%s"
    
    cur.execute(query, (name,companyId,id))
    mysql.connection.commit()
    return "tamam"

@app.route('/updateDocument/<string:id>',methods=['PUT'])
def updateDocument(id):

    cur=mysql.connection.cursor()
    content=request.get_json()
    name=content['name']
    folderId=content['folderId']
    id=content['id']
    query="UPDATE document SET name=%s,folderId=%s WHERE id=%s"
    
    cur.execute(query, (name,folderId,id))
    mysql.connection.commit()
    return "tamam"


@app.route("/deleteCompany/<string:id>",methods=['DELETE'])
def deleteCompany(id):
     cur=mysql.connection.cursor()
   
     query="Delete from company WHERE id=%s"
    
     cur.execute(query, (id))
     mysql.connection.commit()
     return "tamam"
@app.route("/deleteFolder/<string:id>",methods=['DELETE'])
def deleteFolder(id):
     cur=mysql.connection.cursor()
   
     query="Delete from folder WHERE id=%s"
    
     cur.execute(query, (id))
     mysql.connection.commit()
     return "tamam"

@app.route("/deleteDocument/<string:id>",methods=['DELETE'])
def deleteDocument(id):
     cur=mysql.connection.cursor()
   
     query="Delete from document WHERE id=%s"
    
     cur.execute(query, (id))
     mysql.connection.commit()
     return "tamam"

@app.route('/searchCompany',defaults={'page':1})
@app.route('/searchCompany/<int:page>',methods=['POST'])
def companySearch(page):
    page-=1
    perpage=10
    startat=page*perpage
    sqlQuery = ""
    content=request.get_json()
    if content['name'] != "" :
        if content['mail'] != "":
            sqlQuery = "Select * from company WHERE name Like %s and mail Like %s limit %s,%s"
            cur = mysql.connection.cursor()
            cur.execute(sqlQuery,("%"+content['name']+"%","%"+content['mail']+"%" ,startat,perpage))
            data = cur.fetchall()
            cur.close()
            return jsonify(data)
        else:
            sqlQuery = "Select * from company WHERE name Like %s limit %s,%s"
            cur = mysql.connection.cursor()
            
            cur.execute(sqlQuery,("%"+content['name']+"%",startat,perpage))
            data = cur.fetchall()
            cur.close()
            return jsonify(data)
    elif content['mail'] != "" :
        
        sqlQuery = "Select * from company WHERE mail Like %s limit %s,%s"
        cur = mysql.connection.cursor()
        cur.execute(sqlQuery,("%"+content['mail']+"%",startat,perpage))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    else:
       
        sqlQuery = "Select * from company limit %s,%s"
        cur = mysql.connection.cursor()
        cur.execute(sqlQuery,(startat,perpage))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)

@app.route('/searchFolder',defaults={'page':1})
@app.route('/searchFolder/<int:page>',methods=['POST'])
def folderS(page):
    page-=1
    perpage=10
    startat=page*perpage
    sqlQuery = ""
    content=request.get_json()
    if content['name'] != "" :
        
            sqlQuery = "Select * from folder WHERE name Like %s limit %s,%s"
            cur = mysql.connection.cursor()
            cur.execute(sqlQuery,("%"+content['name']+"%",startat,perpage))
            data = cur.fetchall()
            cur.close()
            return jsonify(data)
    else:
       
        sqlQuery = "Select * from folder limit %s,%s"
        cur = mysql.connection.cursor()
        cur.execute(sqlQuery,(startat,perpage))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
@app.route('/searchDocument',defaults={'page':1})    
@app.route('/searchDocument/<int:page>',methods=['POST'])
def documentS(page):
    page-=1
    perpage=10
    startat=page*perpage
    sqlQuery = ""
    content=request.get_json()
    if content['name'] != "" :
        
            sqlQuery = "Select * from document WHERE name Like %s limit %s,%s"
            cur = mysql.connection.cursor()
            cur.execute(sqlQuery,("%"+content['name']+"%",startat,perpage))
            data = cur.fetchall()
            cur.close()
            return jsonify(data)
    else:
       
        sqlQuery = "Select * from document limit %s,%s"
        cur = mysql.connection.cursor()
        cur.execute(sqlQuery,(startat,perpage))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)


  
    



if __name__ == '__main__':
    app.run(port=3001,debug=True)