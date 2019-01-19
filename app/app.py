import logging
import os
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
try:
    import api

    if __name__ == "__main__":
        print('Create')
        app = api.create_app()
        app.run(debug=True)
        print('Run done') 
except Exception as ex:
    logging.error('Failed start: '+ str(e))
    