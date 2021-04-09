import pandas as pd
import numpy as np
import torch
import torch.nn as nn

##Create the model
class LinearRegression(nn.Module):
    def __init__(self, in_size, out_size):
       super().__init__()
       self.lin = nn.Linear(in_features = in_size, out_features = out_size)
    def forward(self, X):
        pred = self.lin(X)
        return(pred)

def train(model, loss_fun, optimizer, trainLoader, n_epochs=3):
    for epoch in range(n_epochs):
        running_loss = 0.0
        num_iters = len(trainLoader)
        for i, data in enumerate(trainLoader, 0):

            inputs, labels = data

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = loss_fun(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss+= loss.item()
            if i % 2000 == 1999:
                print(f"Loss at epoch [{epoch}/{n_epochs}], iteration [{i + 1}/{num_iters}]: {running_loss / 2000}")
                running_loss = 0.0
    print(f"Training is donde after {n_epochs} epochs!")

def main():
    #Loading the data
    data = pd.read_csv('//./bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv')

    data['price'] = (data['High'] + data["Low"])/2
    data.drop(['Open','Close','Volume_(BTC)', 'Volume_(Currency)','Weighted_Price','High','Low'], axis=1, inplace=True)

    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
    data = data.set_index('Timestamp')
    data = data.resample('6H').mean()
    data = data.dropna()

    #Splitting data into training and testing data
    testSize = int(0.1 * len(data))
    trainSize = len(data)-testSize 

    trainSet, testSet = torch.utils.data.random_split(data,[trainSize, testSize])

    trainLoader = torch.utils.data.DataLoader(trainSet, batch_size=4, num_workers=0)
    testLoader = torch.utils.data.DataLoader(trainSet, batch_size=4, num_workers=0)

    print(f"Training set consists of {len(trainSet)} test set consists of {len(testSet)}.")

    ## Defining model, loss function and optimizer
    model = LinearRegression(2,1)
    loss_func = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    train(model, loss_func,optimizer, trainLoader, n_epochs=100)


if __name__ == '__main__':
    main()