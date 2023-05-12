from flask import Flask, render_template, request
from split import *

member_names = []

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="india@123",
    database="split_bill"
)

# Create a cursor object
cursor = db.cursor()

app = Flask(__name__)

@app.route("/")
def home():
    title = 'Split Bill - Home'
    return render_template('index.html', title=title)

@app.route('/split_expense_show_group')
def split_expense_show_group():
    group_names = show_group_name()
    return render_template('select_group.html', groups=group_names)
    

@app.route('/show_member', methods=['GET','POST'])
def show_member():
    global table_name 
    if request.method == 'POST':
        table_name = request.form['group']
    member_names = show_column_name(table_name[2:len(table_name)-3])
    return render_template("show_member.html",members = member_names)


@app.route('/split_expense_result',methods = ['GET','POST'])
def split_result():
    if request.method == 'POST':
        split_member_names = list(request.form.getlist('member'))
        amount = int(request.form['amount'])
        expence_name = request.form['expence_name']
        paidby = request.form['paidby']
        choice = request.form['split']
        cos_amount = list(request.form.getlist('cos_amount'))
        print(table_name,split_member_names,amount,expence_name,paidby,choice,cos_amount)
        
    split_an_expense(table_name,split_member_names,amount,expence_name,paidby,choice,cos_amount)
    return render_template("split_expense_result.html")



@app.route('/create_group',methods = ['GET','POST'])
def create_group():
    return render_template("create_group.html")

@app.route('/create_group_result',methods = ['GET','POST'])
def create_group_result():
    if request.method == 'POST':
        table_name = request.form['groupName']
        member_names = request.form.getlist('member[]')
        createGroup(table_name,member_names)
    return render_template("create_group_result.html")




@app.route('/genrate_bill',methods = ['GET','POST'])
def genrate_bill():
    group_names = show_group_name()
    return render_template('select_group_for_bill_set.html', groups=group_names)
    

@app.route('/select_split_choice',methods = ['GET','POST'])
def select_split_choice():
    if request.method == 'POST':
        table_name = request.form['group']
    group_name = table_name[2:len(table_name)-3]
    member_names = show_column_name(table_name[2:len(table_name)-3])
    return render_template('select_split_choice.html',members = member_names,group = group_name)


@app.route('/show_group_split', methods=['GET','POST'])
def show_group_split():
    if request.method == 'POST':
        split_type = request.form['split_type']
        table_name = request.form['group']
        member_name = request.form.get('member')

        if split_type == 'all_split' :
            results = all_bill_settlement(table_name)
            return render_template('all_split_result.html',result = results)
        else:
            results = individual_bill_settlement(table_name,member_name)
            return render_template('individual_split_result.html',result1 = results[0], result2 = results[1])

    return render_template('show_group_split.html')



if __name__ == '__main__':
    app.run()
    cursor.close()