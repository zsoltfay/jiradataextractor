from jira import JIRA
from tkinter import *
from tkinter import messagebox
from prettytable import PrettyTable
import json


def import_auth_data():
    with open("auth_data.json", "r") as data_file:
        return json.load(data_file)


def initialization():
    # Imports auth data from auth_data.json
    jira_auth_object = import_auth_data()
    # main jira object
    global jira
    jira = JIRA(basic_auth=(jira_auth_object["username"],
                            jira_auth_object["password"]),
                options={'server': jira_auth_object["jira_server"]})
    return jira


def import_main_geometry_dimmension():
    with open("configuration.json", "r") as data_file:
        data = json.load(data_file)
        main_geometry_dimmension = data["body_configuration"]["main_window"]["geometry"]["width"] + \
                                   "x" + \
                                   data["body_configuration"]["main_window"]["geometry"]["height"]
    return main_geometry_dimmension


def import_main_geometry_title():
    with open("configuration.json", "r") as data_file:
        data = json.load(data_file)
        title = data["body_configuration"]["main_window"]["title"]
        print("Title is:", title)
        return title


def main_tk_obj(root):
    # print(import_main_geometry_dimmension())
    root.geometry(import_main_geometry_dimmension())
    root.title(import_main_geometry_title())
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
    if component:
        jql = create_jql(component)
        draw_table(jql)
    else:
        messagebox.showerror("Error", "Please fill the component box!")


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
