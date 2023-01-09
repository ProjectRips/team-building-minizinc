include "globals.mzn";


int: num_persons = 60;
set of int: persons = 0..num_persons-1;
array[1..num_persons, 1..2] of int: persons_status = 
  array2d(1..num_persons, 1..2, [
        0,0,
        1,1,
        2,0,
        3,1,
        4,0,
        5,1,
        6,0,
        7,1,
        8,0,
        9,1,
        10,0,
        11,1,
        12,0,
        13,1,
        14,0,
        15,1,
        16,0,
        17,1,
        18,0,
        19,1,
        20,0,
        21,1,
        22,0,
        23,1,
        24,0,
        25,1,
        26,0,
        27,1,
        28,0,
        29,1,
        30,0,
        31,1,
        32,0,
        33,1,
        34,0,
        35,1,
        36,0,
        37,1,
        38,0,
        39,1,
        40,0,
        41,1,
        42,0,
        43,1,
        44,0,
        45,1,
        46,0,
        47,1,
        48,0,
        49,1,
        50,0,
        51,1,
        52,0,
        53,1,
        54,0,
        55,1,
        56,0,
        57,1,
        58,0,
        59,1,
]);



int: num_teams = 10;
set of int: teams = 0..num_teams-1;

% The services
int: service1 = 1;
int: service2 = 2;
int: service3 = 3;
int: service4 = 4;
int: service5 = 5;
int: service6 = 6;


int: num_services = 6;
array[1..num_services] of set of int: service = [
            {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,},
            {20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,},
            {40,41,42,43,44,},
            {45,46,47,48,49,},
            {50,51,52,53,54,},
            {55,56,57,58,59,},
]; 


int: num_coaching = 20;
array[1..num_coaching, 1..2] of int: coaching = 
  array2d(1..num_coaching, 1..2, [
       1,0,
       3,2,
       5,4,
       7,6,
       9,8,
       11,10,
       21,20,
       23,22,
       25,24,
       27,26,
       29,28,
       31,30,
       41,40,
       43,42,
       45,46,
       47,48,
       51,50,
       53,52,
       55,56,
       57,58,
]);

array[persons] of var teams: team;

array[teams, persons] of var 0..1: team3;

solve :: int_search(team, first_fail, indomain_median, complete) satisfy;



constraint

  forall(t in teams) (
      forall(f in 1..num_services) (
          sum(person in service[f]) ( bool2int(team[person] == t) ) <= 4
      )
  )
;

constraint

  forall(p1 in service[service1], p2 in service[service2]) (team[p1] != team[p2]) /\
  forall(p5 in service[service5], p6 in service[service6]) (team[p5] != team[p6]) 
;

constraint

  forall(c in 1..num_coaching) (team[coaching[c,1]]==team[coaching[c,2]])
;

constraint

 
 (team[5] = team[41] \/ team[5] = team[51]) /\
 
 (team[15] = team[40] \/ team[15] = team[51]) /\
 
 (team[25] = team[24] \/ team[25] = team[50]) 


;


constraint
  team[1] = 1 /\

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
       team3[t,p]=1 /\
       forall(i in persons where i < p) (
          team3[t, i] = 0
       )
       /\ (p > 1 -> mins[t+1] > mins[t]) 
     )
  )
  /\
  increasing(mins)

;

output ["{"] ++ [
 "\"" ++ "Team " ++ show_int(2, t+1) ++ "\" : " ++
    show([p | p in persons where fix(team[p]) = t]) ++ if t!=num_teams-1 then "," else "" endif
  | t in 0..num_teams-1
] ++ ["}"]
;
    
    