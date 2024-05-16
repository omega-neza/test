import tkinter as tk
from tkinter import scrolledtext, simpledialog
from tkinter import messagebox
from app import get_answer_for_question, find_best_match, load_knowledge_base, save_knowledge_base

class ChatBotApp:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot")

        self.knowledge_base = load_knowledge_base('knowledge_base.json')

        self.label = tk.Label(master, text="You:")
        self.label.grid(row=0, column=0, sticky='w')

        self.user_input = tk.Entry(master, width=50)
        self.user_input.grid(row=0, column=1)

        self.conversation_history = scrolledtext.ScrolledText(master, width=60, height=15, state='disabled')
        self.conversation_history.grid(row=1, columnspan=2)

        self.ask_button = tk.Button(master, text="Ask", command=self.ask_question)
        self.ask_button.grid(row=2, columnspan=2)

    def ask_question(self):
        user_question = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)

        if user_question.lower() == 'quit':
            self.master.quit()
            return

        best_match = find_best_match(user_question, [q["question"] for q in self.knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, self.knowledge_base)
            self.update_conversation(f'You: {user_question}\nBot: {answer}\n')
        else:
            self.update_conversation(f'You: {user_question}\nBot: I don\'t know the answer. Can you teach me?\n')

            if messagebox.askyesno("Teach Bot", "Do you want to teach me the answer?"):
                new_answer = simpledialog.askstring("Input", "Type the answer:")
                if new_answer:
                    self.knowledge_base["questions"].append({"question": user_question, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', self.knowledge_base)
                    self.update_conversation(f'Bot: Thank you! I learned a new response!\n')

    def update_conversation(self, text):
        self.conversation_history.configure(state='normal')
        self.conversation_history.insert(tk.END, text)
        self.conversation_history.configure(state='disabled')
        self.conversation_history.yview(tk.END)

def main():
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
