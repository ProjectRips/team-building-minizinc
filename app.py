
from flask import Flask, request, render_template, redirect, url_for
import os
import minizinc
import json


app = Flask(__name__)
app.secret_key = "secret"


def mnz_teams_building(path):

  # Create a MiniZinc model
  model = minizinc.Model(path)


  # Transform Model into a instance
  gecode = minizinc.Solver.lookup("gecode")
  instance = minizinc.Instance(gecode, model)

  # Solve the instance
  result = instance.solve( nr_solutions=10, optimisation_level=5)
  return result

  
#   return result


# route =============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form-team')
def form_team_page():
    return render_template('form_team.html')

@app.route('/form-team', methods=['POST'])
def post_form_team():
    num_persons = int(request.form.get("num_persons"))
    num_teams = int(request.form.get("num_teams"))
    num_services = int(request.form.get("num_services"))
    services_pairing = request.form.getlist("service_pairing[]")
    services = request.form.getlist("services[]")
    statuses = request.form.getlist("statuses[]")
    input_max_status = request.form.getlist("input_max_status[]")
    example = request.form.get("example")


    num_max_same = ""

    if request.form.get("num_max_same") != "" and request.form.get("num_max_same") != None :
        num_max_same = request.form.get("num_max_same")
    
    if(example == "true"):
        return redirect(url_for('form_render_example_table', 
                            num_persons=num_persons, 
                            num_teams=num_teams, 
                            num_services=num_services,
                            num_max_same=num_max_same,
                            input_max_status=input_max_status,
                            services_pairing=services_pairing,
                            services=services,
                            statuses=statuses))
    else: 
         return redirect(url_for('form_render_table', 
                            num_persons=num_persons, 
                            num_teams=num_teams, 
                            num_services=num_services,
                            num_max_same=num_max_same,
                            input_max_status=input_max_status,
                            services_pairing=services_pairing,
                            services=services,
                            statuses=statuses))

@app.route('/form-team-example')
def form_team_example_page():
    return render_template('form_team_example.html')

@app.route('/form-team-example', methods=['POST'])
def post_form_team_example():
    num_persons = int(request.form.get("num_persons"))
    num_teams = int(request.form.get("num_teams"))
    num_services = int(request.form.get("num_services"))
    services_pairing = request.form.getlist("service_pairing[]")
    services = request.form.getlist("services[]")
    statuses = request.form.getlist("statuses[]")
    input_max_status = request.form.getlist("input_max_status[]")



    num_max_same = ""

    if request.form.get("num_max_same") != "" and request.form.get("num_max_same") != None :
        num_max_same = request.form.get("num_max_same")
    


    return redirect(url_for('form_render_table', 
                            num_persons=num_persons, 
                            num_teams=num_teams, 
                            num_services=num_services,
                            num_max_same=num_max_same,
                            input_max_status=input_max_status,
                            # num_max_emp=num_max_emp,
                            # num_max_intern=num_max_intern,
                            services_pairing=services_pairing,
                            services=services,
                            statuses=statuses))


@app.route('/form-table')
def form_render_table():
    return render_template("form_table.html")

@app.route('/form-table-example')
def form_render_example_table():
    return render_template("form_table_example.html")

