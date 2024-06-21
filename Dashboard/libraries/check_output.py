import os

def check_score():
    folder_dir = os.getcwd() + '/Dashboard/results'
    files = os.listdir(folder_dir)
    file = [f for f in files if 'score' in f]

    if file:
        return True
    else:
        return False