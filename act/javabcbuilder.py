import subprocess
from act import Act
from sample.projectcode import ProjectCode
from utils.inout import *
from subprocess import call


class JAVABCBuilder(Act):
    def start(self):
        projects_dir = join_path(self.arguments.data_dir, self.arguments.projects_dir)
        dir_names = get_directories(projects_dir)
        for dir_name in dir_names:
            for project_name in self.arguments.projects:
                if get_basename(dir_name) == project_name or len(self.arguments.projects) == 0:
                    print 'Analyzing {}'.format(get_basename(dir_name))
                    self.arguments.current_project = project_name
                    project_code = ProjectCode(project_dir=dir_name, arguments=self.arguments)
                    if self.arguments.prepare:
                        project_code.prepare_bc()
                    else:
                        project_code.retrieve_bc_for_java()
			# pass

                    project_bc_dir = join_path(self.arguments.data_dir, self.arguments.bcs_dir, project_name)
		    ll_files = get_files_in_dir(str(project_bc_dir), ext='.ll')
                    for ll_file in ll_files:
			java_file_dir = str(ll_file).replace('.ll', '.java')
			make_dir_if_not_exist(java_file_dir)
			ll_file_name = get_basename(ll_file)
                        parent_dir = get_parent_dir(ll_file)
			if not str(parent_dir).endswith('.java'):
			    parent_dir = java_file_dir
			    try:
				call(['mv', ll_file, str(parent_dir) + '/' + ll_file_name], stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT, close_fds=True)
				ll_file = join_path(java_file_dir, ll_file_name)
			    except:
				print 'crash in mv ll file'
				continue
			bc_file = join_path(parent_dir, ll_file_name.replace('.ll', '.bc'))
			# print 'll file: ', str(ll_file)
			# print 'bc file: ', str(bc_file)
                        llvm_as_log_file = join_path(parent_dir, 'llvm-as.log.txt')
                        function_names_file = join_path(parent_dir, 'functions.txt')
                        llvm_as = 'llvm-as'
                        LOG = open(llvm_as_log_file, 'w')
                        try:
                            call([llvm_as, ll_file, '-o', bc_file], stdout=LOG, stderr=subprocess.STDOUT, close_fds=True)
                        except:
			    print 'crash in llvm_as', str(ll_file)
			functions = open(function_names_file, 'w')
			lines = read_lines(ll_file)
			functions_name = []
			prev_line = ''
			for line in lines:
			    if line[0:6] == 'define':
				functions_name.append(line + prev_line + '\n')
			    prev_line = line
			functions.writelines(functions_name)

