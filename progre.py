import subprocess
import tkinter as tk
from tkinter import scrolledtext

# List of languages
LANGUAGES = ['en', 'et', 'ru']


# Function to run a Django command
def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


# Function for the 'makemigrations' command
def makemigrations():
    output = run_command('python manage.py makemigrations')
    append_output("Makemigrations", output)


# Function for the 'migrate' command
def migrate():
    output = run_command('python manage.py migrate')
    append_output("Migrate", output)


# Function for the 'makemessages' command for all languages
def makemessages():
    outputs = []
    for lang in LANGUAGES:
        output = run_command(f'python manage.py makemessages -l {lang}')
        outputs.append(f"Language {lang}:\n{output}\n")
    append_output("Makemessages", "\n".join(outputs))


# Function for the 'compilemessages' command
def compilemessages():
    output = run_command('python manage.py compilemessages')
    append_output("Compilemessages", output)


# Function for the 'test' command
def runtests():
    output = run_command('python manage.py test')
    append_output("Run Tests", output)


# Function for the 'collectstatic' command
def collectstatic():
    output = run_command('python manage.py collectstatic --noinput')
    append_output("Collectstatic", output)


# Function to append command output to the Text widget
def append_output(command, output):
    text_output.insert(tk.END, f"\n{command}:\n{output}\n")
    text_output.see(tk.END)


# Main window
root = tk.Tk()
root.title("Django Command Runner")

# Create buttons for each command
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn_makemigrations = tk.Button(root, text="Makemigrations", command=makemigrations)
btn_makemigrations.pack(pady=10)

btn_migrate = tk.Button(root, text="Migrate", command=migrate)
btn_migrate.pack(pady=10)

btn_makemessages = tk.Button(root, text="Makemessages", command=makemessages)
btn_makemessages.pack(pady=10)

btn_compilemessages = tk.Button(root, text="Compilemessages", command=compilemessages)
btn_compilemessages.pack(pady=10)

btn_runtests = tk.Button(root, text="Run Tests", command=runtests)
btn_runtests.pack(pady=10)

btn_collectstatic = tk.Button(root, text="Collectstatic", command=collectstatic)
btn_collectstatic.pack(pady=10)

output_label = tk.Label(root, text="Command Output")
output_label.pack(pady=5)

# Create a scrolled text widget to display command output
text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
text_output.pack(pady=10)

# Button for clearing output
btn_clear = tk.Button(root, text="Clear Output", command=lambda: text_output.delete(1.0, tk.END))
btn_clear.pack(pady=10)

# Run the main loop
root.mainloop()
