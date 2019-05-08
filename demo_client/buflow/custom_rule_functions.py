from bubble3.functions import register, trace,timer

@timer
@trace
def replace(inp,s,r):
    return inp.replace(s,r)
    #yield inp.replace(s,r)

#adder=lambda *a:[]
#register(adder)
def replace_hello_with_goodbye(inp):
    return replace(inp,'Hello','Goodbye')
register(replace_hello_with_goodbye) #alias
#register(replace_hello_with_goodbye,'say_goodbye') #alias

register(replace)
register(replace,'s') #alias  sed 's///'
