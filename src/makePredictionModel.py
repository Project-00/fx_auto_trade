# -*- coding: utf-8 -*-
# ライブラリのインポート
import numpy as np
import tensorflow as tf
import os.path
from predictionDataMaker import predictionDataMaker

# parameterの中身 OPEN:始値 CLOSE:終値 HIGH:高値 LOW:安値
def makePredictionModel(parameter):

    pdm = predictionDataMaker(parameter)

    X_train = pdm[0]
    X_test = pdm[1]
    Y_train = pdm[2]
    Y_test = pdm[3]
    scaler = pdm[4]
    n_stocks = pdm[5]   # 要素数

    # -- tensorflowのニューラルネットワーク構築 --



    # ニューロンの数を設定（２層のニューラルネットワーク）（シンプル過ぎるから要修正点）
    n_neurons_1 = 256
    n_neurons_2 = 128

    # セッションの開始
    net = tf.InteractiveSession()

    # プレースホルダーの作成
    X = tf.placeholder(dtype=tf.float32, shape=[None, n_stocks], name="X")
    Y = tf.placeholder(dtype=tf.float32, shape=[None], name="Y")

    # 初期化
    sigma = 1
    weight_initializer = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=sigma)
    bias_initializer = tf.zeros_initializer()


    # バイアスと隠れ層の重み
    W_hidden_1 = tf.Variable(weight_initializer([n_stocks, n_neurons_1]), name="h1weight")
    bias_hidden_1 = tf.Variable(bias_initializer([n_neurons_1]), name="h1bias")
    W_hidden_2 = tf.Variable(weight_initializer([n_neurons_1, n_neurons_2]), name="h2weight")
    bias_hidden_2 = tf.Variable(bias_initializer([n_neurons_2]), name="h2bias")

    # 出力の重み
    W_out = tf.Variable(weight_initializer([n_neurons_2, 1]), name="weight")
    bias_out = tf.Variable(bias_initializer([1]), name="bias")

    # 隠れ層の設定（ReLU＝活性化関数）
    hidden_1 = tf.nn.leaky_relu(tf.add(tf.matmul(X, W_hidden_1),bias_hidden_1))

    hidden_2 = tf.nn.leaky_relu(tf.add(tf.matmul(hidden_1, W_hidden_2), bias_hidden_2))

    # 出力層の設定
    out = tf.transpose(tf.add(tf.matmul(hidden_2, W_out), bias_out))

    # 損失関数(誤差の計算)交差エントロピー
    mse = tf.reduce_mean(tf.squared_difference(out,Y))

    # 最適化関数
    opt = tf.train.AdamOptimizer(name="opt").minimize(mse)

    # 初期化
    net.run(tf.global_variables_initializer())


    # ニューラルネットワークの設定
    batch_size = 80         # 同時に処理する数
    mse_train = []          # 空箱にしておく(随時addしていくため）
    mse_test = []           # 上に同じ

    # 反復処理数
    epochs = 3000
    for e in range(epochs):
        net.run(opt, feed_dict={X: X_train, Y: Y_train})


    # -- テストデータで予測 --
    pred_test = net.run(out, feed_dict={X: X_test})

    # 予測値をテストデータに戻す（値も正規化から戻す）
    pred_test = np.concatenate((pred_test.T, X_test), axis=1)
    pred_inv = scaler.inverse_transform(pred_test)

    # 予想結果の値はpred_inv
    print(pred_inv)
    # 読み方は左から close open high low vol


    #訓練済みモデルの保存
    cwd = os.getcwd()
    saver = tf.train.Saver()
    saver.save(net, cwd + "\\" + parameter + "_PredictionModel.ckpt")
    print('Saved a model.')

    net.close()

    return(pred_inv)

# if __name__ == "__main__":
#     a = makePredictionModel("OPEN")