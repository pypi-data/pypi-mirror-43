import functools
import warnings
import numpy as np
from .base import Decomposition, svd
from ...core.structures import Tensor, TensorCPD, residual_tensor
from ...core.operations import khatri_rao, hadamard


# TODO: Need to add option of sorting vectors in the factor matrices and making them sign invariant
class BaseCPD(Decomposition):

    def __init__(self, init, max_iter, epsilon, tol, random_state, verbose):
        super(BaseCPD, self).__init__()
        self.init = init
        self.max_iter = max_iter
        self.epsilon = epsilon
        self.tol = tol
        self.random_state = random_state
        self.verbose = verbose

    def copy(self):
        """ Copy of the Decomposition as a new object """
        new_object = super(BaseCPD, self).copy()
        return new_object

    @property
    def name(self):
        """ Name of the decomposition

        Returns
        -------
        decomposition_name : str
        """
        decomposition_name = super(BaseCPD, self).name
        return decomposition_name

    def decompose(self, tensor, rank, keep_meta):
        raise NotImplementedError('Not implemented in base (BaseCPD) class')

    @property
    def converged(self):
        """ Checks convergence

        Returns
        -------
        is_converged : bool
        """
        try:  # This insures that the cost has been computed at least twice without checking number of iterations
            is_converged = abs(self.cost[-2] - self.cost[-1]) <= self.tol
        except IndexError:
            is_converged = False
        return is_converged

    def _init_fmat(self, tensor, rank):
        """ Initialisation of factor matrices

        Parameters
        ----------
        tensor : Tensor
            Multidimensional data to be decomposed
        rank : tuple
            Should be of shape (R,1), where R is the desired tensor rank. It should be passed as tuple for consistency.

        Returns
        -------
        fmat : list[np.ndarray]
            List of factor matrices
        """
        self.cost = []  # Reset cost every time when method decompose is called
        t_rank = rank[0]
        fmat = [np.array([])] * tensor.order
        # Check if all dimensions are greater then kryskal rank
        dim_check = (np.array(tensor.shape) >= t_rank).sum() == tensor.order
        if dim_check:
            if self.init is 'svd':
                for mode in range(tensor.order):
                    # TODO: don't really like this implementation
                    fmat[mode], _, _ = svd(tensor.unfold(mode, inplace=False).data, t_rank)
            elif self.init is 'random':
                fmat = [np.random.randn(mode_size, t_rank) for mode_size in tensor.shape]
            else:
                raise NotImplementedError('The given initialization is not available')
        else:
            fmat = [np.random.randn(mode_size, t_rank) for mode_size in tensor.shape]
            if self.verbose and self.init != 'random':
                warnings.warn(
                    "Specified rank value is greater then one of the dimensions of a tensor ({} > {}).\n"
                    "Factor matrices have been initialized randomly.".format(t_rank, tensor.shape), RuntimeWarning
                )
        return fmat

    def plot(self):
        raise NotImplementedError('Not implemented in base (BaseCPD) class')


