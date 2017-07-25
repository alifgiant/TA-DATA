
if __name__ == '__main__':
    a_file = open('res.txt', 'w')
    print('something', file=a_file)
    print('something2', file=a_file)
    print('something3', file=a_file)
    a_file.close()

