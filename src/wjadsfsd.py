import tkinter as tk
from PIL import Image, ImageTk
import time
 
class TerminalSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set the window size and geometry
        self.geometry("570x343")  # Set window size
        self.title("Terminal")
 
        # Set the title with the desired format: "georgeyanyan.xu — -bash — 80x24"
        self.title("georgeyanyan.xu — -bash — 80x24")
 
        # Load the folder icon and set it as the window icon
 
 # Update with actual folder icon path
        try:
            folder_icon = folder_icon.resize((850, 850))
            folder_icon_image = ImageTk.PhotoImage(folder_icon)
 
            # Set the icon in tkinter (use wm_iconphoto)
            self.wm_iconphoto(True, folder_icon_image)
 
            # Store the reference to avoid garbage collection
            self.icon_ref = folder_icon_image
        except Exception as e:
            
            print(f"Error loading icon: {e}")
            pass
 
        # Rest of your TerminalSimulator code...
        self.terminal_display = tk.Text(
            self, wrap=tk.WORD, font=("Menlo", 11), bg='white', fg='black',
            insertbackground='white', borderwidth=4, highlightthickness=0
        )
        self.terminal_display.pack(expand=True, fill='both', padx=0, pady=0)
 
        # Bind keys to handle preventing deletions before prompt
        self.terminal_display.bind("<BackSpace>", self.handle_backspace)
        self.terminal_display.bind("<Delete>", self.handle_backspace)
 
        # Enable capturing of key presses directly within the terminal area
        self.terminal_display.bind("<Return>", self.handle_command)
 
        # Simulate user entering sudo password
        self.password_mode = False
        self.attempts = 0  # Track the number of attempts
        self.correct_password = "admin123"  # Define the correct password
        self.typed_password = ""  # Store the typed password
 
        # Insert custom startup message (based on the image you provided)
        self.insert_startup_message()
 
        self.prompt = "FVFG2KRFQ6L4:~ georgeyanyan.xu$ "
        self.insert_text(self.prompt)
 
        # Create a tag to hide password input by changing its color to white
        self.terminal_display.tag_configure("hidden", foreground="white")
        self.terminal_display.tag_configure("visible", foreground="black")  # Normal text
 
    def insert_text(self, text, tag="visible"):
        self.terminal_display.insert(tk.END, text, tag)
        self.terminal_display.yview(tk.END)
 
    def insert_startup_message(self):
        # Custom startup message
        last_login_time = time.strftime("%a %b %d %H:%M:%S", time.localtime())
        startup_message = (
            f"Last login: {last_login_time} on ttys002\n\n"
            "The default interactive shell is now zsh.\n"
            "To update your account to use zsh, please run `chsh -s /bin/zsh`.\n"
            "For more details, please visit https://support.apple.com/kb/HT208050.\n"
        )
        self.insert_text(startup_message)
 
    def get_last_command(self):
        # Get the text after the last prompt (to capture user input)
        content = self.terminal_display.get("1.0", tk.END)
        last_command_index = content.rfind(self.prompt)
        command = content[last_command_index + len(self.prompt):].strip()
        return command
 
    def handle_command(self, event):
        if self.password_mode:
            # Capture typed password during password prompt
            self.handle_password_entry()
        else:
            command = self.get_last_command()
 
            if command == 'exit':
                self.quit()
                return "break"  # Stops the extra newline from appearing
 
            # Simulate the behavior if the command starts with 'sudo'
            if command.startswith("sudo"):
                self.simulate_sudo_command(command)
            else:
                # For non-sudo commands, simulate a 'command not found' bash message
                self.insert_text(f"\n-bash: {command}: command not found\n")
                self.insert_text(self.prompt)  # Insert a new prompt after handling
 
        return "break"  # Prevents the Text widget from adding an extra newline
 
    def simulate_sudo_command(self, command):
        self.insert_text("\nPassword:")  # Simulate password prompt for sudo
        self.insert_key_icon()  # Insert the key icon image
        self.password_mode = True  # Enter password mode
 
        # Bind typing to dynamically apply the hidden tag to the password input
        self.terminal_display.bind("<KeyPress>", self.handle_password_input)
 
        # Start tracking where the password will be typed
        self.password_start_index = self.terminal_display.index(tk.INSERT)
 
    def insert_key_icon(self):
        # Load the key icon image from the specified path
        image = Image.open("/Users/georgeyanyan.xu/Desktop/Key/Key.png")  # Update the filename if necessary
        image = image.resize((11, 15), resample=Image.Resampling.LANCZOS)  # Adjust the size if needed
        photo = ImageTk.PhotoImage(image)
 
        # Insert the image at the current end of the text widget (where Password: ends)
        self.key_image_id = self.terminal_display.image_create(tk.END, image=photo)
 
        # Force the cursor to move to the end after the image
        self.terminal_display.mark_set(tk.INSERT, tk.END)
 
        # Ensure the view follows the cursor
        self.terminal_display.yview(tk.END)
 
        self.terminal_display.image = photo  # Keep a reference to avoid garbage collection
        self.terminal_display.mark_set(tk.INSERT, tk.END)
 
    def delete_key_icon(self):
        """Delete the key icon from the terminal display after second input or success."""
        if self.key_image_id:
            self.terminal_display.delete(self.key_image_id)  # Remove the image using its ID
            self.key_image_id = None  # Reset the reference
 
 
    def handle_password_input(self, event):
        """Handle password input and immediately hide characters."""
        # Prevent default character insertion
        if len(self.terminal_display.get(self.password_start_index, tk.INSERT)) < 12:
            # Manually insert the character at the current insertion point
            self.terminal_display.insert(tk.INSERT, event.char)
            # Apply the hidden tag to hide the character
            password_end_index = f"{self.password_start_index} +12c"
            self.terminal_display.tag_add("hidden", self.password_start_index, password_end_index)
        return "break"  # Stop default event handling to prevent the character from showing
 
    def handle_password_entry(self):
        # Get typed password (the text after "Password: ")
        content = self.terminal_display.get("3.0", tk.END)
        last_password_prompt = content.rfind("Password:")
        typed_password = content[last_password_prompt + len("Password:"):].strip()
 
        # Record the typed password for checking accuracy later
        self.typed_password = typed_password
        print(f"Typed password: {self.typed_password}")  # You can see what was typed
 
        # Compare the typed password with the correct password
        if self.attempts == 0:
            self.insert_text("\nSorry, try again.\nPassword:")
            self.insert_key_icon()  # Re-insert the key icon for the second password prompt
            self.attempts += 1
        elif self.attempts == 1:
            self.insert_text("\n")
            self.delete_key_icon() 
            self.password_mode = True  # Exit password mode
            self.terminal_display.unbind("<KeyPress>")  # Unbind the key hiding after password mode is done
            self.insert_text(self.prompt)  # Show the prompt after handling the password
 
 
 
    def handle_backspace(self, event):
        """Prevent backspace/delete before the prompt or in password mode."""
        cursor_index = self.terminal_display.index(tk.INSERT)
 
        # Prevent backspace if in password mode
        if self.password_mode:
            return "break"  # Disable backspace during password entry
 
        # Find the index of the last prompt
        prompt_index = self.terminal_display.search(self.prompt, "1.0", tk.END, backwards=True)
 
        if prompt_index:
            # Calculate the end index of the prompt (where the user input starts)
            prompt_end_index = self.terminal_display.index(f"{prompt_index} + {len(self.prompt)}c")
 
            # If the cursor is at or before the prompt, disallow deletion
            if self.terminal_display.compare(cursor_index, "<=", prompt_end_index):
                return "break"
 
        # Allow normal backspace behavior
        return None
 
 
if __name__ == "__main__":
    app = TerminalSimulator()
    app.mainloop()