@app.route('/form-table-example', methods=['POST'])
@app.route('/form-table', methods=['POST'])
def form_table_page():
   
    #form data and check for coachinh constraint
    form = []

    # declare variable
    persons = ""
    coach_count = 0
    coach_constraint = ""
    ww = ""
    must_code = ""
    json_data_rows = "["

    # declare num_variables ==================================================
    num_persons = request.form.get("num_persons")
    num_services = request.form.get("num_services")
    num_teams = request.form.get("num_teams")

    num_max_same = ""

    if request.form.get("num_max_same") != "" and request.form.get("num_max_same") != None:
        num_max_same = request.form.get("num_max_same")
    
    input_max_status = eval(request.form.get("input_max_status"))


    services_pairing = request.form.get("services_pairing")
    services_data = eval(request.form.get("services"))
    statuses = eval(request.form.get("statuses"))

    count_must = 0
    for i in range(int(num_persons)):
        must = request.form.get("row-" + str(i) + "-must")
        if(must != "" and must != None):
            count_must += 1
    
    count_want_with = 0
    for i in range(int(num_persons)):
        want_with = request.form.get("row-" + str(i) + "-want")
        if(want_with != "" and want_with != None):
            count_want_with += 1


    count_must2 = 0
    count_want_with2 = 0
    for i in range(int(num_persons)):
        num = request.form.get("row-" + str(i) + "-num")
        id = request.form.get("row-" + str(i) + "-id")
        name = request.form.get("row-" + str(i) + "-name")
        status = request.form.get("row-" + str(i) + "-status")
        coach = request.form.get("row-" + str(i) + "-supervise")
        must = request.form.get("row-" + str(i) + "-must")
        want_with = request.form.get("row-" + str(i) + "-want")
        service = request.form.get("row-" + str(i) + "-service")

        if(i != int(num_persons)-1):
            json_data_rows += '{"num" : "' + num + '", "id" : "' + id + '", "name" : "' + name + '", "status" : "' + status + '", "service" : "' + service + '" },'
        else:
            json_data_rows += '{"num" : "' + num + '", "id" : "' + id + '", "name" : "' + name + '", "status" : "' + status + '", "service" : "' + service + '" }'

        # status -> employee / intern constraint
        persons += "        " +  id + "," + status + ",\n"
        
        #coach
        if(coach != "" and coach != None):
            coach_count += 1
            coach_constraint += "       " + id + "," + coach + ",\n"

        if(must != "" and must != None):
            count_must2 += 1
            splitter = must.split(",")
            must_code += " \n ("
            for m in range(len(splitter)):
                must_code += "team[" + id + "] = team[" + splitter[m] + "]"
                if m != len(splitter) - 1:
                    must_code += " /\\ "
            if(count_must != count_must2):
                must_code += ") /\\\n"
            elif(count_must == count_must2):
                must_code += ") \n"
          

        if(want_with != "" and want_with != None):
            count_want_with2 += 1
            splitter = want_with.split(",")
            ww += " \n ("
            for j in range(len(splitter)):
                ww += "team[" + id + "] = team[" + splitter[j] + "]"
                if j != len(splitter) - 1:
                    ww += " \/ "

            if(count_want_with != count_want_with2):
                ww += ") /\\\n"
            elif(count_want_with == count_want_with2):
                ww += ") \n"

        row_data = {
            "id": id,
            "name": name,
            "status": status,
            "coach": coach,
            "want_with": want_with,
            "service": service,
        }
        form.append(row_data)
    
    json_data_rows += "]"

    json_data_rows = json.loads(json_data_rows)
    # person in a service list
    services = []
    for x in form:
        # check if exists in unique_list or not
        if x["service"] not in services:
            services.append(x['service'])
    

    #list of services
    services_constraint_mzn = ""
    for s in services:
        services_constraint_mzn += "int: service" + str(s) + " = " + str(s) + ";\n"  

    #list of person in each service
    services_people = ""
    for su in services:
        services_people += "            {" 
        for data in form:
            if(data['service'] == su):
                services_people += data["id"] + ","
        services_people += "},\n"

    # constraint team pairing
    pair_str = services_pairing.replace("[", "")
    pair_str = pair_str.replace("]", "")
    pair_str = pair_str.replace("'", "")
    pair_str = pair_str.split(", ")

    constraint_pair = ""
    print(pair_str)
    if(len(pair_str) != 1 and pair_str[0] != ""):
        for p in pair_str:
            arr = p.split(" ")
            if arr[1] == "NOT":
                constraint_pair += "  forall(p" + arr[0] + " in service[service" + arr[0] + "], p" + arr[2] + " in service[service" + arr[2] + "]) (team[p" + arr[0] + "] != team[p" + arr[2] + "]) "
            if p != pair_str[-1]:
                constraint_pair += "/\\\n"
    
    # declare library
    minizinc_code = """include "globals.mzn";\n"""
    
    # persons and its status
    minizinc_code += "\n\nint: num_persons = " + str(num_persons) +";\nset of int: persons = 0..num_persons-1;\n"
    minizinc_code += "array[1..num_persons, 1..2] of int: persons_status = \n"
    minizinc_code += "  array2d(1..num_persons, 1..2, [\n"
    minizinc_code += persons
    minizinc_code += "]);\n\n"

    

    # teams 
    minizinc_code += "\n\nint: num_teams = " + str(num_teams) +";\nset of int: teams = 0..num_teams-1;\n"

    # service
    minizinc_code += "\n% The services\n" + services_constraint_mzn + "\n\n"
    minizinc_code += "int: num_services = " + str(num_services) + ";\n"
    minizinc_code += "array[1..num_services] of set of int: service = [\n"
    minizinc_code += services_people
    minizinc_code += "]; \n"

    # coaching
    minizinc_code += "\n\nint: num_coaching = " + str(coach_count) +";\n"
    minizinc_code += "array[1..num_coaching, 1..2] of int: coaching = \n"
    minizinc_code += "  array2d(1..num_coaching, 1..2, [\n"
    minizinc_code +=  coach_constraint
    minizinc_code += "]);\n\n"

    # teams
    minizinc_code += "array[persons] of var teams: team;\n\n"
    minizinc_code += "array[teams, persons] of var 0..1: team3;\n\n"
    minizinc_code += "solve :: int_search(team, first_fail, indomain_median, complete) satisfy;\n\n\n\n"

    # constraint 

    minizinc_code += "constraint\n\n"

    bool_empty_array = False
    for i in range(0, len(input_max_status)):
        if input_max_status[i] != "" :
            bool_empty_array = True
            break

    if(bool_empty_array == True or (num_max_same != "" and num_max_same != None)):
        minizinc_code += "  forall(t in teams) (\n"

        if(num_max_same != "" and num_max_same != None):
            minizinc_code += "      forall(f in 1..num_services) (\n"
            minizinc_code += "          sum(person in service[f]) ( bool2int(team[person] == t) ) <= " + num_max_same + "\n"
            minizinc_code += "      )\n"
        
        

        if(bool_empty_array == True):
            minizinc_code += "  /\\\n"

        for i in range(0, len(input_max_status)):
            if i != len(input_max_status) - 1 and input_max_status[i] != "" :
                minizinc_code += "      sum(emp_st_"+ str(i) + " in persons where persons_status[emp_st_" + str(i) + "+1,2] ==" + str(i) + ") ( bool2int(team[emp_st_"+ str(i) + "] = t ) )=" + input_max_status[i] +"\n"
                minizinc_code += "      /\\\n"
            elif input_max_status[i] != "":
                minizinc_code += "      sum(emp_st_"+ str(i) + " in persons where persons_status[emp_st_" + str(i) + "+1,2] ==" + str(i) + ") ( bool2int(team[emp_st_"+ str(i) + "] = t ) )=" + input_max_status[i] +"\n"
        minizinc_code += "  )\n"
    minizinc_code += ";\n\n"


    if constraint_pair != "":
        minizinc_code += "constraint\n\n"
        minizinc_code += constraint_pair + "\n"
        minizinc_code += ";\n\n"

    minizinc_code += "constraint\n\n"
    minizinc_code += "  forall(c in 1..num_coaching) (team[coaching[c,1]]==team[coaching[c,2]])\n"
    minizinc_code += ";\n\n"

    if must_code != "":
        minizinc_code += "constraint\n\n"
        minizinc_code += must_code + "\n\n"
        minizinc_code += ";\n\n\n"


    if ww != "":
        minizinc_code += "constraint\n\n"
        minizinc_code += ww + "\n\n"
        minizinc_code += ";\n\n\n"


    # symmetry breaking
    minizinc_code += """constraint
  team[1] = 1 /\\

  forall(t in teams, p in persons) (
      (team[p] = t <-> team3[t, p] = 1)
  )

  /\ % symmetry breaking: ordering of the first person in each team
  let {
    array[1..num_teams] of var persons: mins
  } in
  forall(t in 1..num_teams-1) (
    exists(p in persons) (
       mins[t] = p /\ 
       team3[t,p]=1 /\\
       forall(i in persons where i < p) (
          team3[t, i] = 0
       )
       /\ (p > 1 -> mins[t+1] > mins[t]) 
     )
  )
  /\\
  increasing(mins)

;

output ["{"] ++ [
 "\\\"" ++ "Team " ++ show_int(2, t+1) ++ "\\\" : " ++
    show([p | p in persons where fix(team[p]) = t]) ++ if t!=num_teams-1 then "," else "" endif
  | t in 0..num_teams-1
] ++ ["}"]
;
    
    """

    file = open("team_code.mzn", 'w+')
    file.write(minizinc_code)    
    file.seek(0, os.SEEK_SET)
    file.close()

    result = mnz_teams_building("team_code.mzn")


    solution_list = []

    for x in result:
        # check if exists in unique_list or not
        x = eval(str(x))
        if x not in solution_list:
            solution_list.append(x)
    
    return render_template('result.html', result=solution_list, json_data_rows=json_data_rows, services_data=services_data, statuses=statuses)


@app.route('/result')
def result():
    return render_template('result.html')
 
# ========================================



if __name__ == "__main__":
    app.run()