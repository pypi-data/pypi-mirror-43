# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 20:55:26 2017

@author: Young Ju Kim
"""

import pandas as pd
from datetime import datetime

import psycopg2 as pg
import sqlalchemy as sa
#import ibm_db
import ibm_db_sa
import cx_Oracle as co
import pymysql

from unipy.utils.wrapper import time_profiler


__all__ = ['from_OracleSQL',
           'from_OracleSQL_async']


@time_profiler
def from_OracleSQL(query, h=None, port=None, db=None, u=None, p=None):

    print('Using OracleDB')

    # DB Connection
    dnsStr = co.makedsn(h, str(port), db)
    dnsStr = dnsStr.replace('SID', 'SERVICE_NAME')
    conn = co.connect(u, p, dnsStr)

    # Get a DataFrame
    query_result = pd.read_sql(query, conn)

    # Close Connection
    conn.close()

    return query_result


@time_profiler
async def from_OracleSQL_async(query, h=None, port=None, db=None, u=None, p=None):

    print('Using OracleDB')

    # DB Connection
    dnsStr = co.makedsn(h, str(port), db)
    dnsStr = dnsStr.replace('SID', 'SERVICE_NAME')
    conn = co.connect(u, p, dnsStr)

    # Get a DataFrame
    await pd.read_sql(query, conn)

    # Close Connection
    conn.close()

    #return query_result


if __name__ == '__main__':

    async def DBFunc(query):
        print('Connecting to DB : ')
        await from_OracleSQL_async(query)
