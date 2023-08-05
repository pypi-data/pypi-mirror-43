from functools import wraps
import sys
import warnings

__author__ = "Sebastian Tilders"
__version__ = "1.0.0"

def deprecated(func):
	""" Decorator which designates functions as deprecated """
	@wraps(func)
	def closure(*args, **kwargs):
		warnings.warn("Python 2.7 support my be dropped in the future", PendingDeprecationWarning, stacklevel=2)
		func(*args, **kwargs);
	if(func.__doc__):
		closure.__doc__ = '@deprecated\r\n' + func.__doc__
	else:
		closure.__doc__ = '@deprecated'
	return closure

def constrain(*types):
	"""
	Used to define type constraints:

	Example:
	
	@constrain(int, str)
	def fun(foo,bar):
	    print(foo,bar)

	causes an argument check if fun is called. If a type mismatch is detected
	@constrain will throw an TypeError Exception like this:

	TypeError: Argument 'a' must be of type 'int'

	If you want to constrain class methods, pay attention that class methods take
	their class instance as their first argument.
	You can constrain them with @constrain(object,...):

	class A:
	    @constrain(object, int, str):
	    def fun(self,foo,bar):
	        print(foo,bar)
	"""
	from inspect import signature
	
	def decorate(func):
		fun_names = list(signature(func).parameters.keys())
		
		@wraps(func)
		def constrained_function(*args, **kwargs):
			all_args = enumerate(args + tuple(kwargs.values()))

			for i,v in all_args:
				if not isinstance(v,types[i]):
					raise TypeError("Argument '{:}' in function '{:}' must be of type '{:}'".format(fun_names[i],func.__name__,types[i].__name__))
			func(*args,**kwargs)
		return constrained_function
	return decorate
