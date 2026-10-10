import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import os

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

class EmailExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Extractor")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value="emails.txt")

        self._build_ui()

    def _build_ui(self):
        padding = {"padx": 10, "pady": 5}

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)

        tk.Label(self.root, text="Input File:").grid(row=0, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.input_path).grid(row=0, column=1, sticky="we", **padding)
        tk.Button(self.root, text="Browse", command=self.browse_input).grid(row=0, column=2, **padding)

        tk.Label(self.root, text="Output File:").grid(row=1, column=0, sticky="w", **padding)
        tk.Entry(self.root, textvariable=self.output_path).grid(row=1, column=1, sticky="we", **padding)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2, **padding)

        tk.Button(self.root, text="Extract Emails", command=self.extract_emails, width=20).grid(row=2, column=1, pady=10)

        tk.Label(self.root, text="Extracted Emails:").grid(row=3, column=0, sticky="nw", **padding)
        self.result_area = scrolledtext.ScrolledText(self.root, width=70, height=16)
        self.result_area.grid(row=3, column=1, columnspan=2, sticky="nsew", **padding)
        self.count_label = tk.Label(self.root, text="Total: 0")
        self.count_label.grid(row=4, column=1, sticky="w", **padding)

        self.root.rowconfigure(3, weight=1)

    def browse_input(self):
        path = filedialog.askopenfilename(
            title="Select Input Text File",
            filetypes=[("Text Files", "*.txt")]
        )
        if path:
            self.input_path.set(path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Select Output Text File",
            defaultextension=".txt",
            initialfile="emails.txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            self.output_path.set(path)

    def extract_emails(self):
        input_file = self.input_path.get().strip()
        output_file = self.output_path.get().strip()

        if not input_file or not os.path.isfile(input_file):
            messagebox.showerror("Error", "Please select a valid input file.")
            return

        if not output_file:
            messagebox.showerror("Error", "Please select an output file.")
            return

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read input file:\n{e}")
            return

        emails = EMAIL_REGEX.findall(text)
        unique_emails = []
        seen = set()
        for email in emails:
            if email not in seen:
                seen.add(email)
                unique_emails.append(email)

        self.result_area.delete("1.0", tk.END)
        if unique_emails:
            result_text = "\n".join(unique_emails)
            self.result_area.insert(tk.END, result_text)
            self.count_label.config(text=f"Total: {len(unique_emails)}")
        else:
            self.result_area.insert(tk.END, "No email addresses found.")
            self.count_label.config(text="Total: 0")

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(unique_emails))
            messagebox.showinfo("Success", f"Extracted {len(unique_emails)} email(s) and saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save output file:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailExtractorApp(root)
    root.mainloop()
