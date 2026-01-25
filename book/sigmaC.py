import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def draw_sigma_c_proof():
    fig, ax = plt.subplots(figsize=(8, 6))

    # Hide standard axes
    ax.axis('off')
    
    # Define positions
    sigma_s = 1.0
    a = 2.5
    sigma_c = 4.0
    b = 5.5
    
    radius = b - sigma_s
    
    # Vertical line height (make sure it covers the circle)
    y_lim = radius + 0.5
    
    x_min = -1
    x_max = b + radius + 1
    
    # Draw Real Axis
    ax.plot([x_min, x_max], [0, 0], 'k', linewidth=1.5)
    # Add arrow at the end
    ax.plot(x_max, 0, '>k', markersize=6, clip_on=False)
    ax.text(x_max, -0.8, r'$\mathrm{Re}\ s$', fontsize=24, ha='center')

    # Draw vertical dashed lines at sigma_s and sigma_c
    # Requirement 1: Equal length up and down
    ax.plot([sigma_s, sigma_s], [-y_lim, y_lim], 'k--', linewidth=1)
    ax.plot([sigma_c, sigma_c], [-y_lim, y_lim], 'k--', linewidth=1)

    # Mark points on the real axis
    # Requirement 2: Offset text for sigma_c and sigma_s
    
    # sigma_s
    ax.plot(sigma_s, 0, 'ko', markersize=4)
    ax.text(sigma_s - 0.3, -0.8, r'$\sigma_s$', fontsize=24, ha='center')
    
    # a
    ax.plot(a, 0, 'ko', markersize=4)
    ax.text(a, -0.8, r'$a$', fontsize=24, ha='center')
    
    # sigma_c
    ax.plot(sigma_c, 0, 'ko', markersize=4)
    ax.text(sigma_c + 0.3, -0.8, r'$\sigma_c$', fontsize=24, ha='center')
    
    # b
    ax.plot(b, 0, 'ko', markersize=4)
    ax.text(b, -0.8, r'$b$', fontsize=24, ha='center')

    # Requirement 3: Circle centered at b, tangent to sigma_s line
    # Radius is b - sigma_s
    # Using a different linestyle (dashdot)
    circle = patches.Circle((b, 0), radius, fill=False, linestyle='-.', edgecolor='k', linewidth=1.5)
    ax.add_patch(circle)

    # Set limits to ensure everything is visible
    ax.set_xlim(x_min, x_max + 0.2)
    ax.set_ylim(-y_lim - 0.2, y_lim + 0.2)
    ax.set_aspect('equal')
    
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    draw_sigma_c_proof()
