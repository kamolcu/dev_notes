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


class AppsCollections(Base):
    __tablename__ = 'apps_collections'
    __table_args__ = (
        PrimaryKeyConstraint('collection_id', 'app_id'),
    )
    collection_id = Column(Integer)
    app_id = Column(Integer)


class Translate(Base):
    __tablename__ = 'translates'
    id = Column(Integer, primary_key=True)
    locale = Column(String(10))
    languagable_id = Column(Integer)  # instance id
    languagable_type = Column(String(20))  # 'Collection'
    #text = Column(String(255))
    #title = Column(String(255))
    name = Column(String(255))  # EN name
    #description = Column(String(1024))
    #key_feature = Column(String(1024))
    #body = Column(String(1024))
    #nit_type = Column(String(1024))
    #caption = Column(String(1024))
    #dventage = Column(String(1024))


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


def save_col(parent_id, today, th_val, slug):
    col = Collection(parent_id=parent_id, pkey=gen_pkey(),
                     name=th_val, is_category='0', pds_collection='2', created_at=today, updated_at=today, slug=slug)
    session.add(col)
    session.commit()
    return col

def save_translate(name, col_id):
    translate_instance = Translate(locale='en_US', languagable_id=col_id, languagable_type='Collection',name=name)
    session.add(translate_instance)
    session.commit()

def save_app_col_relation(col_id):
    # app_id = 1 is iTruemart
    link = AppsCollections(collection_id=col_id, app_id=1)
    session.add(link)
    session.commit()


def gen_pkey():
    return '3%s%s%s%s%s' % (random.randint(10, 99), random.randint(100, 999), random.randint(10, 99), random.randint(10, 99), random.randint(100, 999))


def build_key(sheet, row_idx, col_idx):
    key = ''
    for col in range(0, col_idx + 1):
        key += sheet.cell(row_idx, col).value.strip()
    return key

if __name__ == '__main__':
    # Open the workbook
    fname = 'cat_tree.xlsx'
    xl_workbook = xlrd.open_workbook(fname)
    th_sheet = xl_workbook.sheet_by_name('THAI')
    en_sheet = xl_workbook.sheet_by_name('ENG')
    slug_sheet = xl_workbook.sheet_by_name('SLUG')
    if(th_sheet.nrows != en_sheet.nrows):
        err = 'Total row count not equal Thai = %s, Eng = %s.' % (
            th_sheet.nrows, en_sheet.nrows)
        sys.exit(err)
    print 'Total row count = %s. Start processing ...' % th_sheet.nrows
    num_cols = th_sheet.ncols
    row_counter = 0
    key_list = []
    key_map = {}
    last_saved_level = 0
    for row_idx in range(1, th_sheet.nrows):
        row_counter += 1
        slug = slug_sheet.cell(row_idx, 0).value
        if(slug != ''):
            slug = str(slug).strip()
        else:
            slug = None
        print 'row=%s, slug=%s' % (row_counter, slug)
        for col_idx in range(0, num_cols):
            th_cell_obj = th_sheet.cell(row_idx, col_idx)
            en_cell_obj = en_sheet.cell(row_idx, col_idx)
            th_val = th_cell_obj.value.strip()
            en_val = en_cell_obj.value.strip()

            if(th_val != '' and en_val != ''):
                # print '%s %s %s %s' % (row_counter, col_idx, th_val, en_val)
                doc_key = build_key(en_sheet, row_idx, col_idx)
                # print doc_key
                if (doc_key not in key_list) and (doc_key != ''):
                    saved_level = col_idx + 1
                    # proceed save
                    if(col_idx == 0):
                        parent_id = 0
                    else:
                        if(last_saved_level >= saved_level):
                            prev_doc_key = build_key(
                                en_sheet, row_idx, col_idx - 1)
                            parent_id = key_map[prev_doc_key]

                    key_list.append(doc_key)
                    #print 'parent_id=%s' % parent_id

                    today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    # Create collection as category
                    col = save_col(parent_id, today, th_val, slug)
                    # Create apps_collections
                    save_app_col_relation(col.id)
                    # Create translate
                    save_translate(en_val, col.id)

                    latest_col = col.id
                    print 'saved_level=%s, latest_collection_id=%s' % (saved_level, latest_col)
                    key_map[doc_key] = latest_col
                    parent_id = latest_col
                    if(last_saved_level != saved_level):
                        last_saved_level = saved_level

            else:
                if(th_val == '' and en_val == ''):
                    continue
                err = 'Row[%s] TH and EN conflicts.' % (row_idx + 1)
                sys.exit(err)
