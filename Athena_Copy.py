# -*- coding: utf-8 -*-
from pyathena import connect
from pprint import pprint

def get_list(query_list):
    val_list=[]
    for data in query_list:
        val_list.extend([data[0]])
    
    return val_list
def get_input_val(input_type):
    while True:
        input_val=input(input_type+" 입력하세요: ")
        if(input_val != ''):
            return input_val
        print("공백입력은 안됩니다. 다시 입력해주세요.")

def getRemoveList(source_list):

    for element in source_list:
        print(element)
    remove_list=[]
    print("제외할 값을 입력해주세요.")
    print("더 이상 입력하지 않으시려면 QUIT_ 를 입력해주세요.")
    while True:
        check_flag=0
        input_val=input("제외할 리스트 입력: ")

        if(input_val == "QUIT_"):
            return remove_list

        for database in source_list:
            if(database == input_val):
                check_flag=1
                remove_list.extend([input_val])
        
        if(check_flag==0):
            print("리스트에 없는 값을 입력하였습니다.")



def getChangeWord():

    change_word_list=[]

    while True:
        print("변경전값과 변경될값을 입력해주세요. ")
        print("종료를 원하시면 변경전값에 QUIT_ 입력")
        print("변경 초기화를 원하시면 변경전값에 AGAIN_ 입력")
        while True:
            old_str=str(get_input_val("변경전값:"))
            if(old_str == "QUIT_"):
                #print(change_word_list)
                #print(len(change_word_list))
                return change_word_list
            elif(old_str == "AGAIN_"):
                print("이전 입력값은 모두 삭제 됩니다.")
                change_word_list.clear()
                change_word_list = []
                continue
            new_str=str(get_input_val("변경될값:"))
            print("###################################################################")
            change_word_list.extend([[old_str,new_str]])
            #print(len(change_word_list))
def get_change_schemalist(change_word_list,source_schema_list):
    change_schemalist=[]
    for schema in source_schema_list:
        old_schema=schema
        new_schema=old_schema
        for change_word in change_word_list:
            new_schema=new_schema.replace(change_word[0], change_word[1])
        if(old_schema != new_schema):
            change_schemalist.extend([[old_schema,new_schema]])
    return change_schemalist

def replaceInList(asis_list, change_word_list):
    tobe_list=[]
    for element in asis_list:
        tobe_element=element
        for(old, newstr) in change_word_list:
            tobe_element=tobe_element.replace(old, newstr)
        
        tobe_list.extend([tobe_element])

    return tobe_list
def replaceWord(str,change_word_list):
    new_str=str
    for (old, newstr) in change_word_list:
        new_str=new_str.replace(old,newstr)
    return new_str


def InputNumber(min_number,max_number):
    while True:
        try:
            number = int(input("숫자를 입력하세요: "))
            if(number >=min_number and number <= max_number):
                return number
            
            print(str(min_number)+"~"+str(max_number)+"까지 입력")
        except Exception as ex:
            continue

def MainMenu():
    print("###################################################################")
    print("  1. database 전체 COPY")
    print("  2. TABLE COPY")

    input_val = InputNumber(1,2)
    print("###################################################################")
    return input_val

def getDatabase(database_list):
    for database in database_list:
        print(database)
    while True:
        input_val=input("선택할 database 입력: ")

        for database in database_list:
            if(database == input_val):
                return input_val
        
        print("database에 없는 값을 입력하였습니다.")

def parseTableDdl(table_ddl):
    find_query="\nWITH SERDEPROPERTIES ( \n  'escape.delim'='\\\\') \n"
    find_query2="  LINES TERMINATED BY '\\n' \n  ESCAPED BY '\\\\' \n"
    parse_table_ddl=[]
    print(table_ddl)
    for ddl in table_ddl:
        new_ddl=""
        for line in ddl.split("\n"):
            
            if("COMMENT" in line and line[-1] == ')' ):
                #print(line[1:line.find("COMMENT")] + line[-1:])
                new_ddl=new_ddl + line[1:line.find("COMMENT")-1] + line[-1:] + "\n"
            elif("COMMENT" in line and line[-2] == ')' ):
                #print(line[1:line.find("COMMENT")] + line[-1:])
                new_ddl=new_ddl + line[1:line.find("COMMENT")-1] + line[-2:] + "\n"
            elif("COMMENT" in line and line[-1] == ',' ):
                #print(line[1:line.find("COMMENT")] + line[-2:])
                new_ddl=new_ddl + line[1:line.find("COMMENT")-1] + line[-1:] + "\n"
            elif("COMMENT" in line and line[-2] == ','):
                new_ddl=new_ddl + line[1:line.find("COMMENT")-1] + line[-2:] + "\n"
            elif("COMMENT" in line):
                new_ddl=new_ddl + line[1:line.find("COMMENT")-1] + ", \n"
            else :
                #print(line)
                new_ddl=new_ddl+line+"\n"
            
        new_ddl = new_ddl.replace(find_query,"\n  ESCAPED BY '\\\\' \n")

        new_ddl = new_ddl.replace(find_query2,"  ESCAPED BY '\\\\' \n  LINES TERMINATED BY '\\n' \n")
        print(new_ddl)
        parse_table_ddl.extend([new_ddl])
    return parse_table_ddl

