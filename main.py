import json
import os
import sys
import time


#repetitive values needed
def current_time():
    t = time.localtime()
    return str(time.strftime("%H:%M:%S", t))
def json_dict(filename):
    with open(filename) as data:
        return json.load(data) 
def json_write(filename, newdata):
    with open(filename, "w") as data:
        data.write(json.dumps(newdata, indent=4,sort_keys=True))
def end(s='''Would you like to repeat this action?
              1) Yes
              2) Return to menu'''):
    return int(input(s))
def end_cycle(num, result):
    match result:
        case 1:
            main(num)
        case 2:
            main(modules = int(input('''Select action by entering a number as a prompt.
        1) Add task
        2) View Tasks (completed, inprogress and not started)
        3) Update Tasks
        4) Delete Tasks
        5) Exit Program''')))
        case _:
            print("invalid selection")
            end_cycle()



def main(modules = int(input('''Select action by entering a number as a prompt.
        1) Add task
        2) View Tasks (completed, inprogress and not started)
        3) Update Tasks
        4) Delete Tasks
        5) Exit Program'''))):

    
    match modules:
        case 1:
            add_task()
        case 2:
            view_tasks()
        case 3:
            update_tasks()
        case 4:
            delete_tasks()
        case 5:
            print("terminating program")
            sys.exit(3)
        case _:
            print("invalid selection")
            main()
            


def add_task():

#local variables
    taskname = str(input("name of task?: "))
    desc = str(input("write a descripion for the task: "))
    status = int(input('''What is the status of this task?: 
                       1) Completed
                       2) In Progress
                       3) Incomplete'''))
    status_map = {
        1: "COM",
        2: "IPR",
        3: "INC"
    }

    entry = {
    taskname : {
        "taskID": "sampleID",
        "desc": desc,
        "timeCreated": current_time(),
        "timeUpdated": current_time(),
        "status": status_map[status]
    }
}
    
    #function itself
    try:
        read = json_dict("cfg.json")
        read.update(entry)
        json_write("cfg.json", read)
        
        result = end()
        end_cycle(1, result)

    except FileNotFoundError:
        print("information was not saved, try again [cfg.json file now made to track tasks!]")
        json_write("cfg.json", newdata={})
        add_task()


def view_tasks():
    try:
        task_map={}
        counter=0
        for tasks in json_dict("cfg.json"):
            counter+=1
            print(f"{counter}) {tasks}")
            kp = {counter:tasks}
            task_map.update(kp)

        task = int(input('''What task would you like to view?: '''))

        view_task = task_map[task]
        print(json_dict("cfg.json")[view_task])

        result = end()
        end_cycle(2,result)
        
    except FileNotFoundError:
        print("no information to be viewed, try again [cfg.json file now made to track tasks!]")
        json_write("cfg.json", newdata={})
        add_task()

def update_tasks():
    try:
        task_map={}
        counter=0
        for tasks in json_dict("cfg.json"):
            counter+=1
            print(f"{counter}) {tasks}")
            kp = {counter:tasks}
            task_map.update(kp)

        task = int(input('''What task would you like to Update: '''))

        view_task = task_map[task]
        print(view_task)

        attributes = json_dict("cfg.json")[view_task]

        task_map={}
        counter = 0
        for data_type in attributes:
            counter+=1
            print(f"{counter}) {data_type}")
            kp = {counter:data_type}
            task_map.update(kp)
        
        attribute = int(input('''What data type would you like to Update: '''))
        new_attribute=task_map[attribute]
        
        new_info=str(input("enter new info: "))
        entry={data_type: new_info}

        updated_attribute = json_dict("cfg.json")
        updated_attribute[view_task].update(entry)

        updated_attribute[view_task].update({"timeUpdated":current_time()}) #
        json_write("cfg.json", updated_attribute)

        result = end()
        end_cycle(3, result)

    except FileNotFoundError:
        print("No file for updating information, try again [cfg.json file now made to track tasks!]")
        json_write("cfg.json", newdata={})
        add_task()

def delete_tasks():
    try:
        task_map={}
        counter=0
        for tasks in json_dict("cfg.json"):
            counter+=1
            print(f"{counter}) {tasks}")
            kp = {counter:tasks}
            task_map.update(kp)

        task = int(input('''What task would you like to Delete: '''))
        view_task = task_map[task]

        a=json_dict("cfg.json")
        del a[view_task]

        json_write("cfg.json", a)

        result = end()
        end_cycle(4, result)

    except FileNotFoundError:
        print("No file for deleting information, try again [cfg.json file now made to track tasks!]")
        json_write("cfg.json", newdata={})
        add_task()


main()