from flask import Flask
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from flask import jsonify, request
import json

mysql = MySQL()
app = Flask(__name__)
# MySQL configurations

mysql.init_app(app)
api = Api(app)
app.config['MYSQL_DATABASE_USER'] = 'SREEMATHI'
app.config['MYSQL_DATABASE_PASSWORD'] = 'SREEMAISH1@'
app.config['MYSQL_DATABASE_DB'] = 'mydatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


parser = reqparse.RequestParser()
class CustomersList(Resource):
     def get(self):
        conn = mysql.connect()

        cursor = conn.cursor()
        sql = "SELECT * FROM customers;"
        cursor.execute(sql)
         # cursor.callproc('spCreateUser', (name, age, spec))
        #data = cursor.fetchall()
        data = cursor.fetchall()
        resp = jsonify(data)
        return resp

     def post(self):
        parser.add_argument("name")
        parser.add_argument("fname")
        parser.add_argument("lname")
        parser.add_argument("address")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        # student_id = int(max(STUDENTS.keys())) + 1
        # student_id = '%i' % student_id
        # STUDENTS[student_id] = {
        #   "name": args["name"],
        #   "age": args["age"],
        #   "spec": args["spec"],
        # }
        conn = mysql.connect()

        cursor = conn.cursor()
        sql = "INSERT INTO customers (name, fname, lname, address, age, spec ) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (args["name"], args["fname"],args["lname"],args["address"],args["age"], args["spec"])
        cursor.execute(sql, val)
       # cursor.callproc('spCreateUser', (name, age, spec))
        data = cursor.fetchall()
        conn.commit()
        resp = jsonify('Customer Added successfully!')
        return resp


class Customer(Resource):
     def get(self, name):
          if name not in Customers:
              return "Customer "+ name +" Not found", 404
          else:
              return Customers[name]
     def put(self, name):
          parser.add_argument("name")
          parser.add_argument("age")
          parser.add_argument("spec")
          args = parser.parse_args()
          if name not in Customers:
              return "Record not found", 404
          else:
              customer = CUSTOMERS[name]
              customer["name"] = args["name"] if args["name"] is not None else customer["name"]
              customer["age"] = args["age"] if args["age"] is not None else customer["age"]
              customer["spec"] = args["spec"] if args["spec"] is not None else customer["spec"]
              return customer, 200


     def post(self,name):
         conn = mysql.connect()
         cursor = conn.cursor()
         try:
             _json = request.json
             name = _json['name']
             fname = _json['fname']
             lname = _json['lname']
             email = _json['email']
             address = _json['address']
             spec = _json['spec']
             age = _json['age']

             # validate the received values
             if fname and lname and email and address and spec and request.method == 'POST':
                 # do not save password as a plain text
                 # save edits
                 sql = "UPDATE customers SET fname=%s,lname=%s,address=%s,age=%s,Email=%s,spec=%s WHERE name=%s"
                 data = (fname,lname,address,age,email,spec,name)

                 cursor.execute(sql, data)
                 conn.commit()
                 resp = jsonify('Customer detail updated successfully!')
                 resp.status_code = 200
                 return resp
             else:
                 return not_found()
         except Exception as e:
             print(e)
         finally:
             cursor.close()
             conn.close()

     def delete(self,name):
         try:
             conn = mysql.connect()
             cursor = conn.cursor()
             cursor.execute("DELETE FROM customers WHERE name=%s", (name))
             conn.commit()
             resp = jsonify('Customer detail deleted successfully!')
             resp.status_code = 200
             return resp
         except Exception as e:
             print(e)
         finally:
             cursor.close()
             conn.close()
     # def delete(self, name):
     #      if student_id not in STUDENTS:
     #          return "Not found", 404
     #      else:
     #          del STUDENTS[student_id]
     #          return '', 204
api.add_resource(CustomersList, '/customer/')
api.add_resource(Customer, '/customer/<name>')



if __name__ == "__main__":
  app.run(debug=True)