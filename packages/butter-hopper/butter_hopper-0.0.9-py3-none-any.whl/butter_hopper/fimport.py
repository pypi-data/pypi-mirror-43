## fimport


"""
    Functional import in Python
    Everything is implicit.

"""


"""
    Usage:
    ```
    same as import utils_base
    fimport('from utils_base')

    same as import utils_base but renamed. 
    fimport('* as alias from utils_base') 

    import a single exported name
    fimport('{ exported_name } from utils_base') ;
    ```

    In the file you wanna exports use decorators :3
    @fexport(type=EXPORTS.FUNC)
    def my_function() :
        return 2+2
    
    @fexport(type=EXPORTS.CLASS)

"""