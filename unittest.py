from app.models import User, Role, Post
from app import db
import unittest


class FlaskClientTestCase(unittest.TestCase):

    def test_db_init(self):
        pass

    @staticmethod
    def test_make_role():
        user_role = Role(name='User')
        admin_role = Role(name='Administrator')
        moder_role = Role(name='Moderator')
        db.session.add_all([admin_role, moder_role, user_role])
        db.session.commit()

    def test_roles(self):
    	pass
        # self.assertTrue(Role.query.filter_by(name='Adminstrator').)


if __name__ == '__main__':
    FlaskClientTestCase.test_make_role()
