from tkinter import *
from tkinter import ttk
import engine as en

database_name = 'new_db'
login = 'alina'
password = 'anzor'

cursor = None

try:
    cursor = en.connect_as_user(login, password, database_name)
except Exception as e:
    print(type(e))
    print(e.args)
    print(e)


def btnCommand_createDB():
    global cursor
    en.create_database(database_name, login)
    cursor = en.connect_as_user(login, password, database_name)


def btnCommand_deleteDB():
    global cursor
    if cursor is not None:
        en.disconnect_user(cursor)
        en.drop_database(database_name)
        cursor = None


def btnCommand_clearTablesDB():
    if cursor is None:
        return

    def btnCommand_clearTables():
        en.clear_all_tables(cursor)
        root1.destroy()

    root1 = Toplevel()
    root1.title('Отчистка таблиц')
    root1.geometry("300x70+550+200")
    Label(root1, text="Вы уверены, что хотите очистить все таблицы?").pack(side=TOP)
    btn_yes = Button(root1, text="Да", command=btnCommand_clearTables)
    btn_no = Button(root1, text="Нет", command=root1.destroy)
    btn_yes.pack()
    btn_no.pack()


def btnCommand_printTableDepartment():
    root2 = Toplevel()
    root2.title('Отделы')
    root2.geometry("+30+100")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three")
    tree.column("#0", width=40, minwidth=40, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')

    tree.heading("#0", text="id")
    tree.heading("one", text="name")
    tree.heading("two", text="phone")
    tree.heading("three", text="kpi")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_department(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
    tree.pack()


def btnCommand_printTableBank():
    root2 = Toplevel()
    root2.title('Банки')
    root2.geometry("+800+100")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three")
    tree.column("#0", width=40, minwidth=40, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')

    tree.heading("#0", text="id")
    tree.heading("one", text="name")
    tree.heading("two", text="address")
    tree.heading("three", text="interest")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_bank(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
    tree.pack()


def btnCommand_printTableEmployee():
    root2 = Toplevel()
    root2.title('Сотрудники')
    root2.geometry("+30+500")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven")
    tree.column("#0", width=40, minwidth=40, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')
    tree.column("four", anchor='center')
    tree.column("five", anchor='center')
    tree.column("six", anchor='center')
    tree.column("seven", anchor='center')

    tree.heading("#0", text="id")
    tree.heading("one", text="name")
    tree.heading("two", text="department")
    tree.heading("three", text="mobile_phone")
    tree.heading("four", text="bank")
    tree.heading("five", text="salary")
    tree.heading("six", text="prize")
    tree.heading("seven", text="total_salary")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_employee(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[7] = values[7][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3],
                                                                    values[4], values[5], values[6],
                                                                    values[7]))
    tree.pack()


def btnCommand_printTablesDB():
    if cursor is None:
        return
    btnCommand_printTableDepartment()
    btnCommand_printTableBank()
    btnCommand_printTableEmployee()


def btnCommand_workWithTableDepartment():
    if cursor is None:
        return

    def btnCommand_clearTable():
        en.clear_department(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_department(cursor, entry1.get(), entry2.get(), entry3.get(), entry4.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='name')
        label.grid(row=0, column=1)
        label = Label(root2, text='phone')
        label.grid(row=0, column=2)
        label = Label(root2, text='kpi')
        label.grid(row=0, column=3)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.grid(row=1, column=0)
        result = en.print_table_department(cursor)
        var = 0
        if len(result) != 0:
            var = int(result[len(result) - 1][0].split(',')[0][1:])
        entry1.insert(0, str(var+1))
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '')
        entry3 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '')
        entry4 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '0')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=2)

    def btnCommand_deleteLine():
        def btnAccept():
            en.delete_department_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите id')
        label.pack()
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '0')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.pack()

    root1 = Toplevel()
    root1.title('Отделы')
    root1.geometry("400x250+550+200")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_printTable = Button(root1, text="Вывести таблицу", command=btnCommand_printTableDepartment())

    btn_addNewLine = Button(root1, text="Добавить новую запись", command=btnCommand_addNewLine)

    btn_deleteLine = Button(root1, text="Удалить запись (id)", command=btnCommand_deleteLine)

    btn_clearTable.pack()
    btn_printTable.pack()
    btn_addNewLine.pack()
    btn_deleteLine.pack()


