# Usage

### @track

```python
from blackboxml import track, MetricStore

@track(name="resnet_cifar10", tags=["pytorch", "cifar10"])
def train():
    metrics = MetricStore()
    for epoch in range(10):
        metrics.reset()
        for batch in dataloader:
            loss, acc = train_step(batch)
            metrics.update({"loss": loss, "acc": acc}, n=len(batch))
        yield metrics.compute()

train()
```

### Run context manager

```python
from blackboxml import Run

with Run(name="resnet_cifar10", tags=["pytorch"]) as run:
    for epoch in range(10):
        run.log({"loss": train_one_epoch(), "epoch": epoch})
```

### Keras callback

```python
from blackboxml.callback import BlackBoxCallback

model.fit(x_train, y_train, epochs=10,
          callbacks=[BlackBoxCallback(name="lstm_nlp", tags=["keras"])])
```
