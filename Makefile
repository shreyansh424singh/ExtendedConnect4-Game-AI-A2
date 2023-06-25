all:
	python3 -m connect4.ConnectFour ai2 ai connect4/initial_states/tc7.txt --time 5

test:
	clear
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc1.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc2.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc3.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc4.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc5.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc6.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc7.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc8.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc9.txt --time 10
	python3 -m connect4.ConnectFour ai random connect4/initial_states/tc10.txt --time 10

human:
	python3 -m connect4.ConnectFour ai human connect4/initial_states/tc7.txt --time 100

ai:
	python3 -m connect4.ConnectFour ai2 ai connect4/initial_states/tc8.txt --time 100