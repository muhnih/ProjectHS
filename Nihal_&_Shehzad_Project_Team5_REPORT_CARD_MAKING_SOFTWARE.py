import pickle
import os
from tabulate import tabulate
import getpass
from datetime import datetime


def admin_login():
    print('\n!!! Warning: Authorised access only !!!\n')
    global aaccess
    aaccess = False
    user = input('Enter username   :')
    pasw = getpass.getpass(prompt = 'Enter password   :')
    if user == 'admin' and pasw == 'admin':
        aaccess = True
    if aaccess:
        print('Access granted :)')
    else:
        print('\nIncorrect username or password\n')

#--------------------------------------------------------------------------------------------------------------------------------------------
#Teacher 
#--------------------------------------------------------------------------------------------------------------------------------------------
        
def teacher_login():
    print('\n!!! Warning: Authorised access only !!!\n')
    with open('Teacher_details.dat','rb') as f:
        global taccess
        taccess = False
        user = input('Enter username   :')
        pasw = getpass.getpass(prompt = 'Enter password   :')
        name = ''
        try:
            while True:
                r = pickle.load(f)
                if pasw.upper() == r[0] and r[4] == 'AVAILABLE':
                    list = r
                    tid = r[0]
                    for i in range(4):
                        name += r[1][i]
                    name += tid
        except EOFError:
            pass
        if pasw.upper() == tid and user.upper() == name:
            print('Access granted :)')
            global t_sub
            global t_div
            t_sub = list[2]
            t_div = list[3]
            taccess = True
        else:
            print('\nIncorrect username or password\n')
        f.close()

def add_teacher():
    while True:
        with open('Teacher_details.dat','ab+') as f:
            found = False
            tid1 = []
            try:
                f.seek(0)
                while True:
                    r = pickle.load(f)
                    try:
                        tid1.append(r[0])
                        found = True
                    except:
                        pass         
            except EOFError:
                pass
            if not found:
                print('\nCreating Table - Teacher\n')
                tid = '001'
            elif found:
                tid = int(max(tid1)) + 1
                tid = str(tid)
                n = len(tid)
                while n < 3:
                    tid = '0' + tid
                    n += 1
            name = input('Enter name   :')
            sub  = input('''Choose subject
E  -> English
M  -> Mathematics
P  -> Physics
C  -> Chemistry
Cs -> Computer Science
                     :''')
            if sub.upper() == 'M':
                sub = 'Mathematics'
            elif sub.upper() == 'E':
                sub = 'English'
            elif sub.upper() == 'CS':
                sub = 'Computer science'
            elif sub.upper() == 'P':
                sub = 'Physics'
            elif sub.upper() == 'C':
                sub = 'Chemistry'
            else:
                print('\n!!! No subject found with the code:',sub)
                print('!!! Please try again\n')
                break
            div1 = input('Enter division(s) taught   :')
            error = False
            for i in div1:
                if i.lower() not in 'abcdefghij, ':
                    error = True
            div  = ''
            j    = 0
            for i in div1:
                if j > 0:
                    div += ','
                div += i
                j += 1
            stat = 'AVAILABLE'
            l = [tid.upper(),name.upper(),sub.upper(),div.upper(),stat]
            if not error:
                pickle.dump(l,f)
                print('\nTeacher',tid.upper(),'was added successfully :)\n')
                ch = input('Do you want to add more teacher(s) [Y -> Yes] :')
                if ch not in 'yY':
                    break
            elif error:
                print('\n!!! Division should be between "A" and "J" !!!')
            f.close()

