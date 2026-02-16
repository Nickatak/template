try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    # MySQL driver is optional unless DATABASE_URL uses mysql://
    pass