class CPD(BaseCPD):
    """ Canonical Polyadic Decomposition.

    Computed via alternating least squares (ALS)

    Parameters
    ----------
    init : str
        Type of factor matrix initialisation. Available options are `svd` and `random`
    max_iter : int
        Maximum number of iteration
    epsilon : float
        Threshold for the relative error of approximation.
    tol : float
        Threshold for convergence of factor matrices
    random_state : int
    verbose : bool
        If True, enable verbose output

    Attributes
    ----------
    cost : list
        A list of relative approximation errors at each iteration of the algorithm.
    """

    def __init__(self, init='svd', max_iter=50, epsilon=10e-3, tol=10e-5,
                 random_state=None, verbose=False) -> None:
        super(CPD, self).__init__(init=init,
                                  max_iter=max_iter,
                                  epsilon=epsilon,
                                  tol=tol,
                                  random_state=random_state,
                                  verbose=verbose)
        self.cost = []

    def copy(self):
        """ Copy of the CPD algorithm as a new object """
        new_object = super(CPD, self).copy()
        new_object.cost = []
        return new_object

    @property
    def name(self):
        """ Name of the decomposition

        Returns
        -------
        decomposition_name : str
        """
        decomposition_name = super(CPD, self).name
        return decomposition_name

    def decompose(self, tensor, rank, keep_meta=0, kr_reverse=False):
        """ Performs CPD-ALS on the `tensor` with respect to the specified `rank`

        Parameters
        ----------
        tensor : Tensor
            Multidimensional data to be decomposed
        rank : tuple
            Desired Kryskal rank for the given `tensor`. Should contain only one value.
            If it is greater then any of dimensions then random initialisation is used
        keep_meta : int
            Keep meta information about modes of the given `tensor`.
            0 - the output will have default values for the meta data
            1 - keep only mode names
            2 - keep mode names and indices
        kr_reverse : bool

        Returns
        -------
        tensor_cpd : TensorCPD
            CP representation of the `tensor`

        Notes
        -----
        khatri-rao product should be of matrices in reversed order. But this will duplicate original data (e.g. images)
        Probably this has something to do with data ordering in Python and how it relates to kr product
        """
        if not isinstance(tensor, Tensor):
            raise TypeError("Parameter `tensor` should be an object of `Tensor` class!")
        if not isinstance(rank, tuple):
            raise TypeError("Parameter `rank` should be passed as a tuple!")
        if len(rank) != 1:
            raise ValueError("Parameter `rank` should be tuple with only one value!")

        tensor_cpd = None
        fmat = self._init_fmat(tensor, rank)
        core_values = np.repeat(np.array([1]), rank)
        norm = tensor.frob_norm
        for n_iter in range(self.max_iter):

            # Update factor matrices
            for mode in range(tensor.order):
                kr_result = khatri_rao(fmat, skip_matrix=mode, reverse=kr_reverse)
                hadamard_result = hadamard([np.dot(mat.T, mat) for i, mat in enumerate(fmat) if i != mode])
                # Do consecutive multiplication of np.ndarray
                update = functools.reduce(np.dot, [tensor.unfold(mode, inplace=False).data,
                                                   kr_result,
                                                   np.linalg.pinv(hadamard_result)])
                fmat[mode] = update

            # Update cost
            tensor_cpd = TensorCPD(fmat=fmat, core_values=core_values)
            residual = residual_tensor(tensor, tensor_cpd)
            self.cost.append(abs(residual.frob_norm / norm))
            if self.verbose:
                print('Iter {}: relative error of approximation = {}'.format(n_iter, self.cost[-1]))

            # Check termination conditions
            if self.cost[-1] <= self.epsilon:
                if self.verbose:
                    print('Relative error of approximation has reached the acceptable level: {}'.format(self.cost[-1]))
                break
            if self.converged:
                if self.verbose:
                    print('Converged in {} iteration(s)'.format(len(self.cost)))
                break
        if self.verbose and not self.converged and self.cost[-1] > self.epsilon:
            print('Maximum number of iterations ({}) has been reached. '
                  'Variation = {}'.format(self.max_iter, abs(self.cost[-2] - self.cost[-1])))

        if keep_meta == 1:
            mode_names = {i: mode.name for i, mode in enumerate(tensor.modes)}
            tensor_cpd.set_mode_names(mode_names=mode_names)
        elif keep_meta == 2:
            tensor_cpd.copy_modes(tensor)
        else:
            pass
        return tensor_cpd

    @property
    def converged(self):
        """ Checks convergence of the CPD-ALS algorithm.

        Returns
        -------
        bool
        """
        is_converged = super(CPD, self).converged
        return is_converged

    def _init_fmat(self, tensor, rank):
        fmat = super(CPD, self)._init_fmat(tensor=tensor,
                                           rank=rank)
        return fmat

    def plot(self):
        print('At the moment, `plot()` is not implemented for the {}'.format(self.name))
