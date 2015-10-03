import re

float_pattern = re.compile(r"(-?\d*(\.(?=\d))?\d+)")
var_pattern = re.compile(r"([a-zA-Z_]+)")

class Tree:
	def __init__(self, node, left=None, right=None):
		if isinstance(node, Tree):
			self.node = node.node
			self.left = node.left
			self.right = node.right
		else:
			self.node = node
			self.left = left
			self.right = right

	def print_branch(self, el, l):
		if el:
			if callable(getattr(el, "print_tree", None)):
				el.print_tree(l+1)
			else:
				print "\t"*(l+1)+str(el)

	def print_tree(self, l=0):
		print "\t"*l+str(self.node)
		self.print_branch(self.left, l)
		self.print_branch(self.right, l)


def parse_expression(expr, avail_operations=["-","+","*","^"]):
	operations=["-","+","*","^"]
	def available_operations(op):
		ops = operations[:]
		if op == "+":
			return ["+", "*", "^"]
		elif op in "*-":
			return ["*", "^"]
		else:
			return ["^"]


	def get_token(expr, state="expr"):

		def cut_match(expr, match):
			token = match.group(0)
			rest = expr[match.end(0):]
			return token, rest.strip()

		def get_expression(expr):
			def get_brackets_content(line):
				c = 0
				for i, x in enumerate(line):
					if x =="(":
						c+=1
					elif x ==")":
						c-=1
					if c<0:
						print line
						raise ValueError("Wrong expressions(check your brackets)")
					if c == 0:
						return line[1:i], line[i+1:]						

			fl_match = float_pattern.match(expr)
			if fl_match:
				return cut_match(expr, fl_match)
			var_match = var_pattern.match(expr)
			if var_match:
				return cut_match(expr, var_match)
			if expr.startswith('('):
				br_content, expr = get_brackets_content(expr)
				return parse_expression(br_content)[0], expr
			if expr.startswith("-"):
				return -1, expr[1:]
			print "EXPR:", expr
			raise BaseException("Can't match token")

		def get_operation(expr):
			for op in operations:
				if expr.startswith(op):
					return op, (expr[len(op):]).strip()
			return "*", expr

		expr = expr.strip()
		if state=="expr":
			return get_expression(expr)
		elif state=="operation":
			return get_operation(expr)
		else:
			print state
			raise BaseException("Incorrect State!")

	left_token, expr = get_token(expr, "expr")

	built_expr = Tree(left_token)

	operation, expr = get_token(expr, "operation")

	while expr:
		if operation in avail_operations:
			av = available_operations(operation)
			right_branch, new_opeartion, expr = parse_expression(expr, avail_operations=av)
			built_expr = Tree(operation, built_expr, right_branch)
			operation = new_opeartion
		else:
			return built_expr, operation, expr
	return built_expr, None, None


#print Tree('A').__class__==Tree
expr = "(x^3 - x)^2*(x+168)*(123x-27+18*(24x^2-6)^4) + 1+x"
print expr
expr = parse_expression(expr)[0]
expr.print_tree()