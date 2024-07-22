import argparse
import pprint

def argparsing():

	parser = argparse.ArgumentParser()
	parser.add_argument('--foo', help='foo help')
	subparsers = parser.add_subparsers(dest='sub', help='sub-command help')
	parser_a = subparsers.add_parser('a', help='a help')
	parser_a.add_argument('bar', type=int, help='bar help')
	parser.add_argument('--foo', dest= 'foo2' ,  help='2nd foo help')
	values = parser.parse_args()
	return values

def args_param(**args):
	return args

#pprint.pprint(argparsing())
pprint.pprint(args_param(a=1,r=2 ,y=3 , o='this'))
