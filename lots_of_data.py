#!/usr/bin/env python2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database_setup import Base, Category, User, Item

engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_to_database(data):
    session.add(data)
    session.commit()


soccer = Category(name="Soccer")
add_to_database(soccer)
basketball = Category(name="Basketball")
add_to_database(basketball)
baseball = Category(name="Baseball")
add_to_database(baseball)
badminton = Category(name="Badminton")
add_to_database(badminton)
snowboarding = Category(name="Snowbaording")
add_to_database(snowboarding)
frisbee = Category(name="Frisbee")
add_to_database(frisbee)
football = Category(name="Football")
add_to_database(football)
skating = Category(name="Skating")
add_to_database(skating)
hockey = Category(name="Hockey")
add_to_database(hockey)

user1 = User(name="Mike", email="mike@test.com")
add_to_database(user1)
user2 = User(name="Marry", email="marry@test.com")
add_to_database(user2)


items = [Item(
    name="Stick",
    description="Stick description",
    time_added=datetime.now(),
    user_id=user1.id,
    category_name=hockey.name,
)]


items.append(Item(
    name="Goggles",
    description="Goggles description",
    time_added=datetime.now(),
    user_id=user1.id,
    category_name=snowboarding.name,

))

items.append(Item(
    name="Snowboard",
    description="Snowboard description",
    time_added=datetime.now(),
    user_id=user1.id,
    category_name=snowboarding.name,
))

items.append(Item(
    name="Two shinguards",
    description="Two shinguards description",
    time_added=datetime.now(),
    user_id=user1.id,
    category_name=soccer.name,
))

items.append(Item(
    name="Shinguards",
    description="Shinguards description",
    time_added=datetime.now(),
    user_id=user1.id,
    category_name=soccer.name,
))

items.append(Item(
    name="Frisbee",
    description="Frisbee description",
    time_added=datetime.now(),
    user_id=user2.id,
    category_name=frisbee.name,
))

items.append(Item(
    name="Bat",
    description="Bat description",
    time_added=datetime.now(),
    user_id=user2.id,
    category_name=baseball.name,
))

items.append(Item(
    name="Jersey",
    description="Jersey description",
    time_added=datetime.now(),
    user_id=user2.id,
    category_name=soccer.name,
))

items.append(Item(
    name="Soccer Cleats",
    description="Soccer Cleats description",
    time_added=datetime.now(),
    user_id=user2.id,
    category_name=soccer.name,
))

for item in items:
    add_to_database(item)
