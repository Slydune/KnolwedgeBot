import json


# temp file is 29 on index of start
def str_to_dict(in_string, index_of_start):
    in_string = in_string[index_of_start::].strip()
    z = json.loads(in_string)
    return z

# {"text": "school name + course name: + course desc", "metadata": "School 1 School 1 Course"}
def file_dump1(file_name, info):
    file = open(file_name + ".jsonl", "a")
    school1 = info.get('School 1').replace("\n", " ")
    course1 = info.get('School 1 Course').replace("\n", " ")
    desc1 = info.get('Course 1 Desc').replace("\n", " ")
    school2 = info.get('School 2').replace("\n", " ")
    course2 = info.get('School 2 Course').replace("\n", " ")
    desc2 = info.get('Course 2 Desc').replace("\n", " ")
    checK_file = open(file_name+".jsonl","r")
    if "{\"text\":\""+school1+" "+course1+": "+desc1+"\", \"metadata\": \""+school1+" "+course1+"\"}\n" in checK_file.readlines():
        pass
    else:
        file = open(file_name + ".jsonl", "a")
        file.write("{\"text\":\""+school1+" "+course1+": "+desc1+"\", \"metadata\": \""+school1+" "+course1+"\"}\n")
        file.write("{\"text\":\"" + school2 + " " + course2 + ": " + desc2 + "\", \"metadata\": \"" + school2+" "+course2+"\"}\n")
    checK_file.close()
    file.close()


# UNIVERSITY OF LOUISVILLE ELFH 490 LEADERSHIP AND MANAGEMENT matches AMERICAN COUNCIL ON EDUCATION WALT-0007 DISNEY ORGANIZATIONAL LEADERSHIP COURSE
def file_dump2(file_name, info):
    file = open(file_name, "a")
    school1 = info.get('School 1').replace("\n", " ")
    course1 = info.get('School 1 Course').replace("\n", " ")
    school2 = info.get('School 2').replace("\n", " ")
    course2 = info.get('School 2 Course').replace("\n", " ")
    checK_file = open(file_name, "r")
    if school1+" "+course1+" matches " + school2 + " " +course2+"\n" in checK_file.readlines():
        pass
    else:
        file.write(school1+" "+course1+" matches " + school2 + " " +course2+"\n")
    checK_file.close()
    file.close()


file = open("D:/Downloads/TES-A", "r")
output_file = file.read().split("}{")
for temp in output_file:
    try:
        info = str_to_dict(temp, 29)
        file_dump1("firstdata", info)
        file_dump2("seconddata", info)
    except:
        pass
file.close()


