# 文件读写


def write_in_txt(mid):
    with open(r'UserMid.txt', 'a', encoding="utf-8") as file:
        file.write(str(mid))
        file.write('\n')
        file.close()


def read_from_txt():
    with open(r'UserMid.txt', 'r') as file:
        line = file.read().replace('\n', ',')
        mid_list = line.split(',')
        mid_list.pop()
        file.close()
        return mid_list


if __name__ == '__main__':
    read_from_txt()