def update_teacher():
    while True:
        with open('Teacher_details.dat','rb') as f1:
            with open('Teacher_details1.dat','wb') as f2:
                found = False
                update = False
                error = False
                tid = input('Enter teacher id   :')
                try:
                    while True:
                        r = pickle.load(f1)
                        if r[0] == tid.upper() and r[4] == 'AVAILABLE':
                            found = True
                        if found:
                            ch = input('''\nWhat do you want to update?
1. Name
2. Subject taught
3. Division(s) taught
                    :''')
                            if ch == '1':
                                u = 'name'
                            elif ch == '2':
                                u = 'subject'
                            elif ch == '3':
                                u = 'division'
                            else:
                                print('\nPlease choose a valid option :(\n')
                                break
                            old = r[int(ch)]
                            print('\nCurrent',u,'   :',old,'\n')
                            if ch == '1' or ch == '3':
                                new = input('Enter new '+u+'   :')
                            elif ch == '2':
                                new  = input('''Choose subject
E  -> English
M  -> Mathematics
P  -> Physics
C  -> Chemistyr
Cs -> Computer Science
                     :''')
                                if new.upper() == 'M':
                                    new = 'Mathematics'
                                elif new.upper() == 'E':
                                    new = 'English'
                                elif new.upper() == 'CS':
                                    new = 'Computer science'
                                elif new.upper() == 'P':
                                    new = 'Physics'
                                elif new.upper() == 'C':
                                    new = 'Chemistry'
                                else:
                                    print('\n!!! No subject found with the code:',sub)
                                    print('!!! Please try again\n')
                                    os.remove('Teacher_details1.dat')
                                    error = True
                                    break
                            error = False
                            if ch == '3':
                                for i in new:
                                    if i.lower() not in 'abcdefghij':
                                        error = True
                                if not error:
                                    new1 = new
                                    new = ''
                                    j = 0
                                    for i in new1:
                                        if j > 0:
                                            new += ','
                                        new += i
                                        j += 1
                            r[int(ch)] = new.upper()
                        if not error:
                            update = True
                            pickle.dump(r,f2)
                        elif error:
                            print('\n!!! Division should be between "A" and "J" !!!')
                        found1 = found
                        found = False
                except EOFError:
                    pass
                f1.close()
                f2.close()
                if update:
                    print()
                    print('\n',u.upper(),'was updated successfully :)\n')
                    os.remove('Teacher_details.dat')
                    os.rename('Teacher_details1.dat','Teacher_details.dat')
                elif not found1:
                    print('\n!!! Teacher ID not found !!!\n')
                elif update == False and found1 == True:
                    print('\nSorry, an unexpected error occured :(\n')
                    os.remove('Teacher_details1.dat')

                c = input('\nDo you want to update again [Y -> Yes]   :')
                if c not in 'yY':
                    break
                    
def delete_teacher():
    with open('Teacher_details.dat','rb') as f1:
        with open('Teacher_details1.dat','wb') as f2:
            found = False
            update = False
            tid = input('Enter teacher id   :')
            try:
                while True:
                    r = pickle.load(f1)
                    if r[0] == tid.upper() and r[4] == 'AVAILABLE':
                        found = True
                        if found:
                            str = 'DELETED'
                            r[1] = str
                            r[2] = str
                            r[3] = str
                            r[4] = str
                            update = True
                    pickle.dump(r,f2)
            except EOFError:
                pass
            f1.close()
            f2.close()
            if update:
                print()
                print('\nRecord was deleted successfully :)')
                os.remove('Teacher_details.dat')
                os.rename('Teacher_details1.dat','Teacher_details.dat')
            elif found == False:
                print('\n!!! Teacher ID not found !!!\n')
            elif update == False and found == True:
                print('\nSorry, an unexpected error occured :(\n')
                c = input('Do you want to try again [Y -> Yes]   :')
                if c in 'yY':
                    delete_teacher()

def view_teacher():
    with open('Teacher_details.dat','rb') as f:
        l = [['TID','NAME','SUBJECT','DIVISION']]
        try:
            while True:
                r = pickle.load(f)
                if r[4] == 'AVAILABLE':
                    l1 = [r[0],r[1],r[2],r[3]]
                    l.append(l1)
        except EOFError:
            #tabulate returns the values in a table
            print(tabulate(l,headers = 'firstrow',tablefmt = 'fancy_grid'))
            print('End of Records')
            
#--------------------------------------------------------------------------------------------------------------------------------------------
#Student 
#--------------------------------------------------------------------------------------------------------------------------------------------

def add_student():
    while True:
        with open('Student_details.dat','ab+') as f:
            sid1 = []
            found = False
            try:
                f.seek(0)
                while True:
                    r = pickle.load(f)
                    try:
                        sid1.append(r[0])
                        found = True
                    except:
                        pass   
            except EOFError:
                pass
            if not found:
                print('\nCreating Table - Student\n')
                sid = '000001'
            elif found:
                sid = int(max(sid1)) + 1
                sid = str(sid)
                n = len(sid)
                while n < 6:
                    sid = '0' + sid
                    n += 1
            name = input('Enter name   :')
            grade= '12'
            div  = input('Enter division [A to J]  :')
            error = False
            if len(div) > 1 or div.lower() not in 'abcdefghij':
                error = True
            stat = 'AVAILABLE'
            l = [sid.upper(),name.upper(),grade,div.upper(),stat]
            if not error:
                pickle.dump(l,f)
                print('\nStudent',sid.upper(),'was added successfully :)\n')
                ch = input('Do you want to add more student(s) [Y -> Yes] :')
                if ch not in 'Yy':
                    break
            elif error:
                print('\n!!! Division should be between "A" and "J" !!!')
                ch = input('Do you want to try again [Y -> Yes]   ?')
                if ch not in 'yY':
                    break
            f.close()
                