def btnCommand_workWithTableBank():
    if cursor is None:
        return

    def btnCommand_clearTable():
        if cursor is not None:
            en.clear_bank(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_bank(cursor, entry1.get(), entry2.get(), entry3.get(), entry4.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("630x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='name')
        label.grid(row=0, column=1)
        label = Label(root2, text='address')
        label.grid(row=0, column=2)
        label = Label(root2, text='interest')
        label.grid(row=0, column=3)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        result = en.print_table_bank(cursor)
        var = 0
        if len(result) != 0:
            var = int(result[len(result) - 1][0].split(',')[0][1:])
        entry1.insert(0, str(var+1))
        entry1.grid(row=1, column=0)
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '1')
        entry3 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '1')
        entry4 = Entry(root2, width=7, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '1')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=2)

    def btnCommand_deleteLine():
        def btnAccept():
            en.delete_bank_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите id')
        label.pack()
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '0')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.pack()

    root1 = Toplevel()
    root1.title('Банки')
    root1.geometry("400x250+550+200")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_printTable = Button(root1, text="Вывести таблицу", command=btnCommand_printTableBank)

    btn_addNewLine = Button(root1, text="Добавить новую запись", command=btnCommand_addNewLine)

    btn_deleteLine = Button(root1, text="Удалить запись (id)", command=btnCommand_deleteLine)

    btn_clearTable.pack()
    btn_printTable.pack()
    btn_addNewLine.pack()
    btn_deleteLine.pack()


