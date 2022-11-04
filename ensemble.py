"""
File for training the hybrid recommender neural network
"""

# standard library imports
from math import sqrt

# 3rd party imports
import torch
import pandas as pd
import numpy as np
import seaborn as sns

# local imports (i.e. our own code)


class Recommender(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(3, 1)

    def forward(self, x):
        return self.linear(x.float())


class RecommenderDataset(torch.utils.data.Dataset):
    def __init__(self, item, user, content, original):
        item = pd.read_csv(item, index_col=0).reset_index(drop=True)
        self.item_mean = np.nanmean(item.replace(0, np.nan).to_numpy(dtype=np.single))
        item = item.replace(0, self.item_mean)

        user = pd.read_csv(user, index_col=0).reset_index(drop=True)
        self.user_mean = np.nanmean(user.replace(0, np.nan).to_numpy(dtype=np.single))
        user = user.replace(0, self.user_mean)

        content = pd.read_csv(content)

        original = pd.read_csv(original, index_col=0).reset_index(drop=True)

        self.X, self.y = self._getTrainData(user, item, content, original)

    def _getTrainData(self, user_cf, item_cf, content, original_user_rating):
        Xtrain = []
        ytrain = []
        for rowIndex, row in original_user_rating.iterrows():  # iterate over rows
            for columnIndex, value in row.items():
                if value != 0:
                    try:
                        user_value = user_cf.loc[[rowIndex]][columnIndex].values[
                            0
                        ]  # item based cf
                    except KeyError:
                        user_value = self.user_mean
                    try:
                        item_value = item_cf.loc[[rowIndex]][columnIndex].values[
                            0
                        ]  # user based cf
                    except KeyError:
                        item_value = self.item_mean
                    try:
                        content_value = content.loc[[rowIndex]][columnIndex].values[
                            0
                        ]  # value of content_based
                    except KeyError:
                        content_value = 0
                    y_value = original_user_rating.loc[[rowIndex]][columnIndex].values[
                        0
                    ]
                    Xtrain.append((user_value, item_value, content_value))
                    ytrain.append(y_value)

        return (
            torch.tensor(Xtrain, dtype=torch.float),
            torch.tensor(ytrain, dtype=torch.float)[:, None],
        )

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def train_one_epoch():
    running_loss = 0.0

    for data in dataloader:
        inputs, labels = data

        optimizer.zero_grad()

        outputs = model(inputs)

        loss = loss_fn(outputs, labels)
        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    return running_loss


if __name__ == "__main__":
    data = RecommenderDataset(
        r"data\out\user-predictions-noclip.csv",
        r"data\out\item-predictions-noclip.csv",
        r"data\out\content_based.csv",
        r"data\out\user-item-matrix.csv",
    )
    dataloader = torch.utils.data.DataLoader(data, batch_size=32, shuffle=True)
    model = Recommender()
    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters())

    EPOCHS = 1000

    losses = []

    for epoch in range(EPOCHS):
        model.train(True)
        avg_loss = train_one_epoch()

        model.train(False)
        if epoch % 10 == 0:
            print(f"Epoch {epoch + 1} Loss: {avg_loss:.2f}")

        losses.append(avg_loss)

    torch.save(model.state_dict(), "models/model_v2.pt")

    # losses = pd.DataFrame({"Epochs": range(EPOCHS), "RMSE": [sqrt(x) for x in losses]})

    # sns.lineplot(data=losses, x="Epochs", y="RMSE")
