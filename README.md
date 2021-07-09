# FICS


# Download & configure FICS

1. Clone the repository
  - For example: mkdir /home/mansour/code
  - cd /home/mansour/code
  - ```git clone --recurse-submodules https://github.com/RiS3-Lab/FICS.git```
  - cd FICS
2. ```sh install.sh```
3. create a directory as the root of your data (e.g., source code, bitcodes, graphs, etc.)
  - For example: mkdir /home/mansour/data
  - cd /home/mansour/data
  - create a directory inside and name it 'projects': mkdir projects
  - cd /home/mansour/data/projects
4. Modify settings.py and update DATA_DIR to the root of your data
  - For example: DATA_DIR = '/home/mansour/data'
  
# Prepare target codebase

5. In the "projects" directory, clone the source code a codebase you target:
  - For example: git clone https://gitlab.com/libtiff/libtiff.git libtiff-19f6b70
  - cd libtiff-19f6b70
  - git checkout 19f6b70 .
6. Compile the project with clang-3.8 and get compilation database (FICS just supports clang 3.8 and llvm 3.8)
  - For example: cmake -D CMAKE_C_COMPILER="/usr/bin/clang-3.8" -D CMAKE_CXX_COMPILER="/usr/bin/clang++-3.8" .
  - get compilation database: bear make

# Discover the inconsistencies

7. Run FICS on the target codebase:
  - For example: ```sh scripts/get_inconsistencies_real_programs_NN_G2v.sh libtiff-19f6b70 p ns```
  - If you need to run FICS on larger projects like QEMU, change 'ns' to 's'. FICS splits the codebase to submodules
  - *The inconsistencies are saved in mongodb*

# Query the found inconsistencies!!!
8. To query the saved inconsistencies, you need to run the following command:
  - ```python __init__.py -a=QI -p=libtiff-19f6b70 -it=check -f```
  - "-it" argument is inconsistency type and can be: check | call | type | store | order | all
  - if you need to disable filtering, just remove -f


# Analysis Java Program
To analysis Java program, you need to download and install [JLang](https://github.com/polyglot-compiler/JLang). Then use the script [get_inconsistencies_of_java_programs_NN_G2v.sh](./scripts/get_inconsistencies_of_java_programs_NN_G2v.sh) to analysis the Java program. We just modify the generation of bc files and did not modify anything else.
