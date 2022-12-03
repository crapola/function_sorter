import argparse
import pathlib
import re


def load_text(path:str)->str:
	with open(path,'r') as file:
		return str.join('',file.readlines())

def parse_arguments()->str:
	parser=argparse.ArgumentParser(description="Sort functions in a Python file.")
	parser.add_argument("Path",type=pathlib.Path,help="Path to .py file.")
	args=parser.parse_args()
	if not args.Path.exists():
		print(args.Path,"not found.")
		return ""
	return args.Path

def save_text(path:str,txt:str):
	with open(path,'w') as file:
		file.writelines(txt)

def main():
	file_path=parse_arguments()
	#file_path="test.py"
	if not file_path:
		return
	txt=load_text(file_path)
	rx=r"\n^def (?P<funcname>\w+)(.|\n(?!^def ))+"
	matches=re.finditer(rx,txt,re.MULTILINE)
	functions=[(m.span(),m.group(1),m.group(0)) for m in matches]
	if not functions:
		print(txt)
		return
	header=txt[:functions[0][0][0]]
	main_function=next((x for x in functions if x[1]=="main"),[])
	if main_function:
		functions.remove(main_function)
		main_function=[main_function]
	sf=sorted(functions,key=lambda tup:tup[1])+main_function
	output=header+''.join(list(zip(*sf))[2])
	assert len(txt)==len(output),"Output has the wrong size."
	print(output)

if __name__=="__main__":
	main()

