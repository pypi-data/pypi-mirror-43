# 该模块写了一个类ReplaceTableData，在文件夹updatetable/updatetable.py中，主要有两个功能：

## 1。数据库中新表创建，允许的数据形式为dataframe或者是列表字典，创建的表可以没有unique_key。

    from updatetable import *
    creat_new_table = ReplaceTableData('label', 'db_name')
    creat_newtable.write_new_table('df_or_list_dict', 'table_name', dtype, 'unique_key', 'primary_key')


## 2。再不清空原有表的基础上进行表的更新，该表必须有unique_key和primary_key。

    from updatetable import *
    update_table = ReplaceTableData('label', 'db_name')
    update_table.update_table_data('df_or_list_dict', 'table_name', 'unique_key', 'primary_key')

## 3。该类同时提供了利用sql语句从数据库中查询数据的方法，可以返回列表字典，也可以返回dataframe。

    from updatetable import *
    read_data = ReplaceTableData('label', 'db_name')
    list_dict = read_data.fetchall_data("select * from table_name")
    print(list_dict) 返回的结果为查询的列表子弹

    or

    df = pd.read_sql("select * from table_name", read_data.engine_db())
    print(df) 返回的结果dataframe
