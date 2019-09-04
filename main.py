from jira import JIRA
from tkinter import *
from prettytable import PrettyTable


def initialization():
    # main jira object
    global jira
    jira = JIRA(basic_auth=('username', 'password'), options={'server': 'https://jira.org.ro'})
    return jira


def main_tk_obj(root):
    root.geometry("500x400")
    root.title("Search details")
    return root


def create_title_label(root, name, x , y):
    label = Label(root, text=name, width=20, font=("bold", 20))
    label.place(x=x, y=y)


def create_label_text(root, name, x, y):
    label = Label(root, text=name, width=20, font=("bold", 10))
    label.place(x=x, y=y)


def create_label_entry(root, x, y):
    global entry
    entry = Entry(root)
    entry.place(x=x, y=y)
    return entry


def create_button(root, name, width, bg, fg, command, x, y):
    Button(root, text=name, width=width, bg=bg, fg=fg, command=command).place(x=x, y=y)


def store_input():
    data = entry.get()
    return data


def create_jql(data):
    jql = "project='%s' and component='%s'" % ("NOKSUPP", data)
    return jql


def draw_table(jql):
    ticket_list = jira.search_issues(jql, maxResults=10)
    table = PrettyTable()
    table.field_names = ["Issue key", "Issue ID", "Reporter", "Status", "Priority"]
    for i in ticket_list:
        key = str(i.key)
        id = str(i.id)
        reporter = str(i.fields.reporter)
        status = str(i.fields.status)
        priority = str(i.fields.priority)
        table.add_row([key, id, reporter, status, priority])
    print(table)


def main():
    component = store_input()
    jql = create_jql(component)
    draw_table(jql)


if __name__ == "__main__":
    initialization()
    root = Tk()
    main_tk_obj(root)
    create_title_label(root, "Data Extraction", 90, 53)
    create_label_text(root, "Component", 80, 130)
    entry = create_label_entry(root, 240, 130)
    create_button(root, "Extract", 20, "blue", "white", main, 180, 280)
    create_button(root, "Quit", 10, "brown", "white", root.destroy, 220, 310)
    root.mainloop()
