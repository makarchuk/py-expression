import re

float_pattern = re.compile(r"(-?\d*(\.(?=\d))?\d+)")
var_pattern = re.compile(r"([a-zA-Z_]+)")

class Tree(object):
	def __init__(self, node, left=None, right=None):
		self.node = node
		self.left = left
		self.right = right

	def print_branch(self, el, l):
		if el:
			if callable(getattr(el, "print_tree", None)):
				el.print_tree(l+1)
			else:
				print "\t"*(l+1)+str(el)

	def print_node(self):
		return str(self.node)

	def print_tree(self, l=0):
		print "\t"*l + self.print_node()
		self.print_branch(self.left, l)
		self.print_branch(self.right, l)


class Expression(Tree):

	def print_node(self):
		return str(self.node)+"\t"+str(self.type)

	def __init__(self, node=None, left=None, right=None, line=None, number=None, var=None, type=None):
		if type:
			self.type = type
		else:
			#print [node, left, right, line, number, var, type]
			pass
		if line or number or var:
			if line:
				obj = self.parse_expression(line)[0]
				self.node = obj.node
				self.left = obj.left
				self.right = obj.right
				self.type = obj.type
			else:
				self.left = None
				self.right = None
				if number:
					self.type = "number"
					self.node = float(number)
				else:
					self.type = "variable"
					self.node = var
		else:
			super(Expression, self).__init__(node, left, right)


	def parse_expression(self, expr, avail_operations=["-","+","*","^"]):
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
			def get_expression(expr):
				def cut_match(expr, match):
					token = match.group(0)
					rest = expr[match.end(0):]
					return token, rest.strip()

				def get_brackets_content(line):
					c = 0
					for i, x in enumerate(line):
						if x =="(":
							c+=1
						elif x ==")":
							c-=1
						if c<0:
							raise ValueError("Wrong expressions(check your brackets)")
						if c == 0:
							return line[1:i], line[i+1:]						

				fl_match = float_pattern.match(expr)
				if fl_match:
					num, expr = cut_match(expr, fl_match)
					return Expression(number=num), expr
				var_match = var_pattern.match(expr)
				if var_match:
					var, expr = cut_match(expr, var_match)
					return Expression(var=var), expr
				if expr.startswith('('):
					br_content, expr = get_brackets_content(expr)
					return Expression(line = br_content), expr
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

		built_expr = left_token
		if expr:
			operation, expr = get_token(expr, "operation")
			while expr:
				if operation in avail_operations:
					av = available_operations(operation)
					right_branch, new_opeartion, expr = self.parse_expression(expr, avail_operations=av)
					built_expr = Expression(operation, built_expr, right_branch, type="operation")
					operation = new_opeartion
				else:
					return built_expr, operation, expr
		else:
			built_expr = left_token
		return built_expr, None, None


expr = "(x^3 - x)^2*(x+168)*(123x-27+18*(24x^2-6)^4) + 1+x"
print expr
expr = Expression(line = expr)
expr.print_tree()