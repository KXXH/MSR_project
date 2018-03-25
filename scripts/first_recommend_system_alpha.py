# codding=UTF-8
# version=0.0.1
import sqlite3

import tkinter as tk


class UI:
    def __init__(self):
        self.top = tk.Tk()
        self.top.wm_title('测试标签筛选系统')
        self.label1 = tk.Label(self.top, text="language: ")
        self.label1.grid(row=0, sticky=tk.W)
        self.language = tk.Entry(self.top)
        self.language.grid(row=0, column=1, sticky=tk.E)
        self.label2 = tk.Label(self.top, text="topic: ")
        self.label2.grid(row=1, sticky=tk.W)
        self.r_topics = tk.Entry(self.top)
        self.r_topics.grid(row=1, column=1, sticky=tk.E)
        self.ok = tk.Button(self.top, text="OK", command=self.search)
        self.ok.grid(row=3, column=0, columnspan=2)
        self.project_list = tk.Listbox(self.top)
        self.project_list.grid(row=2, sticky=tk.S, columnspan=2)
        self.top.mainloop()

    def search(self):
        print('starting')
        self.project_list.delete(0, tk.END)
        language = self.language.get()
        topics = self.r_topics.get().split(',')
        conn = sqlite3.connect('hot_project_info.db')
        cur = conn.cursor()
        if len(topics) == 1 and topics[0] != '':
            print(topics)
            t = '%' + topics[0] + '%'
            ans = cur.execute('select * from hot_projects where '
                              'language=? and topics like ?', (language, t))
        elif len(topics) > 1:
            print('2')
            t = 'select * from hot_projects where language = \'%s\'' % language
            for topic in topics:
                t = t + ' and topics like \'%' + topic + '%\' '
            # print(t)
            ans = cur.execute(t)
        else:
            print('3')
            ans = cur.execute(
                'select * from hot_projects where language=?', (language,))
        for item in ans:
            # print(type(item))
            self.project_list.insert(tk.END, item[0])


if __name__ == '__main__':
    ui = UI()