def update_student():
    while True:
        with open('Student_details.dat','rb') as f1:
            with open('Student_details1.dat','wb') as f2:
                found = False
                update = False
                error = False
                sid = input('Enter student id   :')
                try:
                    while True:
                        r = pickle.load(f1)
                        if r[0] == sid.upper() and r[4] == 'AVAILABLE':
                            found = True
                        if found:
                            ch = input('''\nWhat do you want to update?
1. Name
2. Division
          :''')
                            if ch == '1':
                                u = 'name'
                                cc = '0'
                            elif ch == '2':
                                cc = 2
                                ch = '3'
                                u = 'division'
                            else:
                                print('Please choose a valid option :(')
                                break
                            old = r[int(ch)]
                            print('Current',u,'   :',old)
                            new = input('Enter new '+u+'   :')
                            if cc == 2:
                                if new.lower() not in 'abcdefghij':
                                    error = True
                            r[int(ch)] = new.upper()
                        if not error:
                            pickle.dump(r,f2)
                            update = True
                        elif error:
                            print('\n!!! Division should be between "A" and "J" !!!')
                        found1 = found
                        found = False
                except EOFError:
                    pass
                f1.close()
                f2.close()
                if update:
                    print()
                    print(u.upper(),'was updated successfully :)\n')
                    os.remove('Student_details.dat')
                    os.rename('Student_details1.dat','Student_details.dat')
                elif not found:
                    print('\n!!! Student ID not found !!!\n')
                elif update == False and found == True:
                    os.remove('Student_details1.dat')
                    print('\nSorry, an unexpected error occured :(\n')
                c = input('\nDo you want to update again [Y -> Yes]   :')
                if c not in 'yY':
                    break
                    

def delete_student():
    with open('Student_details.dat','rb') as f1:
        with open('Student_details1.dat','wb') as f2:
            found = False
            update = False
            sid = input('Enter student id   :')
            try:
                while True:
                    r = pickle.load(f1)
                    if r[0] == sid.upper() and r[4] == 'AVAILABLE':
                        found = True
                        if found:
                            str = 'DELETED'
                            r[1] = str
                            r[2] = str
                            r[3] = str
                            r[4] = str
                            update = True
                    pickle.dump(r,f2)
            except EOFError:
                pass
            f1.close()
            f2.close()
            if update:
                print()
                print('Record was deleted successfully :)')
                os.remove('Student_details.dat')
                os.rename('Student_details1.dat','Student_details.dat')
            elif found == False:
                print('\n!!! Student ID not found !!!\n')
            elif update == False and found == True:
                print('Sorry, an unexpected error occured :(')
                c = input('Do you want to try again [Y -> Yes]   :')
                if c in 'yY':
                    delete_student()

def view_student():
    with open('Student_details.dat','rb') as f:
        l = [['SID','NAME','GRADE','DIVISION']]
        try:
            while True:
                r = pickle.load(f)
                if r[4] == 'AVAILABLE':
                    l1 = [r[0],r[1],r[2],r[3]]
                    l.append(l1)
        except EOFError:
            print(tabulate(l,headers = 'firstrow',tablefmt = 'fancy_grid'))
            print('End of Records')

#--------------------------------------------------------------------------------------------------------------------------------------------
#Marks 
#--------------------------------------------------------------------------------------------------------------------------------------------

