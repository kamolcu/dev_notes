# -*- coding: utf-8 -*-
import datetime
import json

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects import mysql

engine = create_engine(
    'mysql://root:root@docker-pcms.itruemart-local.com/pcms_db?charset=utf8', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Promotion(Base):
    __tablename__ = 'promotions'
    id = Column(Integer, primary_key=True)
    pkey = Column(String(255))
    effects = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    pkey = Column(Integer)
    name = Column(String(200))
    slug = Column(String(50))
    is_category = Column(mysql.ENUM('0', '1'))
    pds_collection = Column(mysql.ENUM('0', '1', '2'))  # 1 = col, 2 = cat
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # deleted_at = Column(DateTime) - Leave default - NULL


def get_children_pkeys(col_pkey):
    output_list = []
    col = session.query(Collection).filter(Collection.pkey == col_pkey).first()
    children = session.query(Collection).filter(
        Collection.parent_id == col.id).add_column(Collection.pkey)
    for child in children:
        output_list.append(child.pkey)

    for child in children:
        output_list += get_children_pkeys(child.pkey)

    return output_list

if __name__ == '__main__':

    cols = [3215522978465, 3856986467976, 3906905110670]
    cols = [3856986467976]
    pkey = 20777369033125
    promotion = session.query(Promotion).filter(Promotion.pkey == pkey).first()
    print 'b4 = %s' % promotion.effects
    target_json = json.loads(promotion.effects)
    existing_list = target_json['discount']['following_items']

    target_col_list = []
    for col in cols:
        children = get_children_pkeys(col)
        target_col_list += children

    new_list = existing_list + target_col_list
    target_json['discount']['following_items'] = new_list

    effects = json.dumps(target_json)
    print 'after = %s' % effects
