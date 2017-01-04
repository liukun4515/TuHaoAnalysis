from  analyse.Util import *
import os

if __name__ == '__main__':
    items = read_item(file_item)
    users = read_user(file_user)

    # 读取deal的数据，把所有的deal数据中的消费记录进行处理
    if os.path.exists(file_acount + npy) is False:
        users_account = get_account(file_deal, users, items)
        # 处理消费记录以后的内容存储users-acount中，写到文件，方便以后处理使用
        write_data(file_acount, users_account)
    # 把所有的圈子进行cluster，并且进行去重
    if os.path.exists(file_cluster + npy) is False:
        clusters = get_cluster(users)
        # 把set的clusters转换成list
        write_data(file_cluster, list(clusters))

    print(len(users))
    num =0
    for user in users:
        if len(user)==1:
            num = num+1
    print(num)
    # 计算每个clusters的总的消费综合，然后按照总和进行排序，
    clusters = read_data(file_cluster + npy)
    num = 0
    for i in clusters:
        if len(i)==1:
            num+=1
    print(num)

    users_account = read_data(file_acount + npy)
    all_money = list()
    for cluster in clusters:
        all = 0
        for userid in cluster:
            all = all + users_account[userid]
        all_money.append((cluster, all))
    # 按照tuple的第二个元素进行排序
    all_money.sort(key=lambda x: x[1], reverse=True)
    # 这里会有一个空的tuple内容，可以查查是如何产生的
    top100_all = 0
    for i in range(0, 100):
        top100_all += all_money[i][1]
        # print(all_money[i][1])
    print(all_money[len(all_money)-1])
    print(all_money[0])
    A = len(clusters)
    B = top100_all
    print("A:   B：  ", (A, B))