from analyse import *


def read_item(file):
    begin_time = time.time()
    items = list()
    for item in open(file):
        datas = item.strip().split(" ")
        items.append(int(datas[1]))
    print("读取文件%s,一共%d数据,使用时间为%d s" % (str(file), len(items), time.time() - begin_time))
    return items


def read_user(file):
    begin_time = time.time()
    users = list()
    for user in open(file):
        datas = user.strip().split(" ")
        one_user = list()
        one_user.append(int(datas[0]))
        for i in range(2, 2 + int(datas[1])):
            one_user.append(int(datas[i]))
        users.append(one_user)
    print("读取文件%s,一共%d数据,使用时间为%d s" % (str(file), len(users), time.time() - begin_time))
    return users


def get_account(file, users, items):
    begin_time = time.time()
    user_account = [0] * len(users)
    j = 0
    for account in open(file):
        j = j + 1
        if j % 100000 == 0:
            print("处理了%d 十万条数据" % (j / 100000))
        datas = account.strip().split(" ")
        one_deal_amount = 0
        # 计算这条购物记录使用的费用为
        for i in range(2, 2 + int(datas[1]) * 2, 2):
            one_deal_amount = one_deal_amount + items[int(datas[i])] * int(datas[i + 1])
        # 把这个记录的购物费用加入到当前的任务使用的费用
        user_account[int(datas[0])] = user_account[int(datas[0])] + one_deal_amount
    print("读取文件%s，一共%d数据，使用时间为%d s" % (str(file), len(user_account), time.time() - begin_time))
    return user_account


def get_cluster(users):
    '''
    对user的圈子进行聚类。把一个人的朋友的朋友聚成一个，并且把相同的类型的数据值添加一次
    其中返回的是一个set，每一个数据是一个tuple，tuple中的数据保证都是唯一的。
    '''
    clusters = set()
    for user in users:
        one_cluster = set()
        one_cluster = one_cluster.union(set(user))

        for id in user:
            one_cluster = one_cluster.union(set(users[id]))
        one_cluster = list(one_cluster)
        one_cluster.sort()
        # one_cluster = set(one_cluster)
        clusters.add(tuple(one_cluster))
    print("发现cluster的个数为:%d" % len(clusters))

    return clusters


def write_data(file, user_account):
    np.save(file, np.array(user_account))


def read_data(file):
    return np.load(file)


# just for test the cluster function
if __name__ == '__main__':
    '''
    这个是一个测试方法，测试按照这种user的情况下，对应的cluster的数目和内容是否正确
    '''
    user0 = [0, 1]
    user1 = [1, 2, 0]
    user2 = [2, 3, 1]
    user3 = [3, 2]
    user4 = [4]
    user = []
    user.append(user0)
    user.append(user1)
    user.append(user2)
    user.append(user3)
    user.append(user4)
    clusters = get_cluster(user)
    print(clusters)
