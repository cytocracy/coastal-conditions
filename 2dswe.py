import numpy
from matplotlib import pyplot
from numba import jit

pyplot.rcParams['font.family'] = 'serif'
pyplot.rcParams['font.size'] = 16

# Update Eta field
@jit(nopython=True) # use Just-In-Time (JIT) Compilation for C-performance
def update_eta_2D(eta, M, N, dx, dy, dt, nx, ny):
    
    # loop over spatial grid 
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            
            # compute spatial derivatives
            dMdx = (M[j,i+1] - M[j,i-1]) / (2. * dx)
            dNdy = (N[j+1,i] - N[j-1,i]) / (2. * dy)
            
            # update eta field using leap-frog method
            eta[j, i] = eta[j, i] - dt * (dMdx + dNdy)
    
    # apply Neumann boundary conditions for eta at all boundaries
    eta[0,:] = eta[1,:]
    eta[-1,:] = eta[-2,:]
    eta[:,0] = eta[:,1]
    eta[:,-1] = eta[:,-2]
    
    return eta          

# Update M field
@jit(nopython=True) # use Just-In-Time (JIT) Compilation for C-performance
def update_M_2D(eta, M, N, D, g, h, alpha, dx, dy, dt, nx, ny):
    
    # compute argument 1: M**2/D + 0.5 * g * eta**2
    arg1 = M**2 / D
    
    # compute argument 2: M * N / D
    arg2 = M * N / D
    
    # friction term
    fric = g * alpha**2 * M * numpy.sqrt(M**2 + N**2) / D**(7./3.)
    
    # loop over spatial grid 
    for i in range(1,nx-1):
        for j in range(1,ny-1):            
            
            # compute spatial derivatives
            darg1dx = (arg1[j,i+1] - arg1[j,i-1]) / (2. * dx)
            darg2dy = (arg2[j+1,i] - arg2[j-1,i]) / (2. * dy)
            detadx = (eta[j,i+1] - eta[j,i-1]) / (2. * dx)
            
            # update M field using leap-frog method
            M[j, i] = M[j, i] - dt * (darg1dx + darg2dy + g * D[j,i] * detadx + fric[j,i])
            
    return M           

# Update N field
@jit(nopython=True) # use Just-In-Time (JIT) Compilation for C-performance
def update_N_2D(eta, M, N, D, g, h, alpha, dx, dy, dt, nx, ny):
    
    # compute argument 1: M * N / D
    arg1 = M * N / D
    
    # compute argument 2: N**2/D + 0.5 * g * eta**2    
    arg2 = N**2 / D
    
    # friction term
    fric = g * alpha**2 * N * numpy.sqrt(M**2 + N**2) / D**(7./3.)
    
    # loop over spatial grid 
    for i in range(1,nx-1):
        for j in range(1,ny-1):            
            
            # compute spatial derivatives
            darg1dx = (arg1[j,i+1] - arg1[j,i-1]) / (2. * dx)
            darg2dy = (arg2[j+1,i] - arg2[j-1,i]) / (2. * dy)
            detady = (eta[j+1,i] - eta[j-1,i]) / (2. * dy)
            
            # update N field using leap-frog method
            N[j, i] = N[j, i] - dt * (darg1dx + darg2dy + g * D[j,i] * detady + fric[j,i])
                        
    return N          

