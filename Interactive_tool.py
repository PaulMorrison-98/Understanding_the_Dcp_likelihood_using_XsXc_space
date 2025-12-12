import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.gridspec import GridSpec

# ----- Constants -----
T = np.linspace(-np.pi, np.pi, 800)
cosT = np.cos(T)
sinT = np.sin(T)

# Surface grid (fixed)
xs = np.linspace(-5, 5, 120)
ys = np.linspace(-6, 6, 120)
X, Y = np.meshgrid(xs, ys)

# Ellipse angle grid (fixed)
tt = np.linspace(0, 2*np.pi, 400)
cos_tt = np.cos(tt)
sin_tt = np.sin(tt)

# ----- Figure & axes -----
fig = plt.figure(figsize=(15, 6))
gs = GridSpec(1, 3, width_ratios=[1, 2, 1], figure=fig)
ax_z  = fig.add_subplot(gs[0, 0])
ax_3d = fig.add_subplot(gs[0, 1], projection='3d')
ax_xy = fig.add_subplot(gs[0, 2])

fig.subplots_adjust(left=0.05, right=0.97, top=0.97, bottom=0.20, wspace=0.03)

# -------------------------------------------------------------------
# Sliders 
# -------------------------------------------------------------------
slider_y1 = 0.10
slider_y2 = 0.05
slider_w  = 0.14
slider_h  = 0.03

# [left, bottom, width, height]

ax_a   = plt.axes([0.05, slider_y1, slider_w, slider_h])
ax_b   = plt.axes([0.23, slider_y1, slider_w, slider_h])
ax_al  = plt.axes([0.41, slider_y1, slider_w, slider_h])
ax_be  = plt.axes([0.59, slider_y1, slider_w, slider_h])
ax_z0  = plt.axes([0.77, slider_y1, slider_w, slider_h])
ax_r   = plt.axes([0.05, slider_y2, slider_w, slider_h])

# Slider objects
sa  = Slider(ax_a,  r'$Xc_{0}$', -5.0, 5.0, valinit=0.0)
sb  = Slider(ax_b,  r'$Xs_{0}$', -4.0, 4.0, valinit=1.0)
sal = Slider(ax_al, r'$\Sigma_{Xc}$', 0.0, 2.0, valinit=0.08)
sbe = Slider(ax_be, r'$\Sigma_{Xs}$', 0.0, 2.0, valinit=1.27)
sz0 = Slider(ax_z0, 'z₀', 0.0, 16, valinit=4.0)
sr  = Slider(ax_r, r'$\theta$', -np.pi, np.pi, valinit=0.0)

for s in (sa, sb, sal, sbe, sz0, sr):
    s.label.set_fontsize(18)
    s.valtext.set_alpha(0)

#########################################################
########################################################

def set_xy_equal(ax):
    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()

    max_range = max(xlim[1] - xlim[0], ylim[1] - ylim[0]) / 2
    midx = (xlim[0] + xlim[1]) / 2
    midy = (ylim[0] + ylim[1]) / 2

    ax.set_xlim3d(midx - max_range, midx + max_range)
    ax.set_ylim3d(midy - max_range, midy + max_range)

def draw(a, b, alpha, beta, z0, theta):

    # Precompute sin/cos(theta) once
    cth = np.cos(theta)
    sth = np.sin(theta)

    # ---- Curve coordinates (not rotated) ----
    # y = Xc, x = Xs in your current labelling
    y = a + cosT
    x = b + sinT

    # ---- PARABOLOID ROTATION (precomputed X, Y grid) ----
    Xp =  X*cth - Y*sth
    Yp =  X*sth + Y*cth

    Z = alpha * Yp**2 + beta * Xp**2

    # ---- Evaluate curve height on rotated paraboloid ----
    xp =  x*cth - y*sth
    yp =  x*sth + y*cth
    z  =  alpha*yp**2 + beta*xp**2

    # ---- LEFT PANEL ----
    ax_z.clear()
    ax_z.plot(T, z, lw=3, color='orange')
    ax_z.axhline(z0, ls='--', lw=3)
    ax_z.set_xlabel(r"$\delta_{CP}$", fontsize=18)
    ax_z.set_ylabel(r"$\chi^2$", fontsize=18)
    ax_z.set_xlim(-np.pi, np.pi)
    ax_z.set_ylim(0, max(16, np.max(z) + 1))

    # ---- 3D SURFACE ----
    ax_3d.clear()
    ax_3d.plot_surface(X, Y, Z, rstride=6, cstride=6, linewidth=0, alpha=0.6)
    ax_3d.plot3D(x, y, z, lw=3, color='orange')

    ax_3d.set_xlim(-6, 6)
    ax_3d.set_ylim(-5, 5)
    ax_3d.set_zlim(0, max(16, np.max(Z)))

    # Force square XY (Xc–Xs)
    set_xy_equal(ax_3d)

    ax_3d.set_xlabel(r"$X_s$", fontsize=16)
    ax_3d.set_ylabel(r"$X_c$", fontsize=16)
    ax_3d.set_zlabel(r"$\chi^2$", fontsize=18)

    ax_3d.set_xticklabels([])
    ax_3d.set_yticklabels([])
    ax_3d.set_zticklabels([])

    # ---- RIGHT PANEL (XY projection) ----
    ax_xy.clear()
    ax_xy.set_xlabel(r"$X_s$", fontsize=16)
    ax_xy.set_ylabel(r"$X_c$", fontsize=16)

    ax_xy.plot(x, y, lw=3, color='orange')

    # Rotated ellipse for z = z0
    if z0 > 0 and alpha > 0 and beta > 0:

        ax1 = np.sqrt(z0/beta)
        ax2 = np.sqrt(z0/alpha)

        ex = ax1 * cos_tt
        ey = ax2 * sin_tt

        ex_rot = ex*np.cos(-theta) - ey*np.sin(-theta)
        ey_rot = ex*np.sin(-theta) + ey*np.cos(-theta)

        ax_xy.plot(ex_rot, ey_rot, lw=3, ls='--')

    ax_xy.set_xlim(-4, 4)
    ax_xy.set_ylim(-6, 6)
    ax_xy.set_aspect('equal', adjustable='box')

    ax_xy.scatter(0, 0, s=80, color='blue', zorder=5)

    ax_xy.set_xticklabels([])
    ax_xy.set_yticklabels([])

    fig.canvas.draw_idle()


def on_change(_):
    draw(sa.val, sb.val, sal.val, sbe.val, sz0.val, sr.val)

sa.on_changed(on_change)
sb.on_changed(on_change)
sal.on_changed(on_change)
sbe.on_changed(on_change)
sz0.on_changed(on_change)
sr.on_changed(on_change)

draw(sa.val, sb.val, sal.val, sbe.val, sz0.val, sr.val)

plt.show()
