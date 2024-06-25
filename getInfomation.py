import pandas as pd

def load_data():
    information = pd.read_csv('./csv_file/information.csv')
    return information

def get_parent(studentName):
    information = load_data()
    if len(information[information["student"]==studentName]["parents"]) > 0:
        return str(information[information["student"]==studentName]["parents"][0])
    return None


if __name__ == '__main__':
    get_parent("丞嘉")