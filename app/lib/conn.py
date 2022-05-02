import sqlalchemy

class ConnectionData:
    user = 'root'
    password = 'root'         #da capire come rimuovere/aggiungere password a utente mysql
    host = 'localhost'
    port = 3306
    database = 'pcto_db'
    """ 
    @staticmethod
    def get_connection():
        return sqlalchemy.create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                ConnectionData.user, ConnectionData.password, ConnectionData.host, ConnectionData.port, ConnectionData.database
            )
        )

    @staticmethod
    def get_engine():
        try:
            engine = ConnectionData.get_connection()
            return engine

        except Exception as ex:
            print("Connection could not be made due to the following error: \n")
            print(type(ex))
            return "Connection Refused"
    """
    @staticmethod
    def get_url():
        return "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(ConnectionData.user,
                                                            ConnectionData.password,
                                                            ConnectionData.host,
                                                            ConnectionData.port,
                                                            ConnectionData.database)
