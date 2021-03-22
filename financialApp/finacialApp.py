from tkinter import *
from datetime import date
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinter import messagebox

class myApp(object):
    def __init__(self,user):
        ##This is variables and data used in the program
        self.jsonFile = user
        self.currentDate = date.today()
        self.isDateInList = False
        for dates in user['data']:
            if(dates['date'] == str(self.currentDate)):
                self.userInfo = {"userName":user['userName'], "balance":dates['balance'], "expenses":dates['expenses'], "budget":dates['budget'], "credits":dates['credits'], "savings":dates['savings']}
                self.isDateInList = True
                break
        if not self.isDateInList:
            self.userInfo = {"userName": user['userName'], "balance":user['data'][-1]['balance'], "expenses":0.0, "budget":user['data'][-1]['budget'], "credits":user['data'][-1]['credits'], "savings":user['data'][-1]['savings']}
        self.listValues = list(self.userInfo.values())
        self.listKeys = list(self.userInfo.keys())
        self.colorValues = ['#fcdf87','#f68741','#10133a','#ef0195','#1b96f3']
        self.listValues.pop(0)
        self.listKeys.pop(0)
        
        ## This is set up for the window.
        ## It is all labels and entries
        self.root = Tk()
        self.root.geometry('500x300')
        self.root.title('Finance App')
        self.root.minsize(1000,600)
        self.graphFrame = LabelFrame(self.root,text="Total money graph: ")
        self.graphFrame.grid(row=2, column=5, sticky=E, rowspan=5)
        self.welcomeLabel = Label(self.root, text="Welcome: "+self.userInfo["userName"])
        self.balanceLabel = Label(self.root, text="Balance: %.2f"%self.userInfo["balance"])
        self.expensesLabel = Label(self.root, text="Expenses: %.2f"%self.userInfo["expenses"])
        self.budgetLabel = Label(self.root, text="Budget: %.2f"%self.userInfo["budget"])
        self.creditLabel = Label(self.root, text="Credits: %.2f"%self.userInfo["credits"])
        self.savingsLabel = Label(self.root, text="Savings: %.2f"%self.userInfo["savings"])
        self.dateLabel = Label(self.root, text="Todays date is: " + str(date.today()), bd=1, relief=SUNKEN, anchor=S)
        self.addIncomeLabel = Label(self.root, text="Add Income:").grid(row = 7, column = 0)
        self.addIncomeEntry = Entry(self.root, textvariable= DoubleVar(), justify= RIGHT)
        self.addExpenseLabel = Label(self.root, text="Add Expense:").grid(row = 8, column = 0)
        self.addExpenseEntry = Entry(self.root, textvariable= DoubleVar(), justify= RIGHT)
        self.addSavingsLabel = Label(self.root, text="Add Savings:").grid(row = 9, column = 0)
        self.addSavingsEntry = Entry(self.root, textvariable= DoubleVar(), justify= RIGHT)
        self.addCreditLabel = Label(self.root, text="Add Credits:").grid(row = 10, column = 0)
        self.addCreditEntry = Entry(self.root, textvariable= DoubleVar(), justify= RIGHT)
        self.subsCreditLabel = Label(self.root, text="Substract Credits:").grid(row = 11, column = 0)
        self.subsCreditEntry = Entry(self.root, textvariable= DoubleVar(), justify= RIGHT)
        self.saveButton = Button(self.root, text="Save!")
        self.plotPieChart()
        self.budgetOptsButton = Button(self.root, text="Options")
        self.savingsOptsButton = Button(self.root, text="Options")
        self.namePending = Label(self.root, text="h").grid(row = 2, column = 4)
        
        ## Positioning of things
        self.welcomeLabel.grid(row = 0, column = 0, columnspan = 2, pady =40, padx =20)
        self.balanceLabel.grid(row = 1, column = 0, columnspan = 2, pady =10)
        self.expensesLabel.grid(row = 2, column = 0, columnspan = 2, pady =10)
        self.budgetLabel.grid(row = 3, column = 0, columnspan = 2, pady =10)
        self.creditLabel.grid(row = 4, column = 0, columnspan = 2, pady =10)
        self.savingsLabel.grid(row = 5, column = 0, columnspan = 2, pady =10)
        self.addIncomeEntry.grid(row = 7, column = 1)
        self.addExpenseEntry.grid(row = 8, column = 1)
        self.addSavingsEntry.grid(row = 9, column = 1)
        self.addCreditEntry.grid(row = 10, column = 1)
        self.subsCreditEntry.grid(row = 11, column = 1)
        self.dateLabel.grid(row=10, column = 3, columnspan=5,sticky=S)
        self.saveButton.grid(row = 12, column = 1, columnspan = 2, sticky=W)
        self.budgetOptsButton.grid(row = 3, column = 3, columnspan = 1, pady =10)
        self.savingsOptsButton.grid(row = 5, column = 3, columnspan = 1, pady =10)


        
        ## Binded functionts
        self.addIncomeEntry.bind('<Return>',self.addBalance)
        self.addExpenseEntry.bind('<Return>',self.addExpense)
        self.addSavingsEntry.bind('<Return>',self.addSavings)
        self.addCreditEntry.bind('<Return>',self.addCredits)
        self.subsCreditEntry.bind('<Return>',self.subsCredits)
        self.saveButton.bind('<Button-1>', self.saveCurrentState)
        self.budgetOptsButton.bind('<Button-1>', self.budgetOptionsWindow)
        self.savingsOptsButton.bind('<Button-1>', self.savingsOptionsWindow)
        self.root.mainloop()

    ##Behaviours

    ##
    #   Used to add income written by the user
    #
    def addBalance(self, event):
        self.userInfo["balance"]+= float(self.addIncomeEntry.get())
        self.balanceLabel.config(text="Balance: %.2f"%self.userInfo["balance"])
        self.addIncomeEntry.delete(0, last=7)
        self.listValues[0] = self.userInfo["balance"]
        self.plotPieChart()
    ##
    #   Used to add an expense and substract from the general balance
    #
    def addExpense(self, event):
        self.userInfo["balance"]-= float(self.addExpenseEntry.get())
        if self.userInfo["balance"]<=0:
            messagebox.showerror("Oops","You spent all your money!")
        self.balanceLabel.config(text="Balance: %.2f"%self.userInfo["balance"])
        self.userInfo["budget"]-= float(self.addExpenseEntry.get())
        self.budgetLabel.config(text="Budget: %.2f"%self.userInfo["budget"])
        if self.userInfo['budget'] <= 0:
            messagebox.showwarning("Oops","You are spending agaisnt your budget")
        self.userInfo["expenses"]+= float(self.addExpenseEntry.get())
        self.expensesLabel.config(text="Expenses: %.2f"%self.userInfo["expenses"])
        self.addExpenseEntry.delete(0, last=7)
        self.listValues[1] = self.userInfo["expenses"]
        self.plotPieChart()
    ##
    #   Used to add savings while substracting from the balance
    #   it is assumed the money comes from general balance
    def addSavings(self, event):
        self.userInfo["balance"]-= float(self.addSavingsEntry.get())
        self.balanceLabel.config(text="Balance: %.2f"%self.userInfo["balance"])
        self.userInfo["savings"]+= float(self.addSavingsEntry.get())
        self.savingsLabel.config(text="Savings: %.2f"%self.userInfo["savings"])
        self.addSavingsEntry.delete(0, last=7)
        self.listValues[4] = self.userInfo["savings"]
        self.plotPieChart()
    ##
    #   Adds credit specified by the user
    #
    def addCredits(self, event):
        self.userInfo["credits"]+= float(self.addCreditEntry.get())
        self.creditLabel.config(text="Credits: %.2f"%self.userInfo["credits"])
        self.addCreditEntry.delete(0, last=7)
        self.plotPieChart()
    ##
    #   Substract payment specifies by user(Payment assumed)
    #
    def subsCredits(self, event):
        temp = self.userInfo["credits"]
        self.userInfo["credits"]-= float(self.subsCreditEntry.get())
        self.creditLabel.config(text="Credits: %.2f"%self.userInfo["credits"])
        self.subsCreditEntry.delete(0, last=7)
        if self.userInfo["credits"]<=0:
            response = messagebox.askyesno("Credits","Did you pay all your credits?")
            if response == 0:
                self.userInfo["credits"]= temp
                self.creditLabel.config(text="Credits: %.2f"%self.userInfo["credits"])
            else:
                self.userInfo["credits"]= 0
                self.creditLabel.config(text="Credits: %.2f"%self.userInfo["credits"])
        self.plotPieChart()
    ##
    #   Plot the pie chart
    #
    def plotPieChart(self):
        self.figure = plt.Figure(figsize=(4,3), dpi=100)
        ax = self.figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(self.figure, self.graphFrame)
        chart_type.get_tk_widget().grid(row = 2, column = 5, sticky=E, rowspan=5)
        ax.pie(self.listValues,labels=self.listKeys, colors=self.colorValues, startangle=270)
    ##
    #   Save the data into the JSON file
    #
    def saveCurrentState(self, event):
        data = {
                "date":str(self.currentDate),
                "balance":self.userInfo['balance'], 
                "expenses":self.userInfo['expenses'], 
                "budget":self.userInfo['budget'], 
                "credits":self.userInfo['credits'], 
                "savings":self.userInfo['savings']
        }
        self.jsonFile['data'].append(data)
        with open("userData.json", "w") as f:
            f.write(json.dumps(self.jsonFile, indent=4))
       
    def budgetOptionsWindow(self, event):
        self.options = Toplevel()
        self.options.lift()
        self.budgetOption = IntVar()
        self.budgetOption.set(2)
        self.options.title('Budget')
        budgetModLabel = Label(self.options, text="Adjust Budget:").pack()
        self.budgetModEntry = Entry(self.options, textvariable= DoubleVar(), justify= RIGHT)
        self.budgetModEntry.pack()
        Radiobutton(self.options, text="Anual", variable=self.budgetOption, value=1, command= lambda: self.budgetOption.set(1)).pack()
        Radiobutton(self.options, text="Monthly", variable=self.budgetOption, value=2, command=lambda: self.budgetOption.set(2)).pack()
        Radiobutton(self.options, text="Daily", variable=self.budgetOption, value=3, command=lambda: self.budgetOption.set(3)).pack()
        self.setBudgetButton = Button(self.options, text="Set")
        self.setBudgetButton.pack()
        self.setBudgetButton.bind('<Button-1>', self.setBudget)

    def setBudget(self,event):
        self.options.attributes('-topmost', True)
        if float(self.budgetModEntry.get()) == 0.0:
            noBudget = messagebox.askyesno("No budget?","Are you sure you want no budget?")
            if noBudget == 1:
                self.userInfo["budget"] = 0
                self.budgetLabel.config(text="Budget: %.2f"%self.userInfo["budget"])
                self.options.destroy()
                self.options.update()
                return            
            return
        response = messagebox.askyesno("Reset?","Do you want to reset your budget?")
        self.userInfo["budget"] = float(self.budgetModEntry.get()) if response == 1 else float(self.calculateBudget())
        self.budgetLabel.config(text="Budget: %.2f"%self.userInfo["budget"])
        self.options.destroy()
        self.options.update()

    def calculateBudget(self):
        return float(self.budgetModEntry.get()) - self.userInfo['expenses']

    def savingsOptionsWindow(self, event):
        options = Toplevel()
        options.lift()
        options.title('Savings')
        

if __name__ == '__main__':
    with open("userData.json") as f:
        data = json.load(f)
    #print(data['CAT'])

    myApp(data)
