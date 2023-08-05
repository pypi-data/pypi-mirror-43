# used to have a common interface
import numpy as np

from scipy.interpolate import griddata, Rbf
from sklearn.svm import SVR

from .idw import Idw


def __points(x, y):
    return np.asarray((x, y), dtype=float).T


def __scipy_griddata(x, y, z, grid, method):
    points = __points(x, y)
    values = np.asarray(z)
    return griddata(points, values, grid, method=method)


def nearest(x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'nearest')


def linear(x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'linear')


def cubic(x, y, z, grid, **settings):
    return __scipy_griddata(x, y, z, grid, 'cubic')


def rbf(x, y, z, grid, **settings):
    # get the settings
    func = settings.get('func', 'thin_plate')
    #epsilon = settings.get('epsilon')
    smooth = settings.get('smooth', 0.0)
    norm = settings.get('norm', 'euclidean') # maybe this works with scipy 1.2

    # create the object
    f = Rbf(x, y, z, function=func, smooth=smooth)
    shape = grid[0].shape

    # apply
    return f(grid[0].flatten(), grid[1].flatten()).reshape(shape)


def idw(x, y, z, grid, **settings):
    # get settings
    radius = settings.get('radius', 5000)
    minp = settings.get('min_points', 4)
    maxp = settings.get('max_points', 20)
    na = settings.get('fill_na')

    # create the object
    f = Idw(x, y, z, radius, min_points=minp, max_points=maxp, fill_na=na)
    shape = grid[0].shape

    # apply
    return f(grid[0].flatten(), grid[1].flatten()).reshape(shape)


def svm(x, y, z, grid, **settings):
    # get settings
    gamma = 'scale'
    kernel = settings.get('kernel', 'rbf')
    tol = settings.get('tol', 1e-3)

    # transform x,y and grid
    X = np.concatenate((x, y)).reshape(2, len(x)).T.copy()
    target = np.asarray(z)
    xx, yy = grid
    Xi = np.concatenate((xx.flatten(), yy.flatten()))
    Xi = Xi.reshape(2, len(xx.flatten())).T.copy()

    # create SVC instance and fit
    svr = SVR(gamma=gamma, kernel=kernel, tol=tol).fit(X, target)

    # apply
    return svr.predict(Xi).reshape(xx.shape)
