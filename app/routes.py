from flask import Flask, render_template, redirect, Blueprint
from app.models import db, Item

main = Blueprint('main', __name__)

@main.route('/')
def land():
    users = Item.query.all()
    return render_template('home.html', users=users)

@main.route('/about/<username>')
def about(username):
    users = [
        {'id':1, 'name' : 'Roal', 'email':'Royal@abcd.in' },
        {'id':2, 'name' : 'Royl', 'email':'Royal@acd.in' },
        {'id':3, 'name' : 'Royal', 'email':'Royal@abd.in' }
    ]
    return render_template('about.html', name = username, users=users)

@main.route('/page1')
def page1():
    return render_template('page1.html')