def inputConnectInfo():
    print("다시 입력은 AGAIN_")
    '''
    input_list=["Source aws_access_key_id",
                "Source aws_secret_access_key",
                "Source s3_staging_dir",
                "Source region_name",
                "Target aws_access_key_id",
                "Target aws_secret_access_key",
                "Target s3_staging_dir",
                "Target region_name"]
    '''
    input_list=["Source profile_name",
                #"Source region_name",
                "Source s3_staging_dir",
                "Target profile_name",
                #"Target region_name",
                "Target s3_staging_dir"]
    i=0
    connect_info={}
    while i < len(input_list) :
        input_val=get_input_val(input_list[i])
        if(input_val=="AGAIN_"):
            i=0
            continue
        connect_info[input_list[i]] = input_val
        i=i+1
    
    return connect_info








if __name__=='__main__':

    connect_info=inputConnectInfo()
    print(connect_info)

    source_cursor = connect(profile_name=connect_info["Source profile_name"],region_name='ap-northeast-2',s3_staging_dir=connect_info["Source s3_staging_dir"]).cursor()
    target_cursor = connect(profile_name=connect_info["Target profile_name"],region_name='ap-northeast-2',s3_staging_dir=connect_info["Target s3_staging_dir"]).cursor()
    
    '''
    source_cursor = connect(aws_access_key_id=connect_info['Source aws_access_key_id'],
                     aws_secret_access_key=connect_info['Source aws_secret_access_key'],
                     s3_staging_dir=connect_info['Source s3_staging_dir'],
                     region_name=connect_info['Source region_name']).cursor()

    target_cursor = connect(aws_access_key_id=connect_info['Target aws_access_key_id'],
                     aws_secret_access_key=connect_info['Target aws_secret_access_key'],
                     s3_staging_dir=connect_info['Target s3_staging_dir'],
                     region_name=connect_info['Target region_name']).cursor()
    '''
    
    source_cursor.execute("show databases")
    source_database_list=get_list(source_cursor.fetchall())
    menu_number=MainMenu()
    
    source_table_list={}
    database_ddl=[]
    table_ddl=[]
    new_table_ddl=[]
    if(menu_number==1):#Database 전체 Copy
           
        
        remove_list=getRemoveList(source_database_list)
        remove_list.extend(['default'])

        for remove_database in  remove_list:
            source_database_list.remove(remove_database)

        change_word_list=getChangeWord()

        for database in source_database_list:
            
            database_ddl.extend(["CREATE DATABASE IF NOT EXISTS " + database])
            source_cursor.execute("show tables in "+ database)
            table_list=get_list(source_cursor.fetchall())
            for table in table_list:
                source_cursor.execute("show create table "+database + "." + table)
                ddl_query_result=get_list(source_cursor.fetchall())
                ddl_scripts=""
                new_ddl_scripts=""
                for ddl in ddl_query_result:
                    new_ddl=ddl
                    ddl_scripts=ddl_scripts + ddl + '\n'

                    if("CREATE EXTERNAL TABLE" in new_ddl or "'s3:" in new_ddl):
                        new_ddl=replaceWord(new_ddl,change_word_list)

                    new_ddl_scripts=new_ddl_scripts + new_ddl + '\n'
                table_ddl.extend([ddl_scripts])
                new_table_ddl.extend([new_ddl_scripts])
        
        
        change_word_list=get_change_schemalist(change_word_list,source_database_list)
        new_database_ddl=replaceInList(database_ddl,change_word_list)
        #new_table_ddl=replaceInList(table_ddl,change_word_list)

        for ddl_script in new_database_ddl:
            print(ddl_script)

        input("실행")

        for ddl_script in new_database_ddl:
            target_cursor.execute(ddl_script)
        new_table_ddl=parseTableDdl(new_table_ddl)
        for ddl_script in new_table_ddl:
            try:
                print(ddl_script)
                #input("실행")
                target_cursor.execute(ddl_script)
            except Exception as ex:
                
                print(ex)

    elif(menu_number == 2):#Table Copy
        mig_database=getDatabase(source_database_list)
        source_cursor.execute("show tables in "+ mig_database)
        table_list=get_list(source_cursor.fetchall())
        remove_table_list=getRemoveList(table_list)
        
        if(len(remove_table_list) >= 1):
            for remove_table in  remove_table_list:
                table_list.remove(remove_table)

        change_word_list=getChangeWord()

        for table in table_list:
            source_cursor.execute("show create table "+mig_database + "." + table)
            ddl_query_result=get_list(source_cursor.fetchall())
            ddl_scripts=""
            new_ddl_scripts=""
            for ddl in ddl_query_result:
                new_ddl=ddl
                ddl_scripts=ddl_scripts + ddl + '\n'

                if("CREATE EXTERNAL TABLE" in new_ddl or "'s3:" in new_ddl):
                    new_ddl=replaceWord(new_ddl,change_word_list)
                new_ddl_scripts=new_ddl_scripts + new_ddl + '\n'
            table_ddl.extend([ddl_scripts])
            new_table_ddl.extend([new_ddl_scripts])
        
        
        #temp_mig_database=[mig_database]
        #change_word_list=get_change_schemalist(change_word_list,temp_mig_database)
        new_table_ddl=replaceInList(table_ddl,change_word_list)


        for ddl_script in new_table_ddl:
            print(ddl_script)
        
        new_table_ddl=parseTableDdl(new_table_ddl)
        input("실행")
        for ddl_script in new_table_ddl:
            try:
                target_cursor.execute(ddl_script)
            except Exception as ex:
                print(ex)

    #target_cursor.execute("show databases")
    #target_database_list=get_list(target_cursor.fetchall())
    #print(target_database_list)