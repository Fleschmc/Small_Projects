# Cloning

## Table of Contents
 - [Description](#Description)
 - [Usage](#Cloning.py%20usage)
## Description  
  The video game Rust has a farming system. Within is a script that will accept a list of clones (each having six genes) and find the optimal cross breed combination.
  An additional feature allows the script to automatically include the best clones produced by crossbreeding and then rerun the algorithm until no better clones are produced
 
 ## Cloning.py usage  
  In commandline or bash type python Cloning.py (arguments)  
    - Must be in the directory where the script is located or provide path to script  
    
  Arguments:  
    Required:  
    clist: This is the list of clones you want to crossbreed. Type them with one space apart e.g. hhhhhh yyyyyy gggggg  
    ncross_breed: This is the maximum number of clones you want to cross breed with. Bigger numbers will increase run time. Typically 4-6 works well.  
    Optional:  
    -h, --h: Shows help message  
    -g, --generate: Indicates that the function should act generatively. Crossbreed, add best clones, repeat until no new good clones.  
    -d, --depth: The number of new clones to be added with each generation. Only supply a value if using --generate. Default = 5
    
  An example would be Cloning.py hhhhhh yyyyyy gggggg 4 -g -d 7  
  The parser will intuit when you are switching from clist to ncross_breed  
