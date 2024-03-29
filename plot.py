from matplotlib import pyplot as plt
import numpy as np
import params

def individualMagnetization(mx, my, mz):
	plt.plot(mx, label = 'mx')
	plt.plot(my, label = 'my')
	plt.plot(mz, label = 'mz')
	plt.title('Magnetization')
	plt.show()

def spins2DT(magdata, step):
    fig, ax = plt.subplots(figsize=(6,6))
    interpolation='nearest'
    Nx = params.Nx
    Ny = params.Ny

    mx=magdata[0:Nx,0:Ny,0]
    my=magdata[0:Nx,0:Ny,1]
    mz=magdata[0:Nx,0:Ny,2]

    im=ax.imshow(mz,interpolation=interpolation, cmap = 'bwr', origin='lower',vmin=-1,vmax=1,zorder=1)
    width=0.0025
    scale=2.0

    Q = ax.quiver(mx,my,pivot='mid',zorder=2,width=width, scale=scale, angles='xy', scale_units='xy')

    fig.colorbar(im, label=r'$m_z$',orientation='vertical')
    fig.savefig("output/step_" + str(step) + ".png", bbox_inches='tight')
        

#@todo: check and remove old functions
def make(size):
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot()
    return fig, ax

def getHeat(ax, arq, i, j):
    axes = {"z": 2, "y": 1, "x": 0}
    if type(ax) == str:
        ax = axes[ax.lower()]
    return (arq.T)[i][j + ax]

def getVectors(ax1, ax2, arq):
    axes = {"z": 2, "y": 1, "x": 0}
    if type(ax1) == str:
        ax1 = axes[ax1.lower()]
    if type(ax2) == str:
        ax2 = axes[ax2.lower()]

    pairs = [[i, j] for i in range(int(len(arq.T) / 3)) for j in range(len(arq))]

    x, y = zip(*pairs)

    pairs = [[(arq.T)[i][j + ax1], (arq.T)[i][j + ax2]]for j in range(0, len(arq.T), 3) for i in range(len(arq))]

    u, v = zip(*pairs)

    return x, y, u, v

def getIm(ax, arq):
    return [[getHeat(ax, arq, i, j) for j in range(0, len(arq.T), 3)] for i in range(len(arq))]

def selectImAx(ax):
    axes = {"z": 2, "y": 1, "x": 0}
    axes_ = {2: "z", 1: "y", 0: "x"}
    if type(ax) == str:
        ax = axes[ax.lower()]
    if ax == 2:
        return axes_[0], axes_[1], axes_[2]
    elif ax == 1:
        return axes_[0], axes_[2], axes_[1]
    elif ax == 0:
        return axes_[1], axes_[2], axes_[0]

def file(arq):
    fig, ax = make([10, 10])

    ax1, ax2, ax3 = selectImAx("z")

    vecs = getVectors(ax1, ax2, arq)
    ax.quiver(*vecs, linewidth=5, angles='xy', scale_units='xy', scale=2.0, pivot="mid")
    ax.set_xlabel(fr"${ax1}$", size=20)
    ax.set_ylabel(fr"${ax2}$", size=20)
    im = ax.imshow(getIm(ax3, arq), cmap='bwr', vmin=-1, vmax=1)
    bar = plt.colorbar(im)
    bar.set_label(fr"$m_{ax3}$", size=20)
    ybot, ytop = ax.get_ylim()
    xleft, xright = ax.get_xlim()

    ax.set_ylim([min([ybot, ytop]), max([ybot, ytop])])
    ax.set_xlim([min([xleft, xright]), max([xleft, xright])])
    #fig.savefig("saida.png", bbox_inches='tight')
    plt.show()

def readFile(path):
    with open(path, "r") as arq:
        linhas = arq.readlines();
        colunas = [[] for i in linhas[0].split(" \t ")[:-1]];
        for linha in linhas:
            for i, ele in enumerate(linha.split(" \t ")[:-1]):
                colunas[i].append(float(ele));
        for item in colunas:
            item = np.array(item)
        
    return np.array(colunas);