def addorupdate_marks():
    with open('Marks.dat','ab+') as f:
        with open('Student_details.dat','rb') as f1:
            sid = input('Enter student ID   :')
            with open('Marks.dat','rb') as f3:
                try:
                    found = False
                    while True:
                        r = pickle.load(f3)
                        if r[0] == sid.upper():
                            found = True
                            math = r[1]
                            phy  = r[2]
                            chem = r[3]
                            cs   = r[4]
                            eng  = r[5]
                except EOFError:
                    print('Loading.....')
                f3.close()
            try:
                found1 = False
                while True:
                    r = pickle.load(f1)
                    if r[0] == sid.upper() and r[4] == 'AVAILABLE':
                        found1 = True
                        st_div = r[3]
            except EOFError:
                pass
            if not found1:
                print('\n!!! No student found with the given ID !!!\n')
            f1.close()
            if found1:
                global tid
                global t_sub
                global t_div
                check = False
                if st_div in t_div:
                    check = True
                if not check:
                    print('\nSorry, you do not have access to add/remove/update marks of this student :(\n')
                if check:
                    if t_sub == 'MATHEMATICS':
                        sub = 1
                    elif t_sub == 'PHYSICS':
                        sub = 2
                    elif t_sub == 'CHEMISTRY':
                        sub = 3
                    elif t_sub == 'COMPUTER SCIENCE':
                        sub = 4
                    elif t_sub ==  'ENGLISH':
                        sub = 5
                    print('SUBJECT               : ',t_sub)
                    theory = input('Enter theory marks    [80]    : ')
                    if int(theory) > 80:
                        print('!!! Theory marks should be less than 80 !!! ')    
                    pract  = input('Enter practical marks [20]    : ')
                    if int(pract) > 20:
                        print('!!! Practical marks should be less than 20 !!! ')
                    if int(theory) < 81 and int(pract) < 21:
                        if not found:
                            if sub == 1:
                                l = [sid.upper(),[theory,pract],['0','0'],['0','0'],['0','0'],['0','0']]
                            elif sub == 2:
                                l = [sid.upper(),['0','0'],[theory,pract],['0','0'],['0','0'],['0','0']]
                            elif sub == 3:
                                l = [sid.upper(),['0','0'],['0','0'],[theory,pract],['0','0'],['0','0']]
                            elif sub == 4:
                                l = [sid.upper(),['0','0'],['0','0'],['0','0'],[theory,pract],['0','0']]
                            elif sub == 5:
                                l = [sid.upper(),['0','0'],['0','0'],['0','0'],['0','0'],[theory,pract]]
                            pickle.dump(l,f)
                        if found:
                            if sub == 1:
                                l = [sid.upper(),[theory,pract],phy,chem,cs,eng]
                            elif sub == 2:
                                l = [sid.upper(),math,[theory,pract],chem,cs,eng]
                            elif sub == 3:
                                l = [sid.upper(),math,phy,[theory,pract],cs,eng]
                            elif sub == 4:
                                l = [sid.upper(),math,phy,chem,[theory,pract],eng]
                            elif sub == 5:
                                l = [sid.upper(),math,phy,chem,cs,[theory,pract]]
                            with open('Marks.dat','rb') as f4:
                                with open('Marks1.dat','wb+') as f5:
                                    try:
                                        update = False
                                        while True:
                                            r = pickle.load(f4)
                                            if r[0] == sid.upper():
                                                update = True
                                                r = l
                                            pickle.dump(r,f5)
                                    except EOFError:
                                        pass
                                    f4.close()
                                    f5.close()
                                    if update:
                                        f.close()
                                        os.remove('Marks.dat')
                                        os.rename('Marks1.dat','Marks.dat')
                                    elif not update:
                                        os.remove('Marks1.dat')

def view_marks():
    with open('Marks.dat','rb') as f:
        l=[['SID','MATH THEORY','MATH PRACT','PHY THEORY','PHY PRACT','CHEM THEORY','CHEM PRACT','CS THEORY','CS PRACT','ENG THEORY','ENG PRACT']]
        try:
            while True:
                r = pickle.load(f)
                l1 = [r[0],r[1][0],r[1][1],r[2][0],r[2][1],r[3][0],r[3][1],r[4][0],r[4][1],r[5][0],r[5][1]]      
                l.append(l1)
        except EOFError:
            print(tabulate(l,headers = 'firstrow',tablefmt = 'fancy_grid'))
            print('-'*20,'End of Records','-'*20)