# 2D Shallow Water Equation code with JIT optimization
# -------------------------------------------------------
def Shallow_water_2D(eta0, M0, N0, h, g, alpha, nt, dx, dy, dt, X, Y):
    
    """
    Computes and returns the discharge fluxes M, N and wave height eta from 
    the 2D Shallow water equation using the FTCS finite difference method.
    
    Parameters
    ----------
    eta0 : numpy.ndarray
        The initial wave height field as a 2D array of floats.
    M0 : numpy.ndarray
        The initial discharge flux field in x-direction as a 2D array of floats.    
    N0 : numpy.ndarray
        The initial discharge flux field in y-direction as a 2D array of floats.    
    h : numpy.ndarray
        Bathymetry model as a 2D array of floats.
    g : float
        gravity acceleration.
    alpha : float
        Manning's roughness coefficient.
    nt : integer
        Number fo timesteps.
    dx : float
        Spatial gridpoint distance in x-direction.
    dy : float
        Spatial gridpoint distance in y-direction.        
    dt : float
        Time step. 
    X : numpy.ndarray
        x-coordinates as a 2D array of floats.
    Y : numpy.ndarray
        y-coordinates as a 2D array of floats.
    
    Returns
    -------
    eta : numpy.ndarray
        The final wave height field as a 2D array of floats.
    M : numpy.ndarray
        The final discharge flux field in x-direction as a 2D array of floats.    
    N : numpy.ndarray
        The final discharge flux field in y-direction as a 2D array of floats.  
    """    
    
    # Copy fields
    eta = eta0.copy()
    M = M0.copy()
    N = N0.copy()
    
    # Compute total thickness of water column D
    D = eta + h
    
    # Estimate number of grid points in x- and y-direction
    ny, nx = eta.shape
    
    # Define the locations along a gridline.
    x = numpy.linspace(0, nx*dx, num=nx)
    y = numpy.linspace(0, ny*dy, num=ny)
    
    # Plot the initial wave height fields eta and bathymetry model
    fig = pyplot.figure(figsize=(10., 6.))
    cmap = 'seismic'
    
    pyplot.tight_layout()
    extent = [numpy.min(x), numpy.max(x),numpy.min(y), numpy.max(y)]
    
    # Plot bathymetry model
    topo = pyplot.imshow(numpy.flipud(-h), cmap=pyplot.cm.gray, interpolation='nearest', extent=extent) 
    
    # Plot wave height field at current time step
    im = pyplot.imshow(numpy.flipud(eta), extent=extent, interpolation='spline36', cmap=cmap, alpha=.75, vmin = -0.4, vmax=0.4)

    pyplot.xlabel('x [m]')
    pyplot.ylabel('y [m]')
    cbar = pyplot.colorbar(im)
    cbar1 = pyplot.colorbar(topo)
    pyplot.gca().invert_yaxis()
    cbar.set_label(r'$\eta$ [m]')
    cbar1.set_label(r'$-h$ [m]')
    
    # activate interactive plot
    pyplot.ion()    
    pyplot.show(block=False)  
    
    # write wave height field and bathymetry snapshots every nsnap time steps to image file
    nsnap = 50
    snap_count = 0
    
    # Loop over timesteps
    for n in range(nt):
        
        # 1. Update Eta field
        # -------------------
        eta = update_eta_2D(eta, M, N, dx, dy, dt, nx, ny)
        
        # 2. Update M field
        # -----------------
        M = update_M_2D(eta, M, N, D, g, h, alpha, dx, dy, dt, nx, ny)
        
        # 3. Update N field
        # -----------------
        N = update_N_2D(eta, M, N, D, g, h, alpha, dx, dy, dt, nx, ny)
        
        # 4. Compute total water column D
        # -------------------------------
        D = eta + h
        
        # update wave height field eta
        if (n % nsnap) == 0:        
            im.set_data(eta)
            fig.canvas.draw()
            
            # write snapshots to Tiff files
            name_snap = "image_out/Shallow_water_2D_" + "%0.*f" %(0,numpy.fix(snap_count+1000)) + ".tiff"
            pyplot.savefig(name_snap, format='tiff', bbox_inches='tight', dpi=125)
            snap_count += 1
                    
    return eta, M, N

Lx = 100.0   # width of the mantle in the x direction []
Ly = 100.0   # thickness of the mantle in the y direction []
nx = 401     # number of points in the x direction
ny = 401     # number of points in the y direction
dx = Lx / (nx - 1)  # grid spacing in the x direction []
dy = Ly / (ny - 1)  # grid spacing in the y direction []

# Define the locations along a gridline.
x = numpy.linspace(0.0, Lx, num=nx)
y = numpy.linspace(0.0, Ly, num=ny)

# Define initial eta, M, N
X, Y = numpy.meshgrid(x,y) # coordinates X,Y required to define eta, h, M, N

# Define constant ocean depth profile h = 50 m
h = 50 * numpy.ones_like(X)

# Define initial eta Gaussian distribution [m]
eta0 = 0.5 * numpy.exp(-((X-50)**2/10)-((Y-50)**2/10))

# Define initial M and N
M0 = 100. * eta0
N0 = 0. * M0

# define some constants
g = 9.81  # gravity acceleration [m/s^2]
alpha = 0.025 # friction coefficient for natural channels in good condition

# Maximum wave propagation time [s]
Tmax = 6.
dt = 1/4500.
nt = (int)(Tmax/dt)

# Compute eta, M, N fields
eta, M, N = Shallow_water_2D(eta0, M0, N0, h, g, alpha, nt, dx, dy, dt, X, Y)