def btnCommand_workWithTableEmployee():
    if cursor is None:
        return

    def btnCommand_clearTable():
        if cursor is not None:
            en.clear_employee(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_employee(cursor, entry1.get(), entry2.get(), entry3.get(),
                             entry4.get(), entry5.get(), entry6.get(), entry7.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("830x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='name')
        label.grid(row=0, column=1)
        label = Label(root2, text='department')
        label.grid(row=0, column=2)
        label = Label(root2, text='mobile_phone')
        label.grid(row=0, column=3)
        label = Label(root2, text='bank')
        label.grid(row=0, column=4)
        label = Label(root2, text='salary')
        label.grid(row=0, column=5)
        label = Label(root2, text='prize')
        label.grid(row=0, column=6)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        result = en.print_table_employee(cursor)
        var = 0
        if len(result) != 0:
            var = int(result[len(result) - 1][0].split(',')[0][1:])
        entry1.grid(row=1, column=0)
        entry1.insert(0, str(var + 1))
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '')
        entry3 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '1')
        entry4 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '')
        entry5 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry5.grid(row=1, column=4)
        entry5.insert(0, '1')
        entry6 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry6.grid(row=1, column=5)
        entry6.insert(0, '1')
        entry7 = Entry(root2, width=7, fg='blue', font=('Arial', 16, 'bold'))
        entry7.grid(row=1, column=6)
        entry7.insert(0, '1')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=3)

    def btnCommand_deleteLineById():
        def btnAccept():
            en.delete_employee_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите id')
        label.pack()
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '0')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.pack()

    def btnCommand_deleteLineByName():
        def btnAccept():
            en.delete_employee_by_mobile_phone(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите номер телефона')
        label.pack()
        entry1 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.pack()

    def btnCommand_findLine():
        def btnAccept():
            result = en.search_employee_by_mobile_phone(cursor, entry1.get())

            root3 = Toplevel()
            tree = ttk.Treeview(root3, selectmode='browse')

            tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven")
            tree.column("#0", width=40, minwidth=40)
            tree.column("one")
            tree.column("two")
            tree.column("three")
            tree.column("four")
            tree.column("five")
            tree.column("six")
            tree.column("seven")

            tree.heading("#0", text="id")
            tree.heading("one", text="name")
            tree.heading("two", text="department")
            tree.heading("three", text="mobile_phone")
            tree.heading("four", text="bank")
            tree.heading("five", text="salary")
            tree.heading("six", text="prize")
            tree.heading("seven", text="total_salary")

            values = result[0][0].split(',')
            values[0] = values[0][1:]
            values[7] = values[7][:-1]
            tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3],
                                                                        values[4], values[5], values[6],
                                                                        values[7]))
            tree.pack()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите имя')
        label.pack()
        entry1 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '')
        entry1.pack()

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.pack()

    def btnCommand_updateLine():
        def btnAccept():
            en.update_employee(cursor, entry1.get(), entry2.get(), entry3.get(),
                             entry4.get(), entry5.get(), entry6.get(), entry7.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("830x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='name')
        label.grid(row=0, column=1)
        label = Label(root2, text='department')
        label.grid(row=0, column=2)
        label = Label(root2, text='mobile_phone')
        label.grid(row=0, column=3)
        label = Label(root2, text='bank')
        label.grid(row=0, column=4)
        label = Label(root2, text='salary')
        label.grid(row=0, column=5)
        label = Label(root2, text='prize')
        label.grid(row=0, column=6)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.grid(row=1, column=0)
        entry1.insert(0, '-1')
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '')
        entry3 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '-1')
        entry4 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '')
        entry5 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry5.grid(row=1, column=4)
        entry5.insert(0, '-1')
        entry6 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry6.grid(row=1, column=5)
        entry6.insert(0, '-1')
        entry7 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry7.grid(row=1, column=6)
        entry7.insert(0, '-1')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отменить", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=3)

    root1 = Toplevel()
    root1.title('Сотрудники')
    root1.geometry("400x250+550+200")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_printTable = Button(root1, text="Вывести таблицу", command=btnCommand_printTableEmployee)

    btn_addNewLine = Button(root1, text="Добавить новую запись", command=btnCommand_addNewLine)

    btn_deleteLineById = Button(root1, text="Удалить сотрудника (id)", command=btnCommand_deleteLineById)

    btn_deleteLineByName = Button(root1, text="Удалить сотрудника (name)", command=btnCommand_deleteLineByName)

    btn_findLine = Button(root1, text="Найти сотрудника (name)", command=btnCommand_findLine)

    btn_updateLine = Button(root1, text="Обновить сотрудника (name)", command=btnCommand_updateLine)

    btn_clearTable.pack()
    btn_printTable.pack()
    btn_addNewLine.pack()
    btn_deleteLineById.pack()
    btn_deleteLineByName.pack()
    btn_findLine.pack()
    btn_updateLine.pack()


if __name__ == '__main__':
    root = Tk()
    root.title('ОАО ТНС')
    root.geometry("400x250+550+200")

    button_createDB = Button(text="Создать базу данных", command=btnCommand_createDB)
    button_deleteDB = Button(text="Удалить базу данных", command=btnCommand_deleteDB)

    button_printTables = Button(text="Вывести все таблицы", command=btnCommand_printTablesDB)
    button_clearTables = Button(text="Очистить все таблицы", command=btnCommand_clearTablesDB)

    button_workWithTableDepartment = Button(text="Отделы", command=btnCommand_workWithTableDepartment)
    button_workWithTableBank = Button(text="Банки", command=btnCommand_workWithTableBank)
    button_workWithTableEmployee = Button(text="Сотрудники", command=btnCommand_workWithTableEmployee)

    button_createDB.pack()
    button_deleteDB.pack()
    button_printTables.pack()
    button_clearTables.pack()
    button_workWithTableDepartment.pack()
    button_workWithTableBank.pack()
    button_workWithTableEmployee.pack()

    root.mainloop()