from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    dims = W.shape[0]
    classes = W.shape[1]
    training = X.shape[0]

    for i in xrange(training):
        scores = X[i, :].dot(W)
        scores_exp = np.exp(scores)

        scores_prob = scores_exp/np.sum(scores_exp)

        for j in xrange(dims):
            for q in xrange(classes):
                if q == y[i]:
                    dW[j, q] += X.T[j, i] * (scores_prob[q]-1)
                else:
                    dW[j, q] += X.T[j, i] * scores_prob[q]
    
        loss += -np.log(scores_prob[y[i]])

    loss /= training
    loss += 0.5 * reg * np.sum(W**2)
  
    dW /= training
    dW += reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    classes = W.shape[1]
    training = X.shape[0] #N
    scores = X.dot(W) #N,C #f
    scores -= scores.max()
    scores_exp = np.exp(scores) #expf
    scores_prob = scores_exp / scores_exp.sum(axis=1, keepdims=True)
    loss = -np.log(scores_prob[range(training), y]).sum() / training
    loss += 0.5 * reg * np.sum(W * W)

    df = scores_prob
    df[range(training), y] -= 1.0

    dW_prep = reg * W
    dW = X.T.dot(df) / training + dW_prep

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
