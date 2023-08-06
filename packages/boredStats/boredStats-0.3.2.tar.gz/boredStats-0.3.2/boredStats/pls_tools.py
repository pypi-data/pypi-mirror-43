"""Tools for running Partial-Least Squares Analyses

Finished:
Multitable PLS-C
    
TODO:
Projecting observations into subspace
Multtable PLS-R
Support for pandas
Test suite

Note: These should be able to handle basic PLS-C/ PLS-R analyses since it only
requires a list of arrays
"""

from . import utils
from .corr_tools import cross_corr

import numpy as np

class MultitablePLSC(object):
    def __init__(self, n_iters=None, return_perm=False):
        self.n_iters = n_iters
        self.return_perm = return_perm
    
    @staticmethod
    def _build_corr_xy(y, x_list):
        """Build input for multitable PLSC
        Formula is:
            Y = X1 + X2 + ... + Xn
            
            Where Y is a table of outcome variables and
            Xn are N tables of vars to correlate with Y
        
        Parameters:
        -----------
        y : numpy array
        
        x_list : list
            A list of numpy arrays
            
        Notes:
        ------
        The arrays in y and x_list must have the same
        number of rows
        """
        
        num_vars_in_y = y.shape[1]
        num_vars_in_x = [x.shape[1] for x in x_list]
        
        cross_xy = np.ndarray(shape=[num_vars_in_y, sum(num_vars_in_x)])
        
        start_index = 0
        for x_index, x_table in enumerate(x_list):
            cross_corrmat = cross_corr(y, x_table)
            end_index = start_index + num_vars_in_x[x_index]
            cross_xy[:, start_index:end_index] = cross_corrmat
            
        return cross_xy
    
    @staticmethod
    def _procrustes_rotation(orig_svd, resamp_svd):
        """Apply a Procrustes rotation to resampled SVD results
        
        This rotation is to correct for:
            - axis rotation (change in order of components)
            - axis reflection (change in sign of loadings)
            
        See McIntosh & Lobaugh, 2004 'Assessment of significance'
        
        Parameters:
        -----------
        orig_svd : tuple
        Tuple of SVD results corresponding to original data
        
        resamp_svd : tuple
        Tuple of SVD results corresponding to resampled data
        
        Returns:
        --------
        rotated_u : rotated left singular values
        rotated_diag : rotated diagonal matrix values
        rotated_v : rotated right singular values
        """
        
        original_v = orig_svd[2]
        perm_u = resamp_svd[0]
        perm_diag = resamp_svd[1]
        perm_v = resamp_svd[2]

        n, _, p = np.linalg.svd(np.dot(original_v.T, perm_v), full_matrices=False)
        rotation_matrix = n.dot(p.T)
        
        rotated_u = np.dot(np.dot(perm_u, np.diagflat(perm_diag)), rotation_matrix)
        rotated_v = np.dot(rotation_matrix, np.dot(np.diagflat(perm_diag), perm_v))
        
        sum_of_squares_rotated_u = np.sum(rotated_v[:, :]**2, 0)
        rotated_diag = np.sqrt(sum_of_squares_rotated_u)
        
        return rotated_u, rotated_diag, rotated_v
    
    @staticmethod
    def _p_from_perm_mat(obs_vect, perm_array):
        """Calculate p-values columnwise

        Parameters:
        -----------
        obs_vect : numpy array
        Vector of true observations

        perm_array : numpy array
        N x M array of observations obtained through permutation
            N is the number of permutations used
            M is the number of variables

        Returns:
        --------
        p_values : numpy array
        Vector of p-values corresponding to obs_vect
        """
        p_values = np.ndarray(shape=obs_vect.shape)
        for t, true in enumerate(obs_vect):
            perm_data = perm_array[:, t]
            p_values[t] = utils.permutation_p(true, perm_data)
        return p_values
    
    @staticmethod
    def _bootstrap_z(true_observations, permutation_cube, z_test):
        """Calculate "z-scores" from a cube of permutation data
        
        Works in tandem with mult_plsc_boostrap_saliences
        """
        standard_dev = np.std(permutation_cube, axis=-1)
        bootz = np.divide(true_observations, standard_dev)
        
        zfilt = np.where(np.abs(bootz) < z_test)
        
        #create a copy of data safely using numpy only
        filtered_observations = np.ndarray(shape=true_observations.shape)
        filtered_observations[:, :] = true_observations
        for i in range(len(zfilt[0])):
            row = zfilt[0][i]
            col = zfilt[1][i]
            filtered_observations[row, col] = 0
        
        return filtered_observations, bootz
    
    def mult_plsc(self, y_table, x_tables):
        """Calculate multitable PLS-C, fixed effect model
        See Krishnan et al., 2011 for more
        """
        corr_xy = self._build_corr_xy(y_table, x_tables)
        centered_corr_xy = utils.center_matrix(corr_xy)
        
        u, delta, v = np.linalg.svd(centered_corr_xy, full_matrices=False)
        return u, delta, v

    def mult_plsc_eigenperm(self, y_table, x_tables):
        """Run permutation based testing to determine
        best number of latent variables to use
        
        Parameters:
        -----------
        y_table : numpy array
        Array of variables for Y
        
        x_tables : list
        List of numpy arrays corresponding to X
        
        Returns:
        --------
        output : dict
        Dictionary of outputs
            Defaults to original eigenvalues and associated p-values
            return_perm=True includes matrix of permutation eigenvalues
        
        See Krishnan et al., 2011, 'Deciding which latent variables to keep' 
        """
        if not self.n_iters:
            return AttributeError("Number of permutations cannot be None")
        
        orig_svd = self.mult_plsc(y_table, x_tables)
        orig_sing = orig_svd[1]
        
        n = 0
        perm_singular_values = np.ndarray(shape=[self.n_iters, len(orig_sing)])
        while n != self.n_iters:
            #print('Working on iteration %d out of %d' % (int(n+1), self.n_iters))
            perm_y = utils.perm_matrix(y_table)
            perm_x_tables = [utils.perm_matrix(x) for x in x_tables]
            
            perm_svd = self.mult_plsc(perm_y, perm_x_tables)
            rot_perm = self._procrustes_rotation(orig_svd, perm_svd)

            perm_singular_values[n, :] = rot_perm[1]
            n += 1
        
        p_values = self._p_from_perm_mat(orig_sing, perm_singular_values)
        
        output = {'true_eigenvalues' : orig_sing,
                 'p_values' : p_values}
        if self.return_perm:
            output['permutation_eigs'] = perm_singular_values
        
        return output
    
    def mult_plsc_bootstrap_saliences(self, y_table, x_tables, z_tester=2):
        """Run bootstrap testing on saliences
        
        Parameters:
        -----------
        y_taable, x_tables: inputs for multitable PLSC
        
        z_tester: int
            "Z-score" to test bootstrap samples with
            Default is 2 (or approximately 1.96)
        
        Returns:
        --------
        output: dict
            Dictionary of filtered saliences
            If return_perm is True, output will include the "z-scores" and
            permutation cube data for the salience matrices
        
        See Krishnan et al., 2011, 'Deciding which latent variables to keep' 
        """
        if not self.n_iters:
            raise AttributeError("Number of iterations cannot be None")
            
        true_svd = self.mult_plsc(y_table, x_tables)
        true_ysal = true_svd[0] #saliences for y-table
        true_xsal = true_svd[2] #saliences for x-tables
        
        perm_ysal = np.ndarray(shape=[true_ysal.shape[0],
                                      true_ysal.shape[1],
                                      self.n_iters])
        perm_xsal = np.ndarray(shape=[true_xsal.shape[0],
                                      true_xsal.shape[1],
                                      self.n_iters])
    
        n = 0
        while n != self.n_iters:
            resampled_y = utils.resample_matrix(y_table)
            resampled_x_tables = [utils.resample_matrix(x) for x in x_tables]
            
            resampled_svd = self.mult_plsc(resampled_y, resampled_x_tables)
            rotated_svd = self._procrustes_rotation(true_svd, resampled_svd)
            perm_ysal[:, :, n] = rotated_svd[0]
            perm_xsal[:, :, n] = rotated_svd[2]
            n += 1
        
        filt_ysal, yz = self._bootstrap_z(true_ysal, perm_ysal, z_tester)
        filt_xsal, xz = self._bootstrap_z(true_xsal, perm_xsal, z_tester)
        
        output = {'y_saliences' : filt_ysal,
                  'x_saliences' : filt_xsal}
        if self.return_perm:
            output['zscores_y_saliences'] = yz
            output['zscores_x_saliences'] = xz
            output['permcube_y_saliences'] = perm_ysal
            output['permcube_x_saliences'] = perm_xsal
        
        return output
        
if __name__ == "__main__":
    y_table = np.loadtxt('y_table.txt')
    x_tables = [np.loadtxt('x_table_%d.txt' % (x+1)) for x in range(3)]
    
    p = MultitablePLSC(n_iters=1000)
    
    res_permeigs = p.mult_plsc_eigenperm(y_table, x_tables)
    res_boostrap = p.mult_plsc_bootstrap_saliences(y_table, x_tables)