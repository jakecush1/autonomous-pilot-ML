# steps 2 + 3: LSTM and transformer on the same windows as linear_reg.py
# both read the last H minutes one minute at a time ([dx, dy, wind_e, wind_n] per minute)
# and output the metres drifted east/north over the next H minutes
#
# usage:  python src/main.py lstm            (or: python src/models/nn_models.py lstm)
#         python src/main.py transformer
import math
import os
import sys
import numpy as np
import torch
from torch import nn

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # src/, so this file also runs on its own
from cmn import data_prep as dp
from models.linear_reg import save_results

SEED = 0
EPOCHS = 80
PATIENCE = 10           # stop when val loss hasn't improved for this many epochs
BATCH = 256
LR = 1e-3


class LSTMModel(nn.Module):
    def __init__(self, n_in, hidden=64, layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(n_in, hidden, layers, batch_first=True, dropout=dropout)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(out[:, -1])            # hidden state after the last minute -> (east, north)


class TransformerModel(nn.Module):
    def __init__(self, n_in, d_model=64, heads=4, layers=2, dropout=0.1, seq_len=dp.H):
        super().__init__()
        self.embed = nn.Linear(n_in, d_model)
        # fixed sin/cos positional encoding, so the model knows which minute each row is
        pos = torch.arange(seq_len).unsqueeze(1)
        freq = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(seq_len, d_model)
        pe[:, 0::2], pe[:, 1::2] = torch.sin(pos * freq), torch.cos(pos * freq)
        self.register_buffer("pe", pe)
        layer = nn.TransformerEncoderLayer(d_model, heads, 4 * d_model, dropout, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, layers)
        self.head = nn.Linear(d_model, 2)

    def forward(self, x):
        h = self.encoder(self.embed(x) + self.pe)
        return self.head(h.mean(dim=1))         # average over all minutes -> (east, north)


MODELS = {"lstm": LSTMModel, "transformer": TransformerModel}


def train(name):
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    data = dp.load()
    Xtr, ytr, _ = data["train"]

    # scale inputs and targets with TRAIN stats only (neural nets train badly on raw metres)
    x_mu, x_sd = Xtr.reshape(-1, Xtr.shape[2]).mean(0), Xtr.reshape(-1, Xtr.shape[2]).std(0)
    y_mu, y_sd = ytr.mean(0), ytr.std(0)
    tx = lambda X: torch.tensor((X - x_mu) / x_sd, dtype=torch.float32)
    ty = lambda y: torch.tensor((y - y_mu) / y_sd, dtype=torch.float32)

    model = MODELS[name](Xtr.shape[2])
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.MSELoss()
    Xt, yt = tx(Xtr), ty(ytr)
    Xv, yv = tx(data["val"][0]), ty(data["val"][1])

    best, best_state, bad = float("inf"), None, 0
    for epoch in range(EPOCHS):
        model.train()
        perm = torch.randperm(len(Xt))           # shuffling batches is fine; the split is still by time
        for i in range(0, len(Xt), BATCH):
            idx = perm[i:i + BATCH]
            opt.zero_grad()
            loss = loss_fn(model(Xt[idx]), yt[idx])
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()

        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(Xv), yv).item()
        print(f"epoch {epoch:3d}  train {loss.item():.3f}  val {val_loss:.3f}")
        if val_loss < best:
            best, bad = val_loss, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            bad += 1
            if bad >= PATIENCE:
                break

    model.load_state_dict(best_state)
    model.eval()
    res = {}
    with torch.no_grad():
        for s in ["val", "test"]:
            pred = model(tx(data[s][0])).numpy() * y_sd + y_mu
            res[s] = dp.score(data[s][1], pred)
    save_results(name, res)
    os.makedirs(dp.OUTPUT_DIR, exist_ok=True)
    torch.save(best_state, os.path.join(dp.OUTPUT_DIR, f"{name}.pt"))
    print(f"{name}: val median {res['val']['median_m']:.0f} m  p90 {res['val']['p90_m']:.0f} m"
          f"  | test median {res['test']['median_m']:.0f} m  p90 {res['test']['p90_m']:.0f} m")


if __name__ == "__main__":
    train(sys.argv[1] if len(sys.argv) > 1 else "lstm")
