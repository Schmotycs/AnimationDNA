import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# --- Parameter ---
turns = 2
points = 100
radius = 1
height = 10
strand_radius = 0.08
base_radius = 0.05
pairs_per_half_turn = 5

z = np.linspace(0, height, points)
theta = np.linspace(0, 2*np.pi*turns, points)
num_pairs = int(pairs_per_half_turn*2*turns)
pair_indices = np.linspace(0, points-1, num_pairs, dtype=int)

# --- 3D-Zylinder-Funktion ---
def make_cylinder_between(p1, p2, r=0.05, segments=10):
    v = p2 - p1
    L = np.linalg.norm(v)
    if L == 0:
        L = 1e-8
    v_unit = v / L
    ref = np.array([0, 0, 1]) if abs(v_unit[2]) < 0.9 else np.array([1, 0, 0])
    n1 = np.cross(v_unit, ref)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v_unit, n1)
    t = np.linspace(0, L, 2)
    phi = np.linspace(0, 2 * np.pi, segments)
    T, PHI = np.meshgrid(t, phi)
    X = p1[0] + v_unit[0] * T + r * np.cos(PHI) * n1[0] + r * np.sin(PHI) * n2[0]
    Y = p1[1] + v_unit[1] * T + r * np.cos(PHI) * n1[1] + r * np.sin(PHI) * n2[1]
    Z = p1[2] + v_unit[2] * T + r * np.cos(PHI) * n1[2] + r * np.sin(PHI) * n2[2]
    return X, Y, Z

# --- Plot vorbereiten ---
fig = plt.figure(figsize=(14, 7), facecolor='black')  # Hintergrund schwarz
ax3d = fig.add_subplot([0.025, 0.1, 0.43, 0.9], projection='3d', facecolor='black')
ax2d = fig.add_subplot([0.5, 0.1, 0.3, 0.8], facecolor='black')

ax3d.set_xlim(-3, 3)
ax3d.set_ylim(-3, 3)
ax3d.set_zlim(0, height)
ax3d.set_xticks([])
ax3d.set_yticks([])
ax3d.set_zticks([])
ax3d.view_init(elev=10, azim=0)

# --- 2D-Achse stylen ---
ax2d.set_facecolor('black')
line1, = ax2d.plot([], [], color='deepskyblue', label='Strang1')
line2, = ax2d.plot([], [], color='hotpink', label='Strang2')
ax2d.set_xlim(0, height)
ax2d.set_ylim(-radius * 1.5, radius * 1.5)
ax2d.set_xlabel('Höhe z', color='white')
ax2d.set_ylabel('x-Koordinate', color='white')
ax2d.tick_params(colors='white')
ax2d.legend(facecolor='black', edgecolor='white', labelcolor='white')
ax2d.grid(True, color='gray', alpha=0.4)

# Funktionsgleichungen über dem Plot
equation_text = (
    r"$x_1(z) = r \cdot \cos\left(2\pi \cdot \frac{Frequenz}{Höhe} \cdot z \right)$" + "\n" +
    r"$x_2(z) = - r \cdot \cos\left(2\pi \cdot \frac{Frequenz}{Höhe} \cdot z \right)$"
)
ax2d.text(0.5, 1.12, equation_text, transform=ax2d.transAxes,
          ha='center', va='bottom', fontsize=14, color='white')

# Titel oben in der Mitte
fig.suptitle("Alles Gute zum Geburtstag", fontsize=18, color='white', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])

# --- Animationsfunktion ---
def animate(frame):
    for coll in ax3d.collections[:]:
        coll.remove()
    angle = frame * 0.035
    theta_rot = theta + angle
    x1 = radius * np.cos(theta_rot)
    y1 = radius * np.sin(theta_rot)
    x2 = -radius * np.cos(theta_rot)
    y2 = -radius * np.sin(theta_rot)

    # Außenstränge
    for i in range(points - 1):
        p1 = np.array([x1[i], y1[i], z[i]])
        p2 = np.array([x1[i + 1], y1[i + 1], z[i + 1]])
        X, Y, Z = make_cylinder_between(p1, p2, strand_radius)
        ax3d.plot_surface(X, Y, Z, color='deepskyblue', linewidth=0)
        p1b = np.array([x2[i], y2[i], z[i]])
        p2b = np.array([x2[i + 1], y2[i + 1], z[i + 1]])
        X, Y, Z = make_cylinder_between(p1b, p2b, strand_radius)
        ax3d.plot_surface(X, Y, Z, color='hotpink', linewidth=0)

    # Basenpaare
    for i, idx in enumerate(pair_indices):
        p1b = np.array([x1[idx], y1[idx], z[idx]])
        p2b = np.array([x2[idx], y2[idx], z[idx]])
        color = 'gold' if i % 2 == 0 else 'limegreen'
        X, Y, Z = make_cylinder_between(p1b, p2b, base_radius)
        ax3d.plot_surface(X, Y, Z, color=color, linewidth=0)

    # Linienplot aktualisieren
    line1.set_data(z, x1)
    line2.set_data(z, x2)

    return []

# --- Animation erstellen ---
ani = FuncAnimation(fig, animate, frames=200, interval=50, blit=False)

# GIF speichern (ohne grauen Ran d)
ani.save("AnimationDNA/dna_animation.gif", writer=PillowWriter(fps=20), savefig_kwargs={'facecolor': 'black'})

plt.show()
