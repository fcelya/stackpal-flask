# from app import db

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

# class Optimization(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     code_in = db.Column(db.String(2000),nullable=False)
    # code_out
    # prompt_system_used
    # tokens_prompt
    # tokens_response
    # tokens_total
    # model