def view_report():
    with open('Student_details.dat','rb') as f:
        with open('Marks.dat','rb') as f1:
            sid = input('Enter student ID   :')
            try:
                found = False
                while True:
                    r = pickle.load(f)
                    if r[0] == sid.upper() and r[4] == 'AVAILABLE':
                        sid = r[0]
                        s_name = r[1]
                        s_div = r[3]
                        found = True
            except EOFError:
                pass
            found1 = False
            if found:
                try:
                    found1 = False
                    while True:
                        r = pickle.load(f1)
                        if r[0] == sid.upper():
                            math = r[1]
                            phy  = r[2]
                            chem = r[3]
                            cs   = r[4]
                            eng  = r[5]
                            found1 = True
                except EOFError:
                    pass
            if not found:
                print('\n!!! Student not found !!!\n')
            if not found1:
                print('\n!!! No marks were added for student',sid.upper(),'!!!\n')
            if found and found1:
                #.center() is used to center the text
                print('-'*90)
                print('SHARJAH INDIAN SCHOOL'.center(90))
                print('PO Box: 2564 Sharjah UAE'.center(90))
                print('Tel: 26 562 6662'.center(90))
                print('boys@sissharjah.com'.center(90))
                print('Website: www.sisjuwaiza.com'.center(90))
                print()
                print('FINAL REPORT CARD - 2020-21'.center(90))
                print()
                print('Name of Student   :',s_name)
                print('Student ID        :',sid)
                print('Grade & Section   :','12',s_div)
                print()
                print('GRADE XII YEARLY PERFORMANCE'.center(90))
                l = [['SUBJECT','THEORY (80)','PRACTICAL (20)','TOTAL (100)','GRADE']]
                l1 = ['ENGLISH',eng[0],eng[1],int(eng[0])+int(eng[1])]
                if l1[3] > 90 and l1[3] <= 100:
                    grade1 = 'A1'
                elif l1[3] > 80 and l1[3] <= 90:
                    grade1 = 'A2'
                elif l1[3] > 70 and l1[3] <= 80:
                    grade1 = 'B1'
                elif l1[3] > 60 and l1[3] <= 70:
                    grade1 = 'B2'
                elif l1[3] > 50 and l1[3] <= 60:
                    grade1 = 'C1'
                elif l1[3] > 40 and l1[3] <= 50:
                    grade1 = 'C2'
                elif l1[3] > 32 and l1[3] <= 40:
                    grade1 = 'D'
                elif l1[3] <= 32:
                    grade1 = 'F [FAILED]'
                l1.append(grade1)
                l2 = ['MATHEMATICS',math[0],math[1],int(math[0])+int(math[1])]
                if l2[3] > 90 and l2[3] <= 100:
                    grade2 = 'A1'
                elif l2[3] > 80 and l2[3] <= 90:
                    grade2 = 'A2'
                elif l2[3] > 70 and l2[3] <= 80:
                    grade2 = 'B1'
                elif l2[3] > 60 and l2[3] <= 70:
                    grade2 = 'B2'
                elif l2[3] > 50 and l2[3] <= 60:
                    grade2 = 'C1'
                elif l2[3] > 40 and l2[3] <= 50:
                    grade2 = 'C2'
                elif l2[3] > 32 and l2[3] <= 40:
                    grade2 = 'D'
                elif l2[3] <= 32:
                    grade2 = 'F [FAILED]'
                l2.append(grade2)
                l3 = ['PHYSICS',phy[0],phy[1],int(phy[0])+int(phy[1])]
                if l3[3] > 90 and l3[3] <= 100:
                    grade3 = 'A1'
                elif l3[3] > 80 and l3[3] <= 90:
                    grade3 = 'A2'
                elif l3[3] > 70 and l3[3] <= 80:
                    grade3 = 'B1'
                elif l3[3] > 60 and l3[3] <= 70:
                    grade3 = 'B2'
                elif l3[3] > 50 and l3[3] <= 60:
                    grade3 = 'C1'
                elif l3[3] > 40 and l3[3] <= 50:
                    grade3 = 'C2'
                elif l3[3] > 32 and l3[3] <= 40:
                    grade3 = 'D'
                elif l3[3] <= 32:
                    grade3 = 'F [FAILED]'
                l3.append(grade3)
                l4 = ['CHEMISTRY',chem[0],chem[1],int(chem[0])+int(chem[1])]
                if l4[3] > 90 and l4[3] <= 100:
                    grade4 = 'A1'
                elif l4[3] > 80 and l4[3] <= 90:
                    grade4 = 'A2'
                elif l4[3] > 70 and l4[3] <= 80:
                    grade4 = 'B1'
                elif l4[3] > 60 and l4[3] <= 70:
                    grade4 = 'B2'
                elif l4[3] > 50 and l4[3] <= 60:
                    grade4 = 'C1'
                elif l4[3] > 40 and l4[3] <= 50:
                    grade4 = 'C2'
                elif l4[3] > 32 and l4[3] <= 40:
                    grade4 = 'D'
                elif l4[3] <= 32:
                    grade4 = 'F [FAILED]'
                l4.append(grade4)
                l5 = ['COMPUTER SCICENCE',cs[0],cs[1],int(cs[0])+int(cs[1])]
                if l5[3] > 90 and l5[3] <= 100:
                    grade5 = 'A1'
                elif l5[3] > 80 and l5[3] <= 90:
                    grade5 = 'A2'
                elif l5[3] > 70 and l5[3] <= 80:
                    grade5 = 'B1'
                elif l5[3] > 60 and l5[3] <= 70:
                    grade5 = 'B2'
                elif l5[3] > 50 and l5[3] <= 60:
                    grade5 = 'C1'
                elif l5[3] > 40 and l5[3] <= 50:
                    grade5 = 'C2'
                elif l5[3] > 32 and l5[3] <= 40:
                    grade5 = 'D'
                elif l5[3] <= 32:
                    grade5 = 'F [FAILED]'
                l5.append(grade5)
                l.append(l1)
                l.append(l2)
                l.append(l3)
                l.append(l4)
                l.append(l5)
                print(tabulate(l,headers = 'firstrow', tablefmt = 'fancy_grid'))
                result = [['RESULT - GRADE 12']]
                if grade1 == 'F [FAILED]' or grade2 == 'F [FAILED]' or grade3 == 'F [FAILED]' or grade4 == 'F [FAILED]' or grade5 == 'F [FAILED]':
                    rr = ['Detained In Grade 12']
                else:
                    rr = ['Passed And Promoted From Grade 12']
                result.append(rr)
                print(tabulate(result,headers = 'firstrow', tablefmt = 'grid'))
                print()
                print('THANK YOU'.center(90))
                datentime=str(datetime.now())
                print('\nPricipal, SHARJAH INDIAN SCHOOL','                           ','viewed on:',datentime[0:19])
                print('-'*90)

