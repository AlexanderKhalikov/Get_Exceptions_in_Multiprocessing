from fnmatch import fnmatch
import os
from shutil import copy
from multiprocessing import Pool
import time
import logging
from datetime import datetime


logging.basicConfig(level=logging.DEBUG, filename="logfile.txt", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

directory_name = ''
directory_to_write = ''


time_format = '%y/%m/%d %H:%M:%S'
start_time = '28/05/28 09:52:26'
end_time = '28/05/28 09:52:28'


def process_file(file):

    file_time_created = time.strftime(time_format, time.gmtime(os.path.getmtime(directory_name + file)))

    datetime_object = datetime.strptime(file_time_created, time_format)
    if datetime.strptime(start_time, time_format) < datetime_object < datetime.strptime(end_time, time_format):
        return

    if fnmatch(file, '*Response.txt'):
        filename = directory_name + file
        try:
            with open(filename, 'r', encoding='utf-8') as myfile:
                data = myfile.read()
                if data.find('xception') != -1:
                    try:
                        requestFile = directory_name + file.replace('Response', 'Request')
                        responseFile = directory_name + file
                        try:
                            copy(requestFile, directory_to_write)
                            copy(responseFile, directory_to_write)
                        except Exception as e:
                            logging.info('Error 1')
                            logging.info(str(e) + '\n')
                            print(str(e))
                    except FileNotFoundError:
                        logging.info('Error 2')
                        print('no such file - ', requestFile)
                        logging.info('no such file - ' + str(requestFile) + '\n')
        except UnicodeDecodeError:
            logging.info('Error 3')
            print('error unicode decode -', filename)
            logging.info('error unicode decode -' + str(filename) + '\n')


if __name__ == '__main__':
    logging.info('\n')
    try:
        number_of_processes = 50
        # pool = Pool(os.cpu_count())  # Create a multiprocessing Pool

        logging.info('Number of processes - ' + str(number_of_processes))
        logging.info('Directory to scan ' + directory_name)

        pool = Pool(number_of_processes)

        start_time = time.time()

        pool.map(process_file, os.listdir(directory_name))

        pool.close()
        elapsed_time = time.time() - start_time

        logging.info('Elapsed time in sec - ' + str(elapsed_time))
        logging.info('Elapsed time in min - ' + str(elapsed_time / 60))
        logging.info('Number of scanned files - ' + str(len(os.listdir(directory_name))))
    except Exception as a:
        logging.info('Error 0')
        logging.info(str(a) + '\n')

        print()
        print()

