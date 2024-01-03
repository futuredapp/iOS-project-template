import os
import glob
import fileinput

def update_fastfile_env_variables(file_path, var_name, new_value):
    if not os.path.isfile(file_path):
        print(f"File does not exist: {file_path}")
        return

    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            if f"ENV['{var_name}']" in line:
                line = f"ENV['{var_name}'] = '{new_value}'\n"
            print(line, end='')

def rename_files_and_directories_in_directory(dir_path, old_text, new_text):
    if not os.path.isdir(dir_path):
        print(f"Directory does not exist: {dir_path}")
        return

    for root, dirs, files in os.walk(dir_path):
        for dir_name in dirs:
            if old_text in dir_name:
                old_dir_path = os.path.join(root, dir_name)
                new_dir_name = dir_name.replace(old_text, new_text)
                new_dir_path = os.path.join(root, new_dir_name)
                os.rename(old_dir_path, new_dir_path)
                # Recursive call for subdirectories
                rename_files_and_directories_in_directory(new_dir_path, old_text, new_text)

        for file_name in files:
            if old_text in file_name:
                old_file_path = os.path.join(root, file_name)
                new_file_name = file_name.replace(old_text, new_text)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)

def replace_text_in_all_files_in_directory(dir_path, old_text, new_text):
    if not os.path.isdir(dir_path):
        print(f"Directory does not exist: {dir_path}")
        return

    for file_path in glob.glob(os.path.join(dir_path, '*')):
        if os.path.isfile(file_path):
            with fileinput.FileInput(file_path) as file:
                for line in file:
                    print(line.replace(old_text, new_text), end='')

def get_names_of_app_and_package():
    app_name = input("Project name: ")
    if not app_name:
        print("You need to enter a name")
        exit(1)

    package_name = input("Package name (e.g. com.example.test): ")
    if not package_name:
        print("You need to enter a package name")
        exit(1)

    if package_name.count('.') != 2:
        print("You did not enter the package name correctly")
        exit(1)

    return app_name, package_name

def replace_text_in_xcodeproj(file_path, old_text, new_text):
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: {file_path}")

    # Open and read the file data
    with open(file_path, "r") as file:
        file_data = file.read()

    # Replace the text
    file_data = file_data.replace(old_text, new_text)

    # Write the changes back to the file
    with open(file_path, "w") as file:
        file.write(file_data)


# Main script

# Get app name and package name
app_name, package_name = get_names_of_app_and_package()

# Update values in Fastfile
update_fastfile_env_variables("fastlane/Fastfile", "APP_IDENTIFIER", package_name)
update_fastfile_env_variables("fastlane/Fastfile", "APP_NAME", app_name)
update_fastfile_env_variables("fastlane/Fastfile", "APP_SCHEME", app_name)

# Update values in pbxproj file
replace_text_in_xcodeproj("Template.xcodeproj/project.pbxproj", "app.futured.Template", package_name)
replace_text_in_xcodeproj("Template.xcodeproj/project.pbxproj", "app.futured.TemplateTests", f"{package_name}Test")
replace_text_in_xcodeproj("Template.xcodeproj/project.pbxproj", "app.futured.TemplateUITests", f"{package_name}.UITest")

# Replace text in all files in root directory
replace_text_in_xcodeproj("Template.xcodeproj/project.pbxproj", "Template", app_name)
replace_text_in_all_files_in_directory(".", "Template", app_name)

# Rename directories
rename_files_and_directories_in_directory(".", "Template", app_name)
