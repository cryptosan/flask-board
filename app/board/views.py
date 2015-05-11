from flask import Blueprint, render_template

board = Blueprint('board', __name__, template_folder='templates')

@board.route('/')
@board.route('/index')
def board_index():
	pass