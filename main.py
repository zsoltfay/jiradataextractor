from jira import JIRA
from tkinter import *
from prettytable import PrettyTable


class Extractor:
    def __init__(self, master):
        self.master = master
        self.jira = self.initialization()
        self.create_widgets()
        self.jql = None
        self.project_name = None
        self.component = None

    @staticmethod
    def initialization():
        jira = JIRA(basic_auth=('username', 'password'), options={'server': 'https://jira.organization.ro'})
        return jira

    def create_widgets(self):
        self.master.geometry("500x400")
        self.master.title("Search details")

        self.label_0 = Label(self.master, text="Data Extraction", width=20, font=("bold", 20))
        self.label_0.place(x=90, y=53)
        self.label_1 = Label(self.master, text="Project Name", width=20, font=("bold", 10))
        self.label_1.place(x=80, y=130)
        self. entry_1 = Entry(self.master)
        self.entry_1.place(x=240, y=130)
        self.label_2 = Label(self.master, text="Component", width=20, font=("bold", 10))
        self. label_2.place(x=80, y=180)
        self.entry_2 = Entry(self.master)
        self.entry_2.place(x=240, y=180)
        Button(self.master, text="Extract", width=20, bg="blue", fg="white", command=self.get_ticket_list).place(x=180, y=280)
        Button(self.master, text="Quit", width=10, bg="brown", fg="white", command=self.master.destroy).place(x=220, y=310)

    def get_input(self):
        self.project_name = self.entry_1.get()
        self.component = self.entry_2.get()

    def create_jql(self):
        print(self.get_input)
        self.jql = "project='%s' and component='%s'" % (self.project_name, self.component)

    def get_list_of_comments(self, key):
        list_of_comments = []
        comments = self.jira.comments(key)
        a = int(0)
        for i in comments:
            if int(i.id) > a:
                a = int(i.id)
                list_of_comments.append(self.jira.comment(key, a).body)
        return list_of_comments

    @staticmethod
    def draw_table(lista):
        table = PrettyTable()
        table.field_names = ["Issue key", "Issue ID", "Reporter", "Status", "Priority"]
        for i in lista:
            key = str(i.key)
            id = str(i.id)
            reporter = str(i.fields.reporter)
            status = str(i.fields.status)
            priority = str(i.fields.priority)
            table.add_row([key, id, reporter, status, priority])
        print(table)

    def get_ticket_list(self):
        self.get_input()
        self.create_jql()
        ticket_list = self.jira.search_issues(self.jql, maxResults=10)
        self.draw_table(ticket_list)


master = Tk()
b = Extractor(master)
master.mainloop()
