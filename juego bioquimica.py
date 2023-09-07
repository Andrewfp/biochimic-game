import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk, ImageDraw

class Game:
    def __init__(self, window):
        self.window = window
        self.window.title("Guessing Game")
        self.current_level = 0
        self.remaining_attempts = 5
        self.images = ["cell.jpg", "tissue.jpg", "organ.jpg"]
        self.answers = ["Cell", "Tissue", "Organ"]
        self.definitions = {
            "Cell": "A cell is the basic unit of life.",
            "Tissue": "Tissue is a group of cells that perform a specific function.",
            "Organ": "An organ is a structure formed by different types of tissues that work together."
        }
        self.user_answer = tk.StringVar()
        self.feedback_shown = False
        self.initialize_level()

    def initialize_level(self):
        if self.current_level < len(self.images):
            self.image = Image.open(self.images[self.current_level])
            self.image = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(self.window, image=self.image)
            self.image_label.pack()

            self.question_label = tk.Label(self.window, text="What is this?")
            self.question_label.pack()

            self.answer_entry = tk.Entry(self.window, textvariable=self.user_answer)
            self.answer_entry.pack()

            self.guess_button = tk.Button(self.window, text="Guess", command=self.check_answer)
            self.guess_button.pack()
        else:
            self.end_game()

    def check_answer(self):
        correct_answer = self.answers[self.current_level]
        user_answer = self.user_answer.get()
        if user_answer.lower() == correct_answer.lower():
            self.current_level += 1
            self.remaining_attempts = 5
            definition = self.definitions.get(correct_answer, "No definition available.")
            messagebox.showinfo("Correct", f"Correct Answer: {correct_answer}\n\nEnglish Definition:\n{definition}")
            self.image_label.destroy()
            self.question_label.destroy()
            self.answer_entry.destroy()
            self.guess_button.destroy()
            self.feedback_shown = False  # Restablece la bandera
            self.initialize_level()
        else:
            self.remaining_attempts -= 1
            if self.remaining_attempts == 0:
                self.end_game()
            else:
                if not self.feedback_shown:
                    self.user_answer.set("")
                    self.show_incorrect_feedback()
                    self.feedback_shown = True  # Establece la bandera

    def show_incorrect_feedback(self):
        feedback_image = Image.open("incorrect_feedback.jpg")  # Reemplaza "incorrect_feedback.jpg" con la imagen que desees mostrar como retroalimentación
        feedback_image = ImageTk.PhotoImage(feedback_image)

        # Crea una ventana secundaria para mostrar la retroalimentación
        feedback_window = Toplevel(self.window)
        feedback_window.title("Incorrect Feedback")

        feedback_label = tk.Label(feedback_window, image=feedback_image)
        feedback_label.image = feedback_image
        feedback_label.pack()

        self.window.after(1000, lambda: self.hide_feedback(feedback_window, feedback_label))

    def hide_feedback(self, feedback_window, feedback_label):
        feedback_label.pack_forget()
        feedback_window.destroy()  # Cierra la ventana secundaria

        if self.current_level < len(self.images):
            self.image_label.pack()  # Vuelve a mostrar la imagen actual
            self.user_answer.set("")  # Borra la respuesta incorrecta
        self.feedback_shown = False  # Restablece la bandera

    def end_game(self):
        messagebox.showinfo("End of Game", "You have completed the game.")

if __name__ == "__main__":
    main_window = tk.Tk()
    game = Game(main_window)
    main_window.mainloop()