#--------------------------------------------------------------------------------------------------------------------------------------------
#Project
#--------------------------------------------------------------------------------------------------------------------------------------------
                
print('SHARJAH INDIAN SCHOOL'.center(90))
print('PO Box: 2564 Sharjah UAE'.center(90))
print('Tel: 26 562 6662'.center(90))
print('boys@sissharjah.com'.center(90))
print('Website: www.sisjuwaiza.com'.center(90))
print()
print('Welcome to SHARJAH INDIAN SCHOOL'.center(90))
while True:
    s_or_t_or_a = input('''Are you a
S: Student
T: Teacher
A: Admin
              :''')
    print()
    if s_or_t_or_a.upper() == 'S':
        view_report()
    elif s_or_t_or_a.upper() == 'A':
        admin_login()
        if aaccess:
            while True:
                ch = input('''\n1. Add teacher
2. Update teacher details
3. Delete teacher
4. View teacher list

5. Add student
6. Update student details
7. Delete student
8. View student list

Enter your choice       :''')
                if ch == '1':
                    add_teacher()
                elif ch == '2':
                    update_teacher()
                elif ch == '3':
                    delete_teacher()
                elif ch == '4':
                    view_teacher()
                elif ch == '5':
                    add_student()
                elif ch == '6':
                    update_student()
                elif ch == '7':
                    delete_student()
                elif ch == '8':
                    view_student()
                else:
                    print('\nPlease enter a valid choice\n')
                c = input('Do you want to continue as Admin [Y/N] ?')
                if c not in 'yY':
                    break
            
    elif s_or_t_or_a.upper() == 'T':
        teacher_login()
        if taccess:
            while True:
                ch = input('''\n1. Add marks
2. Update marks
3. View report*
*one student a time

Enter your choice :''')
                if ch == '1' or ch == '2':
                    addorupdate_marks()
                elif ch == '3':
                    view_report()
                else:
                    print('\nPlease enter a valid choice\n')
                c = input('Do you want to continue as Teacher [Y/N] ?')
                if c not in 'yY':
                    break
    else:
        print('\nOoops, an error occured :(\n')
    c = input('Do you want to :\nY: Home page\nN: Exit\n               :')
    if c not in 'Yy':
        print('\nTHANK YOU'.center(90))
        break

#--------------------------------------------------------------------------------------------------------------------------------------------
#End
#By Nihal & Shehzad
#Thank you
#--------------------------------------------------------------------------------------------------------------------------------------------
            
            

                     
            
