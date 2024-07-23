# prefetchparser
A simple script to parse Prefetch artifacts and save the output to CSV file. This is part of my automation script during Incident Response or Digital Forensics examinations, sometimes we need to check this artifact where Prefetch files can reveal the execution of unknown or suspicious executables, which may indicate malware or unauthorized software. These Prefetch files provide a record of which programs have been executed on a system. This helps forensic analysts determine the usage of specific applications.

## How to Use
Instructions to Use the Script:

- Save the script as prefetchparser.py.
- Open a terminal or command prompt.
- Navigate to the directory where the script is saved.
- Run the script using the following command:

   `python3 prefetchparser.py <inputfolder> <outputfolder>`

Replace <input_folder> with the path to your folder containing Prefetch files and <output_folder> with the path to the folder where you want the CSV file to be saved.

# Help Output
To see the help message and usage instructions, you can run:

`python prefetchparser.py --help`

# Prefetch Paths
Here are the paths that we should take a look at to find these artifacts.
```
C:\Windows\Prefetch
```

# Example of Commands
Here are the paths that we should take a look at to find these artifacts.
```
python3 prefetchparser.py C:\ D:\pretech_report\
```
