import mysql.connector
try:
    mydb = mysql.connector.connect(host = "localhost", user="root", passwd="1234", database="library_management")
    mycursor = mydb.cursor();
    ans ='Y'
    print("Enter your name");
    std_name =  input().upper();
    print("Enter your Id");
    std_id = input().upper();
    while(ans == "Y"):
        print("Issue or Renewal or Return")
        req = input().upper();
        if (req.upper() == "ISSUE"):
            print("Please mention subject of the book")
            sub = str(input().upper())
            print("Please select the author from the list below:")
            query = "Select b_name from book where subject=%s"
            mycursor.execute(query,(sub,))
            res = mycursor.fetchall();
            for row in res:
               strin =str(row)
               print(strin[2:(len(strin)-3)])
            print("Name of book to be issued")
            b_name = input().upper();
            query1 = "select count from book where b_name = %s and subject =%s"
            res = mycursor.execute(query1,(b_name,sub,))
            res1 =str(mycursor.fetchall());
            r_count = res1[2:3]
            #print(r_count)
            new_count = int(r_count)
            #print(r_count)

            if (new_count>0):
                query2 = "update book set count = count-1 where b_name =%s and subject =%s"
                mycursor.execute(query2,(b_name,sub,))
                mydb.commit();
                query7 = "Select date(date_add(sysdate(),Interval 14 day)) from dual"
                mycursor.execute(query7)
                return_date=str(mycursor.fetchone())
                date = return_date[15:27]
                print("Issued %s book author:%s by %s.Kindly return by %s"%(sub,b_name,std_name,date))
                query3 ="insert into student(std_name,issue_date,return_date,bauthor,subject,id) values(%s,sysdate(),date_add(sysdate(),interval 14 day),%s,%s,%s)"
                mycursor.execute(query3,(std_name,b_name,sub,std_id,))
                mydb.commit();
            else:
                print("Book not available")
            print("CONTINUE? Y/N")
            ans =input().upper().upper()
        #-----------------------------Renewal
        elif (req.upper() == "RENEWAL"):
            print("Please mention subject of the book to be renewed")
            sub = str(input().upper())
            print("Following are the books that you have issued")
            query8 = "select distinct(bauthor) from student where subject = %s  and id = %s"
            mycursor.execute(query8, (sub, std_id,))
            res3 = mycursor.fetchall();
            for row in res3:
                res4 = str(row);
                print(res4[2:(len(res4) - 3)])

            print("Please enter the author of the book")
            b_name = input().upper();
            query4 = "select count(*) from student where id=%s and bauthor=%s and subject=%s"
            mycursor.execute(query4, (std_id, b_name, sub,))
            res = str(mycursor.fetchall());
            count = res[2:3]
            # print(res[2:3])
            new_count = int(count)
            if new_count == 2:
                print("Book cannot be renewed more than two times.Kindly return the book")
            elif new_count == 0:
                print("Kindly issue the book first")
            else:
                query5 = "insert into student(std_name,issue_date,return_date,bauthor,subject,id) values(%s,sysdate(),date_add(sysdate(),interval 14 day),%s,%s,%s)"
                mycursor.execute(query5, (std_name, b_name, sub, std_id,))
                mydb.commit();
                query6 = "select date(date_add(sysdate(),interval 14 day)) from dual"
                mycursor.execute(query6);
                return_date = str(mycursor.fetchone());
                date = return_date[15:27]
                print("You have successfully renewed %s book(Author:%s).Kindly return it by %s" % (sub, b_name, date))
                print("CONTINUE? Y/N")
                ans = input().upper().upper()
        elif(req.upper() == "RETURN"):
            print("Please mention subject of the book to be renewed")
            sub = str(input().upper())
            print("Please enter the author of the book")
            b_name = input().upper();
            query6="Update book set count=count+1 where b_name=%s and subject=%s"
            mycursor.execute(query6,(b_name,sub))
            mydb.commit();
            print("Book return Successful")
            print("CONTINUE? Y/N")
            ans = input().upper()
        else:
            print("Invalid option")
            print("CONTINUE? Y/N")
            ans = input().upper()

except :
    print("Please select correct options")












