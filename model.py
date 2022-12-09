"""Models for melon tasting appointment app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    username = db.Column(db.String, primary_key=True)

    reservations = db.relationship("Reservation", back_populates="user")
    
    def __repr__(self):

        return f"<User username={self.username}>"
    

    @classmethod
    def create(cls, username):
       """Create and return a new user."""

       return cls(username=username)

    
    @classmethod
    def get_by_id(cls, username):
        return cls.query.get(username)

    

class Reservation(db.Model):
    """A reservation."""

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False) 
    start_time = db.Column(db.Time, nullable=False)
    end_time =  db.Column(db.Time, nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)

    user = db.relationship("User", back_populates="reservations")

    def __repr__(self):

        return f"<Reservation reservation_id={self.reservation_id} username={self.username} date={self.date}>"
    

    @classmethod
    def create(cls, user, date, start_time, end_time):
        """Create and return a new reservation."""

        return cls(user=user, date=date, start_time=start_time, end_time=end_time)
    

    @classmethod
    def get_reservations_by_username(cls, username):
        """Return a list of reservations by username."""

        return cls.query.filter(Reservation.username == username).all()
    

    # check if this is right...
    # @classmethod
    # def get_reservation_by_id(cls, reservation_id):
    #     """Return a reservation by id, returns None if not found."""

    #     return cls.query.get(reservation_id)
    

    @classmethod
    def get_reservation_by_date(cls, date):
        """Return a reservation by date, returns None if not found."""

        return cls.query.filter(Reservation.date == date).all()


    
    
def connect_to_db(flask_app, db_uri="postgresql:///melon_tastings_db", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

    

if __name__ == "__main__":
    from server import app

    connect_to_db(app)