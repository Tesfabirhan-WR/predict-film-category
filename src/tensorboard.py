from datetime import datetime
from tensorflow import keras

log_dir = f"my_log_dir/{datetime.now():%Y%m%d-%H%M%S}"

callbacks = [
    keras.callbacks.TensorBoard(
        log_dir=log_dir,
        histogram_freq=1,  # weight histograms each epoch (needs validation data, which validation_split provides)
    )
]

history = final_model.fit(
    X_train_d,
    y_train,
    epochs=20,
    batch_size=128,
    validation_split=0.2,
    callbacks=callbacks,
)