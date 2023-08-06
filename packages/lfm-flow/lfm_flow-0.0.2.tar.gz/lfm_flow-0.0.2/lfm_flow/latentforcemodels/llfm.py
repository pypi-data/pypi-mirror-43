import tensorflow as tf
from tensorflow_probability.python.distributions import MultivariateNormalFullCovariance

class LLFM:

    def __init__(self, kernel, jitter=1e-5):
        self.jitter = jitter
        self.kernel = kernel

    def _build_likelihood(self):
        """
        Tensorflow function to compute the multivate normal log likelihood
        """
        Kyy = self.kernel(self.t_input, self.t_input_shape)
        Kyy += tf.diag(1e-4 * tf.ones(Kyy.shape[0], dtype=Kyy.dtype))
        mvn = MultivariateNormalFullCovariance(covariance_matrix=Kyy)

        logpdf = mvn._log_prob(
            tf.transpose(self.Y, (1, 0)))
        return tf.reduce_sum(logpdf)

    def predict_lf(self, tnew, return_cov=False):
        """
        Predicts the value of the latent forces at times tnew
        """

        Kyy = self.kernel(self.t_input, self.t_input_shape)
        Kyy += tf.diag(self.jitter * tf.ones(Kyy.shape[0], dtype=Kyy.dtype))

        # Cholesky decomposition
        Lyy = tf.linalg.cholesky(Kyy)

        Kyf = self.kernel.lf_cross_cov(self.t_input,
                                       self.t_input_shape,
                                       tnew)
        mf = tf.matmul(
            tf.transpose(Kyf, (1, 0)),
            tf.linalg.cholesky_solve(Lyy, self.Y))

        if return_cov:

            Dtsq = tnew[:, None] - tnew[None, :]
            Dtsq = Dtsq[None, ...] / self.kernel.lf_length_scales[:, None, None]
            Dtsq = Dtsq ** 2

            Kff_diag = tf.exp( -Dtsq )

            Kff = Kff_diag[0, ...]

            covf = Kff - tf.matmul(tf.transpose(Kyf, (1, 0)),
                                   tf.linalg.cholesky_solve(Lyy, Kyf))

            return mf, covf

        else:
            return mf
