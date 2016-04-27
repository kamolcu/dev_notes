# -*- coding: utf-8 -*-
import sys
import xlrd
from xlrd.sheet import ctype_text
import random
import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects import mysql

engine = create_engine(
    'mysql://root:1q2w3e4r@127.0.0.1/pcms?charset=utf8', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

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

def build_key(sheet, row_idx, col_idx):
    key = ''
    for col in range(0, col_idx + 1):
        key += sheet.cell(row_idx, col).value.strip()
    return key

if __name__ == '__main__':
    # Open the workbook
    fname = 'slug_cat_tree.xlsx'
    xl_workbook = xlrd.open_workbook(fname)
    slug_sheet = xl_workbook.sheet_by_name('SLUG')
    print 'Total row count = %s. Start processing ...' % slug_sheet.nrows
    row_counter = 0
    for row_idx in range(1, slug_sheet.nrows):
        row_counter += 1
        slug = slug_sheet.cell(row_idx, 0).value
        pkey = slug_sheet.cell(row_idx, 1).value
        #print 'row=%s,pkey=%s, slug=%s' % (row_counter, pkey, slug)
        session.query(Collection).filter(Collection.pkey == pkey).update({"slug": slug})
        session.commit()
        #today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        #col = save_col(pkey, slug, today)
