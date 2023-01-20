include "globals.mzn"; 

int: num_persons = 60;
set of int: persons = 0..num_persons-1;
int: num_teams = 10;
set of int: teams = 1..num_teams;

% The services
int: A = 1;
int: B = 2;
int: C = 3;
int: D = 4;
int: E = 5;
int: F = 6;

int: num_services = 6;
array[1..num_services] of set of int: service = 
   [
      0..19, % Service A
     20..39, %         B 
     40..44, %         C
     45..49, %         D
     50..54, %         E
     55..59  %         F
   ];

int: num_coaching = 20;
%  (coach, coached)
array[1..num_coaching, 1..2] of int: coaching = 
  array2d(1..num_coaching, 1..2, [
         0, 1,
         2, 3,
         4, 5,
         6, 7,
         8, 9,
        10,11,
        20,21,
        22,23,
        24,25,
        26,27,
        28,29,
        30,31,
        40,41,
        42,43,
        45,46,
        47,48, 
        50,51,
        52,53,
        55,56,
        57,58
    ]);



array[persons] of var teams: team;
array[teams, persons] of var 0..1: team3;

% solve satisfy;
solve :: int_search(
                      team, 
                      first_fail, 
                      indomain_median, 
                      complete) satisfy;


constraint

  forall(t in teams) (

     sum(existingemployee in persons where existingemployee mod 2 = 1) (
            bool2int(team[existingemployee] = t )
     ) = 3 

     /\

     sum(newemployee in persons where newemployee mod 2==0) ( 
            bool2int(team[newemployee]=t)
     ) = 3 

     /\
     forall(f in 1..num_services) (
       sum(person in service[f]) ( bool2int(team[person] == t) ) <=4 
     )
  )

  /\
 
  forall(pA in service[A], pB in service[B]) (team[pA] != team[pB]) /\
  forall(pE in service[E], pF in service[F]) (team[pE] != team[pF]) /\
  
  forall(c in 1..num_coaching) (team[coaching[c,1]]==team[coaching[c,2]]) /\
  
  (team[5] = team[41] \/ team[5] = team[51]) /\

  (team[15] = team[40] \/ team[15] = team[51]) /\
  
  (team[25] = team[24] \/ team[25] = team[50]) /\

;

constraint
  team[0] = 1 /\

  forall(t in teams, p in persons) (
      (team[p] = t <-> team3[t, p] = 1)
  )

  /\ % symmetry breaking: ordering of the first person in each team
  let {
    array[1..num_teams] of var persons: mins
  } in
  forall(t in 1..num_teams) (
    exists(p in persons) (
       mins[t] = p /\ 
       team3[t,p]=1 /\
       forall(i in persons where i < p) (
          team3[t, i] = 0
       )
       /\ (p > 1 -> mins[t] > mins[t-1]) 
     )
  )
  /\
  increasing(mins)

;


output [
 "Team " ++ show_int(2, t) ++ ": " ++
    show([p | p in persons where fix(team[p]) = t]) ++ "\n"
  | t in 1..num_teams
]
;
