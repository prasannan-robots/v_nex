from github import Github
import os

# Class to handle files between flask and github
class git_file_server:

    # Initialing with path_of_upload_folder as the path where the uploaded files will be
    # Needs a environmental variable with GITHUB_TOKEN as the github api token and GITHUB_REPO as the link to the github repository where the files will be stored
    def __init__(self,path_of_upload_folder):
        self.path_of_upload_folder=path_of_upload_folder
        self.token = os.getenv("GITHUB_TOKEN")
        self.github_object = Github(self.token)
        self.branch = "main"
        self.update_files=[]
        self.repository = self.github_object.get_repo(os.getenv("GITHUB_REPO"))
    
    # Intended to push all files in upload_folder to github_repository
    def add_to_update_file(self):
        for filename in os.scandir(self.path_of_upload_folder):
            if filename.is_file():
                self.update_files.append(filename.path)
                f = open(filename.path,"rb")
                content = f.read()
                self.repository.create_file(filename.path,f"Updated {filename.path}",content,branch=self.branch)
                if os.path.exists(filename.path):
                    os.remove(filename.path)

    # Intend to return an array of all files in image directory
    def get_all_filename(self):
        return self.repository.get_contents("images",ref=self.branch)
    
    # Intend to get file content from github
    def get_file_content(self,filename):
        contents = self.repository.get_contents(filename, ref=self.branch)
        return contents.decoded_content.decode()
    
    # Intend to get file and save it in image directory
    def get_file(self,filename):
        file_content=self.get_file_content(filename)
        f=open(filename,"wb")
        f.write(file_content)
    
    # Intend to download all files in image directory
    def get_all_file(self):
        for i in self.get_all_filename():
            self.get_file(i)   
                



# class github_store:
#     def __init__(self,file_path=None):
#         if file_path == None:
#             self.file_path = "chat_log.txt"
#         self.token = os.getenv("GITHUB_TOKEN")
#         self.github_object = Github(self.token)
#         self.branch = "main"
#         self.repository = self.github_object.get_repo("marsha-nicky/my_knowledge")
    
#     def pull_data(self):
#         contents = self.repository.get_contents(self.file_path, ref=self.branch)
#         return contents.decoded_content.decode()

#     def push(self,path=None, message=None, content=None, branch=None, update=False):

#         if path == None:
#             path = self.file_path
#         if message == None:
#             message = "Added chat knowledge"
#         if content == None:
#             content = self.data
#         if branch == None:
#             branch = self.branch

#         source = self.repository.get_branch(branch)
#         if update:  # If file already exists, update it
#             contents = self.repository.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
#             self.repository.update_file(contents.path, message, content, contents.sha, branch=branch)  # Add, commit and push branch
#             print("github_storage : updated content")
#         else:  # If file doesn't exist, create it
#             self.repository.create_file(path, message, content, branch=branch)  # Add, commit and push branch