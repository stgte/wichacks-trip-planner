from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, searchForm
from anytree import Node, RenderTree
from math import inf
import csv


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    origins = ("NYC", "Miami")
    form.origin.choices = [("1","NYC"),("2","Miami")]
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = searchForm()
    origins = ["NYC","Miami"]
    form.origin.choices = [("1","NYC")]
    form.destination.choices=[("1","NYC"),("2","Miami"),("3","Albany"),("4","Ithaca"),("5","Rochester")]
    if form.validate_on_submit():
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, form.remember_me.data))
        return redirect(url_for('next'))
    return render_template('search.html',  title='Sign In', form=form)

# @app.route('/next', methods=['GET', 'POST'])
# def next():
#     pos = []
#     root = Node(["NYC", 0.0])
#     node1 = Node(["Albany", 39], parent=root)
#     node2 = Node(["Miami", 40], parent=root)
#     node3 = Node(["Miami", 18], parent=node1)
#     node4 = Node(["Albany", 12], parent=node2)
#     node5 = Node(["NYC", 11], parent=node3)
#     node6 = Node(["NYC", 19], parent=node4)
#     pos.append(node5)
#     pos.append(node6)
#     route = node5
#     cheaper = inf
#     for x in pos:
#         total = 0
#         path = str(x)
#         res = [i for i in range(len(path)) if path.startswith(', ', i)]
#         for i in res:
#             total += float(path[i + 2:i + 4])
#         if total < cheaper:
#             route = x
#             cheaper = total
#         # print(total)
#     # print(route)
#     total= '$'+str(total)
#
#     return render_template('next.html', title='Plan', route=str(route), total=total)

def find_next(results,next,origin, pos):
    # next = ''
    add = ''
    min = inf
    for x in results:
        if x[0]==origin:
            if min>float(x[pos]) and x[1] not in next:
                min = float(x[pos])
                add = x[1]
                print(add)
    next.append(add)
    return next, min

def csv_tolist():
    results = []
    with open("app/idk.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')  # change contents to floats
        for row in reader:  # each row is a list
            results.append(row)
    return results

@app.route('/next', methods=['GET', 'POST'])
def next():
    route = []
    total = 0
    results=csv_tolist()
    route.append("NYC")
    for x in range(4):
        route, num=find_next(results, route, route[x], x+2)
        total +=num

    for x in results:
        if x[1]=="NYC" and x[0]==route[-1]:
            route.append("NYC")
            total+=float(x[6])

    return render_template('next.html', title='Plan', route=str(route), total=total)
