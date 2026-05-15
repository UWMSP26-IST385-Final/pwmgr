import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import generator

ctk.set_appearance_mode("system")

MIN_ENTROPY = 75.0


class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)

        self.length_var = tk.IntVar(value=16)
        self.min_numbers_var = tk.IntVar(value=1)
        self.min_special_var = tk.IntVar(value=1)
        self.avoid_ambig_var = tk.BooleanVar(value=False)

        self.charsets_vars: dict[generator.CharsetKey, tk.BooleanVar] = {
            "uppercase": tk.BooleanVar(value=True),
            "lowercase": tk.BooleanVar(value=True),
            "numbers": tk.BooleanVar(value=True),
            "special": tk.BooleanVar(value=True),
        }
        self.charset_checkboxes: dict[generator.CharsetKey, ctk.CTkCheckBox] = {}

        self._build_ui()
        self._update_ui()

        for var in [
            self.length_var,
            self.min_numbers_var,
            self.min_special_var,
            self.avoid_ambig_var,
        ]:
            var.trace_add("write", lambda *_: self._update_ui())
        for var in self.charsets_vars.values():
            var.trace_add("write", lambda *_: self._update_ui())

    def _build_ui(self):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # Length
        len_frame = ctk.CTkFrame(f, fg_color="transparent")
        len_frame.pack(fill=tk.X, pady=4)
        ctk.CTkLabel(len_frame, text="Length:").pack(side=tk.LEFT)
        self.length_label = ctk.CTkLabel(len_frame, text="16", width=28)
        self.length_label.pack(side=tk.RIGHT)
        ctk.CTkSlider(
            len_frame,
            from_=14,
            to=64,
            number_of_steps=50,
            variable=self.length_var,
            command=self._on_length,
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=8)

        # Character sets
        ctk.CTkLabel(f, text="Character Sets", anchor="w").pack(fill=tk.X, pady=(12, 2))
        cs_frame = ctk.CTkFrame(f)
        cs_frame.pack(fill=tk.X)
        for key in generator.CHARSETS:
            cb = ctk.CTkCheckBox(
                cs_frame, text=key.capitalize(), variable=self.charsets_vars[key]
            )
            cb.pack(anchor="w", padx=12, pady=2)
            self.charset_checkboxes[key] = cb

        # Requirements
        ctk.CTkLabel(f, text="Requirements", anchor="w").pack(fill=tk.X, pady=(12, 2))
        req_frame = ctk.CTkFrame(f)
        req_frame.pack(fill=tk.X)
        for row, (label, var) in enumerate(
            [
                ("Min Numbers", self.min_numbers_var),
                ("Min Special", self.min_special_var),
            ]
        ):
            ctk.CTkLabel(req_frame, text=label).grid(
                row=row, column=0, sticky="w", padx=8, pady=4
            )
            ctk.CTkEntry(req_frame, textvariable=var, width=60, justify="center").grid(
                row=row, column=1, padx=8, pady=4
            )
        ctk.CTkCheckBox(
            req_frame,
            text="Avoid Ambiguous (I, l, 1, O, 0)",
            variable=self.avoid_ambig_var,
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 10))

        # Entropy status
        self.entropy_label = ctk.CTkLabel(f, text="")
        self.entropy_label.pack(pady=(10, 2))

        # Generate button
        self.gen_btn = ctk.CTkButton(f, text="Generate", command=self._generate)
        self.gen_btn.pack(fill=tk.X, pady=6)

        # Result row
        result_frame = ctk.CTkFrame(f, fg_color="transparent")
        result_frame.pack(fill=tk.X)
        self.result_var = tk.StringVar()
        ctk.CTkEntry(
            result_frame,
            textvariable=self.result_var,
            font=ctk.CTkFont(family="Courier", size=13),
            justify="center",
            state="disabled",
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ctk.CTkButton(result_frame, text="Copy", command=self._copy, width=70).pack(
            side=tk.RIGHT, padx=(8, 0)
        )

    def _on_length(self, value: float):
        self.length_label.configure(text=str(int(value)))

    def _update_ui(self):
        try:
            length = self.length_var.get()
            min_num = self.min_numbers_var.get()
            min_spec = self.min_special_var.get()
        except tk.TclError:
            length = min_num = min_spec = 0

        avoid_ambig = self.avoid_ambig_var.get()
        charset_states: dict[generator.CharsetKey, bool] = {
            k: v.get() for k, v in self.charsets_vars.items()
        }
        selection: set[generator.CharsetKey] = {
            k for k, checked in charset_states.items() if checked
        }

        for key, checked in charset_states.items():
            if checked:
                remaining = selection - {key}
                too_weak = not remaining or not generator.meets_entropy(
                    length, remaining, MIN_ENTROPY, avoid_ambig
                )
                self.charset_checkboxes[key].configure(
                    state="disabled" if too_weak else "normal"
                )
            else:
                self.charset_checkboxes[key].configure(state="normal")

        req_chars = generator.min_required_chars(selection, min_num, min_spec)
        entropy = generator.compute_entropy(selection, length, avoid_ambig)

        if req_chars > length:
            self.entropy_label.configure(
                text=f"Constraints ({req_chars}) exceed length ({length})",
                text_color="red",
            )
            self.gen_btn.configure(state="disabled")
        elif length < 14:
            self.entropy_label.configure(text="Length must be ≥ 14", text_color="red")
            self.gen_btn.configure(state="disabled")
        elif entropy < MIN_ENTROPY:
            self.entropy_label.configure(
                text=f"{entropy:.1f} bits — too weak", text_color="red"
            )
            self.gen_btn.configure(state="disabled")
        else:
            self.entropy_label.configure(text=f"{entropy:.1f} bits", text_color="green")
            self.gen_btn.configure(state="normal")

    def _copy(self):
        if pwd := self.result_var.get():
            self.clipboard_clear()
            self.clipboard_append(pwd)

    def _generate(self):
        try:
            pwd = generator.generate(
                length=self.length_var.get(),
                char_selection={k for k, v in self.charsets_vars.items() if v.get()},
                min_numbers=self.min_numbers_var.get(),
                min_special=self.min_special_var.get(),
                avoid_ambiguous=self.avoid_ambig_var.get(),
            )
            self.result_var.set(pwd)
        except ValueError as e:
            messagebox.showerror("Error", str(e))


def main():
    app = PasswordGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
