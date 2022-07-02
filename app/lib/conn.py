#Connessione al database
class ConnectionData:
    user = 'root'
    password = ''
    host = 'localhost'
    port = 3306
    database = 'pcto_db'

    @staticmethod
    def get_url():
        return "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(ConnectionData.user,
                                                            ConnectionData.password,
                                                            ConnectionData.host,
                                                            ConnectionData.port,
                                                            ConnectionData.database)
