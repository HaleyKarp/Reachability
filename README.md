## Instructions
To install `tree_sitter` in your conda environment, please run 

    `conda install -c conda-forge tree_sitter_languages` 

Once, installed, running this little `tree_sitter` test environment is easy! Simply run the `test_env.py` file with the file of the code you'd like to parse, the language of the file you are testing, and an output filename. The output file of this program will contain each node from the root level and its children. 
    
     `python3 test_env.py <file.ext> <language> -o <output_filename>`

There is a file called `toy_code.py` for you to test with and an outputfile called `test_out.json` to give you an idea of what the output file will look like. You can run it like this,

    `python3 test_env.py toy_code.py python -o test_out`


*Please note, this test environment only takes `python` and `go` languages for now.* 
*It is necessary to use `python3` when running this code, running `python` will not work.*