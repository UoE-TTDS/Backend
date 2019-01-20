import logging
import os
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
try:
    import api

    if __name__ == "__main__": 
        app = api.create_app()
        #app.run(host='0.0.0.0') 
except Exception as ex:
    logging.error('Failed start: '+ str(e))
